#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: cart2kep
    :platform: Unix
    :synopsis: Convert cartesian elements to keplerian elements

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..data import GM
from ..utils import normaliseAngle, normalisedAtan2
import numpy as np
from numpy import linalg as LA
import math


def cart2kep(R, V):
    """Converts cartesian elements to keplerian elements

    Args:
        R: An array of floats containing the XYZ co-ordinates
            of the satellite for an ECI basis in Km.
        V: An array of floats containing the velocities uvw of 
            the satellite for an ECI basis in Km/s

    Returns:
        A dictionary mapping the symbols for the keplerian 
        elements to the calculated values. e.g:: 

            {
              'a':26559.45536811388409 ,
              'e':0.0028139222014726429,
              'i':0.9077268890773122381,
              'Ω':5.063017814062672041,
              'ω':0.06663686045640246166,
              'ν':4.266175869989886267
            }

        where: 
            a: Semi-major axis(Km)

            e: Eccentricity

            i: Inclination (Radians)

            Ω: RAAN (Radians)

            ω: Argument of Perigee (Radians)

            ν: True Anomoly (Radians)

    """

    h̅ = np.cross(R,V)
    W̅ = calculateUnitOrbitNormal(h̅)
    i = calculateInclination(W̅)
    Ω = calculateRAAN(W̅)
    a = calculateSemiMajAxis(R,V)
    p = calculateP(h̅)
    e = calculateEccentricity(a,p)
    n = calculateMeanMotion(a)
    E = calculateE(R, V, a, n)
    ν = calculateTrueAnom(E, e)
    u = calculateU(R, i, Ω)
    ω = calculateArgofPer(u, ν)

    return {
            'a':a,
            'e':e,
            'i':normaliseAngle(i),
            'Ω':normaliseAngle(Ω),
            'ω':normaliseAngle(ω),
            'ν':normaliseAngle(ν)
            }



def calculateUnitOrbitNormal(h̅):
    """Calculates the unit vector normal to the orbit

    Args:
        h̅ (array): An array of floats representing the orbit normal, obtained from RxV 

    Returns:
        float. The unit orbit normal
    """
    h = LA.norm(h̅)
    Wx = h̅[0]/h
    Wy = h̅[1]/h
    Wz = h̅[2]/h
    W̅ = [Wx, Wy, Wz]
    return W̅

def calculateInclination(W̅):
    """Calculates the inclination from the unit orbit normal

    Args:
        W̅ (float): Unit orbit normal

    Returns:
        float. The inclination in radians
    """
    numerator = math.sqrt(W̅[0]**2 + W̅[1]**2)
    return normalisedAtan2(numerator, W̅[2])

def calculateRAAN(W̅):
    """Calculates the RAAN from the unit orbit normal

    Args:
        W̅ (float): Unit orbit normal

    Returns:
        float. The inclination in radians
    """
    return normalisedAtan2(W̅[0],-W̅[1])

def vectorLength(vector):
    """Calculates the length of a vector using the pythagorean theorem

    Args:
        vector (array): An array of floats representing a 3d vector

    Returns:
        float. The scalar length of the vector
    """
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def calculateP(h̅):
    """Calculates the semi-latus rectum

    Args:
        h̅ (array): An array of floats representing the orbit normal, obtained from RxV 

    Returns:
        float. The semi-latus rectum
    """
    h = LA.norm(h̅)
    return h**2/GM

def calculateSemiMajAxis(R, V):
    """Calculates the semi-major axis

    Args:
        R (array): An array of floats representing the position vector of the satellite

        V (array): An array of floats representing the velocity vector of the satellite

    Returns:
        float. The semi-major axis
    
    """
    r = vectorLength(R)
    v = vectorLength(V)
    return 1/(2/r - v**2/GM)

def calculateEccentricity(a, p):
    """Calculates the eccentricity of the orbit

    Args:
        a (float): The semi-major axis

        p (float): The semi-latus rectum

    Returns:
        float. The eccentricity
    """
    return math.sqrt(1-p/a)

def calculateMeanMotion(a):
    """Calculates the mean motion of the orbit

    Args:
        a (float): The semi-major axis

    Returns:
        float. The mean motion in radians/s
    """
    return math.sqrt(GM/a**3)

def calculateE(R, V, a, n):
    """Calculates the eccentric anomaly
    
    Args:
        R (array): An array of floats representing the position vector of the satellite

        V (array): An array of floats representing the velocity vector of the satellite

        a (float): The semi-major axis

        n (float): The mean motion

    Returns:
        float. The eccentric anomaly in radians
    """
    rv = np.dot(R,V)
    r = LA.norm(R)
    numerator = rv/(a**2*n)
    denominator = 1 - r/a
    return normalisedAtan2(numerator, denominator)

def calculateU(R, i, Ω):
    """Calculates the argument of latitude

    Args:
        R (array): An array of floats representing the position vector of the satellite

        i (float): The inclination in radians

        Ω (float): The RAAN in radians

    Returns:
        float. The argument of latitude in radians
    """
    numerator = R[2]/math.sin(i)
    denominator = R[0]*math.cos(Ω) + R[1]*math.sin(Ω)
    return normalisedAtan2(numerator,denominator)

def calculateTrueAnom(E,e):
    """Calculates the True anomaly

    Args:
        E (float): The eccentric anomaly in radians

        e (float): The eccentricity of the orbit

    Returns:
        float. The true anomaly in radians
    """
    numerator = math.sqrt(1 - e**2) * math.sin(E)
    denominator = math.cos(E) - e
    return normalisedAtan2(numerator, denominator)

def calculateArgofPer(u, ν):
    """Calculates the argument of perigee

    Args:
        u (float): The argument of latitude in radians

        ν (float): The true anomaly in radians

    Returns:
        float. The argument of perigee in radians
    """
    return u - ν
