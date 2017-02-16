#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: keplerianPropogation
    :platform: Unix
    :synopsis: Calculate the postition and velocity vectors of the satellite after some time step

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import math
from .utils import normaliseAngle, normailisedAtan2, writeData
from .cart2kep import cart2kep
from .data import GM
from .solveKepler import solveKepler
from .kep2cart import calculateGausVects
import numpy as np

def propogateOrbit(R,V, δt, steps, baseTime):

    results = [(R,V, baseTime)]
    newR = R
    newV = V
    for step in range(steps):
        newR, newV = calculateOrbitStep(newR, newV, δt)
        results.append((newR, newV, baseTime + δt*(step+1)))
    return results


def calculateOrbitStep(R, V, δt):
    """Calculates the position and velocity vectors of a satellite δt seconds after 
    the epoch for RV

    Args:
        R: The position vector at time t

        V: The velocity vector at time t

        δt: The time step in seconds

    Returns:
        The position and velocity vectors at time t + δt
    """

    kep = cart2kep(R, V)
    r = math.sqrt(R[0]**2 + R[1]**2 + R[2]**2)

    Ei = calculateEccentAnom(r, kep, δt)

    newR =  calculateNewPosition(Ei, kep)
    newV = calculateNewVelocity(Ei, kep)
    
    return (list(newR),list(newV))

def calculateEccentAnom(r, kep, δt):
    """Calculates the eccentric anomoly at time t + δt

    Args:
        r: The initial scalar range (Km)

        kep: A dictionary containing the keplerian elements

        δt: The time step in seconds

    Returns:
        Float. The eccentric anomoly at time t + δt in radians
    """

    n = math.sqrt(GM/kep['a']**3)
    
    cosE0 = r*math.cos(kep['ν'])/kep['a'] + kep['e']
    sinE0 = (r*math.sin(kep['ν']))/(kep['a']*math.sqrt(1-kep['e']**2))
    E0 = normailisedAtan2(sinE0, cosE0) 

    M0 = E0 - kep['e']*math.sin(E0)

    Mi = M0 + n*δt
    
    return solveKepler(kep['e'], Mi)


def calculateNewPosition(Ei, kep):
    """Calculates the new XYZ co-ordinates for the given eccentric anomoly

    Args:
        Ei: Eccentric anomoly (Radians)

        kep: A dictionary of keplerian elements

    Returns
        The position vector of the satellite.
    """

    x = kep['a']*(math.cos(Ei) - kep['e'])
    y = kep['a']*math.sqrt(1-kep['e']**2)*math.sin(Ei)
    
    P,Q = calculateGausVects(kep['Ω'], kep['ω'], kep['i'])
    
    return np.dot(x, P) + np.dot(y, Q)

def calculateNewVelocity(Ei, kep):
    """Calculates the new UVW velocity vector for the given eccentric anomoly

    Args:
        Ei: Eccentric anomoly (Radians)

        kep: A dictionary of keplerian elements

    Returns
        The velocity vector of the satellite.
        
    """

    r = kep['a']*(1-kep['e']*math.cos(Ei))
    xdot = -math.sqrt(kep['a']*GM)*math.sin(Ei)/r
    ydot = math.sqrt(kep['a']*GM)*math.sqrt(1-kep['e']**2)*math.cos(Ei)/r

    P,Q = calculateGausVects(kep['Ω'], kep['ω'], kep['i'])

    return np.dot(xdot, P) + np.dot(ydot, Q)


