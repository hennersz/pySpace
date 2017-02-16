#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: groundTracks
    :platform: Unix
    :synopsis: Calculates position on earth of the satellite

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from .keplerianPropogation import propogateOrbit
from .eci2ecef import ECI2ECEF
from .ECEF2LatLong import ecef2latlong

def getGroundTracks(satData, days):
    eciData = propogateOrbit(satData['R'], satData['V'], 10, int(8640*days), satData['time'])
    
    result = []
    for step in eciData:
        res = eci2latlong(step[0], step[1], step[2])
        result.append(res)
    return result
        

def eci2latlong(R, V, time):
    pos, vel = ECI2ECEF(R,V,time)
    lat, lon, h = ecef2latlong(pos)
    return (time, lat, lon, h)
