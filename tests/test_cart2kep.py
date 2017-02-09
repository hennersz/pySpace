#! /usr/bin/env python
# -*- coding: utf-8 -*-

from context import satelliteSimulator #gets all of my local packages
from satelliteSimulator.cart2kep import cart2kep
from satelliteSimulator.data import *
from math import pi
import pytest

def nearlyEqual(a, b):
    return abs(a-b)<1e-08

# def test_normalisedAtan2():
#     assert normailisedAtan2(1,1) == 0.7853981633974483
#     assert normailisedAtan2(1,-1) == 2.356194490192345
#     assert normailisedAtan2(-1, 1) == 5.497787143782138
#     assert normailisedAtan2(-1, -1) == 3.9269908169872414

# def test_normailseAngle():
#     assert normaliseAngle(1.112324) == 1.112324
#     assert normaliseAngle(7.1) == 0.8168146928204134
#     assert normaliseAngle(-pi) == 3.141592653589793

def test_cart2kep():
    satellites = [jason, GPSIIR, Galileo, Intelsat]
    for satellite in satellites:
        result = cart2kep(satellite['R'], satellite['V'])
        for key in satellite['keplerian']:
            assert nearlyEqual(satellite['keplerian'][key], result[key])
