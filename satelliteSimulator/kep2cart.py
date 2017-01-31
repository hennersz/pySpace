#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: kep2cart
    :platform: Unix
    :synopsis: Convert keplerian elements to cartesian elements

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import math

def calculateGausVects(Ω, ω, i):
    """Calculates the gaussian vectors

    Args:
        Ω (float): The RAAN (Radians)

        ω (float): The argument of perigee (Radians)

        i (float): The inclination (radians)

    Returns:
        A tuple containing the P and Q vectors
    """

    P = calculateP(Ω, ω, i)
    Q = calculateQ(Ω, ω, i)
    return (P, Q)

def calculateP(Ω, ω, i):
    """Calculates the P gaussian vector

    Args:
        Ω (float): The RAAN (Radians)

        ω (float): The argument of perigee (Radians)

        i (float): The inclination (radians)

    Returns:
        An array of floats representing the P vector
    """
    px = math.cos(Ω)*math.cos(ω) - math.sin(Ω)*math.cos(i)*math.sin(ω)
    py = math.sin(Ω)*math.cos(ω) - math.cos(Ω)*math.cos(i)*math.sin(ω)
    pz = math.sin(i)*math.sin(ω)
    return [px, py, pz]

def calculateQ(Ω, ω, i):
    """Calculates the Q gaussian vector

    Args:
        Ω (float): The RAAN (Radians)

        ω (float): The argument of perigee (Radians)

        i (float): The inclination (radians)

    Returns:
        An array of floats representing the Q vector
    """
    qx = -math.cos(Ω)*math.sin(ω) - math.sin(Ω)*math.cos(i)*math.cos(ω)
    qy = -math.sin(Ω)*math.sin(ω) - math.cos(Ω)*math.cos(i)*math.cos(ω)
    qz = math.sin(i)*math.cos(ω)
    return [px, py, pz]
