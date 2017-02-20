#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: ECEF2LatLong
    :platform: Unix
    :synopsis: Converts ECEF coordinates to latitude and longitude

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..utils import normalisedAtan2
import math

def calculateLatLon(R):
    longitude = normalisedAtan2(R[1], R[0])
    latitude = math.atan(R[2]/math.sqrt(R[0]**2 + R[1]**2))
    longitude = math.degrees(longitude)
    latitude = math.degrees(latitude)
    if(longitude > 180):
        longitude -= 360
    return (longitude, latitude)

def calulateHeight(R):
    return math.sqrt(R[0]**2 + R[1]**2 + R[2]**2) - 6367 #average radius of earth

def ecef2latlong(R):
    lon, lat = calculateLatLon(R)
    height = calulateHeight(R)
    return (lat, lon, height)
