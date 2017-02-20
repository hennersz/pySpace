#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: latlong2enu
    :platform: Unix
    :synopsis: Calculates the ENU basis for a given latitude and longitude

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import math


def calculateENUBasis(φ, λ):
    lat = math.radians(φ)
    lon = math.radians(λ)

    e = calculateE(lon)
    n = calculateN(lat, lon)
    u = calculateU(lat, lon)
    return (e, n, u)


def calculateE(λ):
    ex = -math.sin(λ)
    ey = math.cos(λ)

    return [ex, ey, 0]


def calculateN(φ, λ):
    nx = -math.cos(λ)*math.sin(φ)
    ny = -math.sin(λ)*math.sin(φ)
    nz = math.cos(φ)

    return [nx, ny, nz]


def calculateU(φ, λ):
    ux = math.cos(λ)*math.cos(φ)
    uy = math.sin(λ)*math.cos(φ)
    uz = math.sin(φ)

    return [ux, uy, uz]
