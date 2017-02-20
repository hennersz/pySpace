#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: groundTracks
    :platform: Unix
    :synopsis: Calculates position on earth of the satellite

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..converters.ecef2latlong import ecef2latlong


def getGroundTracks(ecefPos):
    result = []
    for step in ecefPos:
        res = ecef2latlong(step)
        result.append(res)
    return result
