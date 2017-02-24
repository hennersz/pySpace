#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: visibility
    :platform: Unix
    :synopsis: Determines if a satellite is visible from a point on earth

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..converters.ecef2latlong import ecef2latlong
from ..converters.latlong2enu import calculateENUBasis, calculateU
from ..data import EARTHRADIUS
from ..utils import normalisedAtan2
from numpy import linalg as LA
import numpy as np
import math
import progressbar


def getBasis(R):
    """Calculates an enu basis from an ecef point

    Args:
        R: Array (float): An array representing a position vector in ECEF
        space (km).

    Returns:
        Tuple: The e, n, and u unit vectors
    """
    lat, lon, h = ecef2latlong(R)
    e, n, u = calculateENUBasis(lat, lon)
    return (e, n, u)


def getS2TSVector(Rs, Rp):
    """Finds the vector between the two points given then projects it onto
    an enu basis.

    Args:
        Rs: Array (float): The position of the satellite in an ECEF basis (km).

        Rp: Array (float): The position of the trackign staiton in an ECEF
        basis (km).
    """
    rss = np.array(Rs) - np.array(Rp)
    Rss = rss/LA.norm(rss)

    e, n, u = getBasis(Rp)
    rsse = np.dot(Rss, e)
    rssn = np.dot(Rss, n)
    rssu = np.dot(Rss, u)

    return (rsse, rssn, rssu)


def calculateAngle(rsse, rssn, rssu):
    """Calculates the angle from north and the satellite elevation angle

    Args:
        rsse, rssn, rssu: The vector between station and satellite projected
        onto the enu basis for the station.

    Returns
        Tuple: θ is the satellite elevation angle (degress) and α is the
        angle from north (degrees)
    """
    θ = math.asin(rssu)
    α = normalisedAtan2(rsse, rssn)
    θ = math.degrees(θ)
    α = math.degrees(α)

    return(θ, α)


def latLon2ecef(lat, lon):
    """Converts a latitude and longitude into an ECEF position vector on the
    surface of the earth

    Args:
        lat (float): Latitude in degrees between 90 and -90

        lon (float): Longitude in degrees between 180 and -180

    Returns:
        Array (float): An ECEF position vector(km).
    """
    u = calculateU(math.radians(lat), math.radians(lon))
    U = np.array(u)
    ecef = U*EARTHRADIUS
    return list(ecef)


def isVisible(Rs, lat, lon, maskingAngle):
    """Determines if a satellite is visible from a tracking station

    Args:
        Rs: Array (float): The position vector of the satellite in ECEF
        space (km).

        lat, lon: float: The latitiude and longitude of the tracking
        station (degrees)

        maskingAngle: float: The minimum elevation at which the tracking
        station can see (degres)

    Returns:
        Bool
    """
    Rp = latLon2ecef(lat, lon)
    rsse, rssn, rssu = getS2TSVector(Rs, Rp)
    θ, α = calculateAngle(rsse, rssn, rssu)

    if θ - maskingAngle > 0:
        return True
    else:
        return False


def stationVisibility(Rs, stations):
    """Determines if a point is visible from any of the stations given

    Args:
        Rs: Array (float): The position of the satellite in ECEF
        space (km).

        stations: Array (tuple): A list of staion latitudes,
        longitudes and masking angles

    Returns:
        Bool.
    """
    for station in stations:
        vis = isVisible(Rs, station[0], station[1], station[2])
        if vis:
            return True

    return False


def getStationPassTimes(ecefData, station):
    """Gets a list of pass times for a station 
    
    Args:
        ecefData: Array: A list of ecef positions
        
        station: Tuple: The lat lon and masking angle of the station
        
    Returns:
        Array: A list of stations with the rise time, set time,
        rise angle and set angle
    """
    seenPrev = False
    res = []
    currStartTime = 0
    θ = 0
    α = 0
    for step in ecefData:
        vis = isVisible(step[0], station[0], station[1], station[2])
        if vis and not seenPrev:
            currStartTime = step[2]
            seenPrev = True
            Rp = latLon2ecef(station[0], station[1])
            rsse, rssn, rssu = getS2TSVector(step[0], Rp)
            θ, α = calculateAngle(rsse, rssn, rssu)
        elif not vis and seenPrev:
            res.append((station[0], station[1], currStartTime, step[2], step[2]-currStartTime, θ, α))
            seenPrev = False
    return res


def allPassTimes(ecefData):
    """ Creates a grid of stations set 10 degrees apart and calculates the 
    total time the satellite is visible from each station
    
    Args:
        ecefData: Array: List of ecef positions
       
    Returns:
        Array: A list of station postions and the total time the 
        satellite is visible.
    """
    stations = []
    for lat in range(19):
        for lon in range(37):
            stations.append(((lat-9)*10, (lon-18)*10, 5)) # All stations have a masking angle of 5 degrees.
    res = []
    bar = progressbar.ProgressBar(redirect_stdout=True, max_value=len(stations)) # This takes a while so progress bar is reassuring
    stationsProcessed = 0
    for station in stations:
        passTimes = getStationPassTimes(ecefData, station)
        totalPassTime = 0
        for step in passTimes:
            totalPassTime += step[1] - step[0]
        res.append((station[0], station[1], totalPassTime))
        stationsProcessed += 1
        bar.update(stationsProcessed)

    return res
