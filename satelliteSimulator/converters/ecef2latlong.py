#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: ECEF2LatLong
    :platform: Unix
    :synopsis: Converts ECEF coordinates to latitude and longitude

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..utils import normalisedAtan2
from ..data import EARTHRADIUS
import math


def calculateLatLon(R):
    """Calculates the latitude and longitude from an ECEF position

    Args:
        R: Array (float): A position in ECEF space (km).

    Returns:
        Tuple: Latitiude and longitude in degrees
    """
    longitude = normalisedAtan2(R[1], R[0])
    latitude = math.atan(R[2]/math.sqrt(R[0]**2 + R[1]**2))

    longitude = math.degrees(longitude)
    latitude = math.degrees(latitude)

    if(longitude > 180):
        longitude -= 360
    return (longitude, latitude)


def calulateHeight(R):
    """Calculates how high above the surface of the earth an ECEF point is

    Args:
        R: Array (float): A position in ECEF space (km).

    Returns:
        Float: The height above the earth surface (km).
    """
    return math.sqrt(R[0]**2 + R[1]**2 + R[2]**2) - EARTHRADIUS


def ecef2latlong(R):
    """Converts a ECEF point to latitude, longitude and height.

    Args:
        R: Array (float): A position in ECEF space (km).

    Returns:
        Tuple: The latitude and longitude (degrees) and heigh (km).
    """
    lon, lat = calculateLatLon(R)
    height = calulateHeight(R)
    return (lat, lon, height)
