#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: solveKepler
    :platform: Unix
    :synopsis: Solves keplers equation numerically

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import math


def f(E, M, e):
    """Keplers equation rearranged to equal 0. Hence this will return
    0 when you have the root of the equation.

    Args:
        E: Eccentric Anomoly (Radians)

        M: Mean Anomoly (Radians)

        e: The eccentricity

    Returns:
        Float

    """
    return E - e * math.sin(E) - M


def solveKepler(e, M):
    """Solves keplers equation numerically using
       newtons method.

    Args:
        e: The eccentricity

        M: The mean anomoly

    Returns:
        Float. the eccentric anomoly that corresponds to M
    """
    if e > 0.8:
        E = math.pi
    else:
        E = M

    # run loop until the result is sufficiently small
    while abs(f(E, M, e)) > 1e-8:
        E = E - (E - e*math.sin(E) - M)/(1 - e*math.cos(E))

    return E
