#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: main
    :platform: Unix
    :synopsis: Main file to run the simulator from

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from satelliteSimulator.plot import plotECI
from satelliteSimulator.utils import readData,writeData
from satelliteSimulator.keplerianPropogation import propogateOrbit
from satelliteSimulator.data import *
import numpy as np

results = propogateOrbit(jason['R'], jason['V'], 10, 10000, jason['time'])
writeData(results, './data/kepProp.csv')
