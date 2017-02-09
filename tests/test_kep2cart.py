#! /usr/bin/env python
# -*- coding: utf-8 -*-

from context import satelliteSimulator #gets all of my local packages
from satelliteSimulator.kep2cart import kep2cart
from satelliteSimulator.data import *

def nearlyEqual(a, b):
    return abs(a-b)<1e-08

def test_kep2cart():
    satellites = [jason, GPSIIR, Galileo, Intelsat]
    for satellite in satellites:
        R,V = kep2cart(satellite['keplerian'])
        for i in range(len(R)):
            assert nearlyEqual(R[i], satellite['R'][i])
        for i in range(len(V)):
            assert nearlyEqual(V[i], satellite['V'][i])
