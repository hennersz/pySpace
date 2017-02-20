#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: differences
    :platform: Unix
    :synopsis: Calculates the differences between two points in an orbit

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import numpy as np
from numpy import linalg as LA
from ..converters.latlong2enu import calculateENUBasis
from ..converters.eci2ecef import ECI2ECEF


def calculateVectorDiff(X1, X2):
    x1 = np.array(X1)
    x2 = np.array(X2)
    return list(x2 - x1)


def calculateH(R):
    h = np.array(R)/LA.norm(R)
    return list(h)


def calculateC(R, V):
    cross = np.cross(R, V)
    norm = LA.norm(cross)
    return list(cross/norm)


def calculateL(C, H):
    return list(np.cross(C, H))


def calculateBasis(R, V):
    H = calculateH(R)
    C = calculateC(R, V)
    L = calculateL(C, H)

    return (H, C, L)


def projectOntoBasis(x, y, z, ΔX):
    ΔXx = np.dot(x, ΔX)
    ΔXy = np.dot(y, ΔX)
    ΔXz = np.dot(z, ΔX)

    return (ΔXx, ΔXy, ΔXz)


def HCLDiff(X1, X2):
    diff = calculateVectorDiff(X1[0], X2[0])
    H, C, L = calculateBasis(X1[0], X1[1])

    return projectOntoBasis(H, C, L, diff)


def ENUDiff(X1, X2, station, time):
    e, n, u = calculateENUBasis(station[0], station[1])
    X1ecef = ECI2ECEF(X1[0], X1[1], time)
    X2ecef = ECI2ECEF(X2[0], X2[1], time)

    diff = calculateVectorDiff(X1ecef[0], X2ecef[0])
    return projectOntoBasis(e, n, u, diff)
