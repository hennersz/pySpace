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
