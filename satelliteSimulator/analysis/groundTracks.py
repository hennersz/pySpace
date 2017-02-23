#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: groundTracks
    :platform: Unix
    :synopsis: Calculates position on earth of the satellite

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..converters.ecef2latlong import ecef2latlong
from .visibility import stationVisibility


def getGroundTracks(ecefPos, stations):
    """Gets the ground track for an array of ECEF positions

    Args:
        ecefPos: Array: An array of position and velocity vectors (km)


    Returns
        Array: An array of latitudes and longitudes (degrees)
    """
    result = []
    for step in ecefPos:
        visible = stationVisibility(step, stations)
        res = ecef2latlong(step)
        result.append((res, visible))
    return result
