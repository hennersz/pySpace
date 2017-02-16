#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: main
    :platform: Unix
    :synopsis: Main file to run the simulator from

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from satelliteSimulator.plot import plotGroundTracks
from satelliteSimulator.utils import readData,writeData
from satelliteSimulator.keplerianPropogation import propogateOrbit
from satelliteSimulator.data import *
from satelliteSimulator.groundTracks import getGroundTracks
import numpy as np

data = getGroundTracks(jason, 1)
writeData(data, './data/groundTracks.csv')
plotGroundTracks(data)
