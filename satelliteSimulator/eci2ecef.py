#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: eci2ecef
    :platform: Unix
    :synopsis: Converts coordinates in an ECI basis to an ECEF basis

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from .data import BASETIME, EARTHRR
import math


def calculateGAST(time):
    difference = time - BASETIME
    days = difference/(60*60*24)
    return math.radians(280.4606 + 360.9856473662*days)

def calculateECEFPos(R, Θ):
    Xf = math.cos(Θ)*R[0] + math.sin(Θ)*R[1]
    Yf = -math.sin(Θ)*R[0] + math.cos(Θ)*R[1]

    return [Xf, Yf, R[2]]

def calculateECEFVel(R, V, Θ):
    Uf = -EARTHRR*(math.sin(Θ)*R[0] - math.cos(Θ)*R[1]) + math.cos(Θ)*V[0] + math.sin(Θ)*V[1]
    Vf = -EARTHRR*(math.cos(Θ)*R[0] + math.sin(Θ)*R[1]) - math.sin(Θ)*V[0] + math.cos(Θ)*V[1]

    return [Uf, Vf, V[2]]

def ECI2ECEF(R,V, time):
    Θ = calculateGAST(time);

    pos = calculateECEFPos(R, Θ)
    vel = calculateECEFVel(R, V, Θ)

    return pos + vel
