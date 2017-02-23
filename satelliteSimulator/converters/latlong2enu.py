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
    """Calculates an ENU unit basis from latitude and lonitude.

    Args:
        φ: float: Latitude (degrees).

        λ: float: Longitude (degrees).

    Returns:
        Tuple: The E, N and U unit vectors
    """
    lat = math.radians(φ)
    lon = math.radians(λ)

    e = calculateE(lon)
    n = calculateN(lat, lon)
    u = calculateU(lat, lon)
    return (e, n, u)


def calculateE(λ):
    """Calculates the E (east) unit vector

    Args:
        λ: float: Longitude (degrees).

    Returns:
        Array (float). The E unit vector.
    """
    ex = -math.sin(λ)
    ey = math.cos(λ)

    return [ex, ey, 0]


def calculateN(φ, λ):
    """Calculates the N (north) unit vector

    Args:
        φ: float: Latitude (degrees).

        λ: float: Longitude (degrees).

    Returns:
        Array (float). The N unit vector.
    """
    nx = -math.cos(λ)*math.sin(φ)
    ny = -math.sin(λ)*math.sin(φ)
    nz = math.cos(φ)

    return [nx, ny, nz]


def calculateU(φ, λ):
    """Calculates the U (up) unit vector

    Args:
        φ: float: Latitude (degrees).

        λ: float: Longitude (degrees).

    Returns:
        Array (float). The U unit vector.
    """
    ux = math.cos(λ)*math.cos(φ)
    uy = math.sin(λ)*math.cos(φ)
    uz = math.sin(φ)

    return [ux, uy, uz]
