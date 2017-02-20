#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: main
    :platform: Unix
    :synopsis: Main file to run the simulator from

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from satelliteSimulator.propogation.rk4 import rk4Propogation
from satelliteSimulator.propogation.keplerianPropogation import propogateOrbit
from satelliteSimulator.data import jason
from satelliteSimulator.analysis.groundTracks import getGroundTracks
from satelliteSimulator.plot import plotGroundTracks
from satelliteSimulator.converters.eci2ecef import ECI2ECEF
from satelliteSimulator.analysis.visibility import isVisible
from mpl_toolkits.basemap import Basemap
from satelliteSimulator.analysis.differences import HCLDiff, ENUDiff
import matplotlib.pyplot as plt
import numpy as np


def initMap():
    m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180)
    m.drawcoastlines()
    m.fillcontinents(color='#209101', lake_color='#0A369D')

    # draw parallels and meridians.
    m.drawparallels(np.arange(-90., 91., 30.))
    m.drawmeridians(np.arange(-180., 181., 60.))
    m.drawmapboundary(fill_color='#0A369D')

    return m


def main():
    #m = initMap()
    rk4 = rk4Propogation(jason['R'], jason['V'], 10, 8640, jason['time'])
    kep = propogateOrbit(jason['R'], jason['V'], 10, 8640, jason['time'])
    diffs1 = []
    diffs2 = []
    for r, k in zip(rk4, kep):
        diffs1.append((r[2],)+HCLDiff((r[0], r[1]), (k[0], k[1])))
    for r, k in zip(rk4, kep):
        diffs2.append((r[2],)+ENUDiff((r[0], r[1]), (k[0], k[1]), (51, -0.5), r[2]))

    plt.scatter([x[0] for x in diffs2], [x[1] for x in diffs2], marker='.', color='k', s=1)
    plt.scatter([x[0] for x in diffs2], [x[2] for x in diffs2], marker='.', color='b', s=1)
    plt.scatter([x[0] for x in diffs2], [x[3] for x in diffs2], marker='.', color='r', s=1)

    plt.show()
    # ecefData = []
    # for step in eciData:
    #     ecefData.append(ECI2ECEF(step[0], step[1], step[2]))

    # groundTracks = getGroundTracks([x[0] for x in ecefData if isVisible(x[0], 51.32, -0.5, 5)])
    # plotGroundTracks(groundTracks, 'y', m)
    # groundTracks = getGroundTracks([x[0] for x in ecefData if not isVisible(x[0], 51.32, -0.5, 5)])
    # plotGroundTracks(groundTracks, 'k', m)
    # plt.title("Ground Tracks")
    # plt.show()


if __name__ == '__main__':
    main()
