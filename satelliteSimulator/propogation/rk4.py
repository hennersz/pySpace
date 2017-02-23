#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: rk4
    :platform: Unix
    :synopsis: Propogates a satellites orbit using the classic Runge-Kutta
         method of solving differential equations

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from ..data import GM, AEGMA96, C20
import numpy as np
from numpy import linalg as LA
import math


def monopoleDiff(r0, R):
    """The differential equation for a monopole gravity model

    Args:
        r0: float: The norm of R.

        R: Array (float): Position vector in ECI space (km)
    """
    x = -(GM*R[0])/r0**3
    y = -(GM*R[1])/r0**3
    z = -(GM*R[2])/r0**3

    return [x, y, z]


def monopoleK(R, h):
    """The k function for monopole gravity

    Args:
        R: Array (float): Position vector in ECI space (km).

        h: The step size in seconds.

    Returns:
        Array (float).
    """
    r0 = LA.norm(R)
    KR = np.array(monopoleDiff(r0, R))
    KR *= (0.5*h**2)
    return list(KR)


def calculateRk2(K1R, V, R, h):
    """Calculates RK2 and RK3

    Args:
        K1R: Array (float): The result of K1 (or K2 when calculating RK3)

        V: Array (float): The velocity vector in ECI space.

        R: Array (float): The psoition vector in ECI Space.

        h: float: The time step in seconds.

    Returns:
        Array (float).
    """
    x = R[0] + h/2*V[0] + K1R[0]/4
    y = R[1] + h/2*V[1] + K1R[1]/4
    z = R[2] + h/2*V[2] + K1R[2]/4

    return [x, y, z]


def calculateRk4(K3R, V, R, h):
    """Calculates RK4

    Args:
        K3R: Array (float): The result of K3.

        V: Array (float): The velocity vector in ECI space.

        R: Array (float): The psoition vector in ECI Space.

        h: float: The time step in seconds.

    Returns:
        Array (float).
    """
    x = R[0] + h*V[0] + K3R[0]
    y = R[1] + h*V[1] + K3R[1]
    z = R[2] + h*V[2] + K3R[2]

    return [x, y, z]


def calculateP(k1, k2, k3):
    """Calculates the P vector

    Args:
        k1: Array (float): The k1 vector

        k2: Array (float): The k2 vector

        k3: Array (float): The k3 vector

    Returns:
        Array (float): The P vector.
    """
    x = 1/3*(k1[0] + k2[0] + k3[0])
    y = 1/3*(k1[1] + k2[1] + k3[1])
    z = 1/3*(k1[2] + k2[2] + k3[2])

    return [x, y, z]


def calculateQ(k1, k2, k3, k4):
    """Calculates the Q vector

    Args:
        k1: Array (float): The k1 vector

        k2: Array (float): The k2 vector

        k3: Array (float): The k3 vector

        k4: Array (float): The k4 vector

    Returns:
        Array (float): The Q vector.
    """
    x = 1/3*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
    y = 1/3*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
    z = 1/3*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2])

    return [x, y, z]


def rk4PropogationStep(R, V, timestep, k):
    """Calculates one step of the RK4 algorithm

    Args:
        R: Array (float): The psoition vector in ECI Space.

        V: Array (float): The velocity vector in ECI space.

        timestep: int: The timestep in seconds.

        k: function: The k function to use (monopole or J2)

    Returns:
        Tuple: The position and velocity vectors after timestep.
    """
    k1 = k(R, timestep)
    RK2 = calculateRk2(k1, V, R, timestep)
    k2 = k(RK2, timestep)
    RK3 = calculateRk2(k2, V, R, timestep)
    k3 = k(RK3, timestep)
    RK4 = calculateRk4(k3, V, R, timestep)
    k4 = k(RK4, timestep)

    P = calculateP(k1, k2, k3)
    Q = calculateQ(k1, k2, k3, k4)

    x = R[0] + timestep*V[0] + P[0]
    y = R[1] + timestep*V[1] + P[1]
    z = R[2] + timestep*V[2] + P[2]

    u = V[0] + Q[0]/timestep
    v = V[1] + Q[1]/timestep
    w = V[2] + Q[2]/timestep

    return ([x, y, z], [u, v, w])


def rk4MonoPropogation(R, V, timestep, steps, baseTime):
    """Calculates an array of steps of the RK4 propogation algorithm.

    Args:
        R: Array (float): The psoition vector in ECI Space.

        V: Array (float): The velocity vector in ECI space.

        timestep: int: The timestep in seconds.

        steps: int: The number of steps to calculate.

        baseTime: float: The start time in seconds.

    Returns:
        Array: An array of steps of the algorithm.
    """
    results = [(R, V, baseTime)]
    newR = R
    newV = V
    for step in range(steps):
        newR, newV = rk4PropogationStep(newR, newV, timestep, monopoleK)
        results.append((newR, newV, baseTime + timestep*(step+1)))
    return results

# ==========================RK4-J2 functions=============================#


def kdδ(m):
    """The kroneker delta function

    Args:
        m: int: Order of expansion.

    Returns:
        1 or 0
    """
    if m == 0:
        return 1
    else:
        return 0


def denormaliseCoefficient(c, n, m):
    """Denormalises a spherical harmonic coefficent

    Args:
        c: float: The coefficient value.

        n: int: Degree of expansion.

        m: int: Order of expansion.

    Returns:
        Float.
    """
    num = math.factorial(n + m)
    den = math.factorial(n-m)*(2*n + 1)*(2-kdδ(m))
    normaliser = math.sqrt(num/den)
    return c/normaliser


def j2diff(R, r0, c, a):
    """The differential for RK4 with J2 correction

    Args:
        R: Array (float): The position vector in ECI Space.

        r0: float: The norm of R.

        c: float: The denormalised spherical harmonic coefficient

        a: float: Scale length for the expansion (km).

    Returns:
        Array (float)
    """
    x = -GM*R[0]/r0**3 + 1.5*GM*(a**2/r0**5)*c*R[0]*(1-(5*R[2]**2)/r0**2)
    y = -GM*R[1]/r0**3 + 1.5*GM*(a**2/r0**5)*c*R[1]*(1-(5*R[2]**2)/r0**2)
    z = -GM*R[2]/r0**3 + 1.5*GM*(a**2/r0**5)*c*R[2]*(3-(5*R[2]**2)/r0**2)

    return [x, y, z]


def j2k(R, h):
    """The k function for RK4 J2 propogation.

    Args:
        R: Array (float): The position vector in ECI Space.

        h: int: The timestep in seconds.

    Returns:
        Array (float).
    """
    c = denormaliseCoefficient(C20, 2, 0)
    r0 = LA.norm(R)
    KR = np.array(j2diff(R, r0, c, AEGMA96))
    KR = (0.5*h**2)*KR
    return list(KR)


def rk4j2Propogation(R, V, timestep, steps, baseTime):
    """Calculates an array of steps of the RK4 J2 propogation algorithm.

    Args:
        R: Array (float): The psoition vector in ECI Space.

        V: Array (float): The velocity vector in ECI space.

        timestep: int: The timestep in seconds.

        steps: int: The number of steps to calculate.

        baseTime: float: The start time in seconds.

    Returns:
        Array: An array of steps of the algorithm.
    """
    results = [(R, V, baseTime)]
    newR = R
    newV = V
    for step in range(steps):
        newR, newV = rk4PropogationStep(newR, newV, timestep, j2k)
        results.append((newR, newV, baseTime + timestep*(step+1)))
    return results
