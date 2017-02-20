#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: kep2cart
    :platform: Unix
    :synopsis: Convert keplerian elements to cartesian elements

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import math
from ..data import GM

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
    py = math.sin(Ω)*math.cos(ω) + math.cos(Ω)*math.cos(i)*math.sin(ω)
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
    qy = math.cos(Ω)*math.cos(i)*math.cos(ω) - math.sin(Ω)*math.sin(ω)
    qz = math.sin(i)*math.cos(ω)
    return [qx, qy, qz]

def calculateSemLatRect(a, e):
    """Calculates the semi latus rectum

    Args:
        a: Semi-major axis (Km)

        e: Eccentricity

    Returns:
        float. The semi latus rectum in Km
    """

    return a*(1-e**2)

def calculateRadDist(p, e, ν):
    """Calculates the radial distance 

    Args:
        p: Semi latus rectum (Km)

        e: Eccentricity

        ν: True Anomoly (Radians)
    """

    return p/(1 + e*math.cos(ν))

def calculatePosition(P, Q, r, ν):
    """Calculates the satellites position vector in the ECI basis

    Args:
        P: The P gaussian vector (Km)

        Q: The Q gaussian vector (Km)

        r: The radial distance (Km)

        ν: The true anomoly (Radians)

    Returns:
        Array of floats. The position vector.
    """

    x = r*math.cos(ν)
    y = r*math.sin(ν)

    X = x*P[0] + y*Q[0]
    Y = x*P[1] + y*Q[1]
    Z = x*P[2] + y*Q[2]

    return [X,Y,Z]

def calculateVelocity(ν, a ,e, r, P, Q):
    """Calculates the velocity vector

    Args:
        ν: True Anomoly (Radians)

        a: Semi-major axis (Km)

        e: Eccentricity

        r: The radial distance (Km)

        P: The P gaussian vector (Km)

        Q: The Q gaussian vector (Km)
    """
    x = r*math.cos(ν)
    y = r*math.sin(ν)

    cosE = x/a + e
    sinE = y/(a*math.sqrt(1-e**2))

    f = math.sqrt(a*GM)/r

    g = math.sqrt(1-e**2)

    U = -f*sinE*P[0] + f*g*cosE*Q[0]
    V = -f*sinE*P[1] + f*g*cosE*Q[1]
    W = -f*sinE*P[2] + f*g*cosE*Q[2]

    return [U, V, W]

def kep2cart(kep):
    P,Q = calculateGausVects(kep['Ω'], kep['ω'], kep['i'])
    p = calculateSemLatRect(kep['a'], kep['e'])
    r = calculateRadDist(p, kep['e'], kep['ν'])
    R = calculatePosition(P, Q, r, kep['ν'])
    V = calculateVelocity(kep['ν'], kep['a'], kep['e'], r, P, Q)
    return (R, V)
