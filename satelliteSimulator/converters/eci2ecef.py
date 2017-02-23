#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: eci2ecef
    :platform: Unix
    :synopsis: Converts coordinates in an ECI basis to an ECEF basis

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..data import BASETIME, EARTHRR
import math


def calculateGAST(time):
    """Calculates the Grenwich apparent siderial time from the
    12h on 1st January 2000

    Args:
        time: float: The current time in seconds

    Returns:
        Float. θGAST in radians
    """
    difference = time - BASETIME
    days = difference/(60*60*24)
    return math.radians(280.4606 + 360.9856473662*days)


def calculateECEFPos(R, Θ):
    """Calculates the ECEF positon from an ECI position

    Args:
        R: Array (float): The position vector in ECI space (km).

        θ: float: The θGAST value corresponding to R

    Returns:
        Array (float). The ECEF position vector
    """
    Xf = math.cos(Θ)*R[0] + math.sin(Θ)*R[1]
    Yf = -math.sin(Θ)*R[0] + math.cos(Θ)*R[1]

    return [Xf, Yf, R[2]]


def calculateECEFVel(R, V, Θ):
    """Calculates the ECEF velocity vector.

    Args:
        R: Array (float): The position vector in ECI space (km).

        V: Array (float): The velocity vector in ECI space (km).

        θ: float: The θGAST value corresponding to R and V

    Returns:
        Array (float): The ECEF velocity vector

    """
    Uf = -EARTHRR*(math.sin(Θ)*R[0] - math.cos(Θ)*R[1])\
        + math.cos(Θ)*V[0]\
        + math.sin(Θ)*V[1]

    Vf = -EARTHRR*(math.cos(Θ)*R[0] + math.sin(Θ)*R[1])\
        - math.sin(Θ)*V[0]\
        + math.cos(Θ)*V[1]

    return [Uf, Vf, V[2]]


def ECI2ECEF(R, V, time):
    """Converts position and velocity vectors from ECI to ECEF

    Args:
        R: Array (float): The position vector in ECI space (km).

        V: Array (float): The velocity vector in ECI space (km).

        time: float: The current time in seconds

    Returns:
        Tuple: The ECEF position and velocity vectors.
    """
    Θ = calculateGAST(time)

    pos = calculateECEFPos(R, Θ)
    vel = calculateECEFVel(R, V, Θ)

    return (pos, vel, time)
