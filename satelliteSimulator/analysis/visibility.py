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
    lat, lon, h = ecef2latlong(R)
    e, n, u = calculateENUBasis(lat, lon)
    return (e, n, u)


def getS2TSVector(Rs, Rp):
    rss = np.array(Rs) - np.array(Rp)
    Rss = rss/LA.norm(rss)

    e, n, u = getBasis(Rp)
    rsse = np.dot(Rss, e)
    rssn = np.dot(Rss, n)
    rssu = np.dot(Rss, u)

    return (rsse, rssn, rssu)


def calculateAngle(rsse, rssn, rssu):
    θ = math.asin(rssu)
    α = normalisedAtan2(rsse, rssn)
    θ = math.degrees(θ)
    α = math.degrees(α)

    return(θ, α)


def latLon2ecef(lat, lon):
    u = calculateU(math.radians(lat), math.radians(lon))
    U = np.array(u)
    ecef = U*EARTHRADIUS
    return list(ecef)


def isVisible(Rs, lat, lon, maskingAngle):
    Rp = latLon2ecef(lat, lon)
    rsse, rssn, rssu = getS2TSVector(Rs, Rp)
    θ, α = calculateAngle(rsse, rssn, rssu)

    if θ - maskingAngle > 0:
        return True
    else:
        return False
