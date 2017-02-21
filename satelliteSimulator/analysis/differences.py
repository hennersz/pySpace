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
    """Calculates the distance vector between 2 position vectors. Must be in
    the same basis e.g ECI or ECEF

    Args:
        X1: Array (float): An array representing the position vector in km.

        X2: Array (float): An array representing the position vector in km.

    Returns:
        Array (float): An array representing the distance vector between X1 and
        X2 in km
    """
    x1 = np.array(X1)
    x2 = np.array(X2)
    return list(x2 - x1)


def calculateH(R):
    """Calculates the height(distance from centre of earth) unit vector for a
    position in ECI space.

    Args:
        R: Array (float): The position of a satellite in an ECI Basis

    Returns:
        Array (float): An array representing the height unit vector
    """
    h = np.array(R)/LA.norm(R)
    return list(h)


def calculateC(R, V):
    """Calculates the cross track(perpendicular to motion) unit vector.

    Args:
        R: Array (float): The position of a satellite in an ECI Basis

        V: Array (float): The velocity of a satellite in an ECI Basis

    Returns:
        Array (float): An array representing the cross track unit vector
    """
    cross = np.cross(R, V)
    norm = LA.norm(cross)
    return list(cross/norm)


def calculateL(C, H):
    """Calculates the along (with satellite motion) unit vecto.

    Args:
        C: Array (float): The cross track unit vector

        H: Array (float): The height unit vector

    Returns:
        Array (float): An array representing the along unit vector.
    """
    return list(np.cross(C, H))


def calculateBasis(R, V):
    """Calculates the height, cross track, along track unit basis.

    Args:
        R: Array (float): The position of a satellite in an ECI Basis

        V: Array (float): The velocity of a satellite in an ECI Basis

    Returns:
        Tuple: A tuple containing the H,C,L unit vectors.
    """
    H = calculateH(R)
    C = calculateC(R, V)
    L = calculateL(C, H)

    return (H, C, L)


def projectOntoBasis(x, y, z, ΔX):
    """Projects a vector in to a unit basis

    Args:
        x, y, z: Array (float): Orthogonal unit vectors

        ΔX: Array (float): The position vector being projected

    Returns:
        Array (float): The position vector projected onto the basis
    """
    ΔXx = np.dot(x, ΔX)
    ΔXy = np.dot(y, ΔX)
    ΔXz = np.dot(z, ΔX)

    return [ΔXx, ΔXy, ΔXz]


def HCLDiff(X1, X2):
    """Calculates the distance between two positions in ECI space and projects it
    onto a HCL basis.

    Args:
        X1, X2: Array (float): Position vectors in the same basis (km)

    Returns:
        Array (float): The difference vector between the two points in an HCL
        basis.
    """
    diff = calculateVectorDiff(X1[0], X2[0])
    H, C, L = calculateBasis(X1[0], X1[1])

    return projectOntoBasis(H, C, L, diff)


def ENUDiff(X1, X2, station, time):
    """Calculates the distance between two points in an ECI basis and projects it
    onto an ENU basis given a tracking station.

    Args:
        X1, X2: Array (float): Position vectors in the same basis (km)

        stations: Tuple (float): The latitude and longitude of the station
        (degrees).

        time: float: The time when the points were sampled

    returns:
        Array (float): The difference vector between the two points in an ENU
        basis.

    """
    e, n, u = calculateENUBasis(station[0], station[1])
    X1ecef = ECI2ECEF(X1[0], X1[1], time)
    X2ecef = ECI2ECEF(X2[0], X2[1], time)

    diff = calculateVectorDiff(X1ecef[0], X2ecef[0])
    return projectOntoBasis(e, n, u, diff)
