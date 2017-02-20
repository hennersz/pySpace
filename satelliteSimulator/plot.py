#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: plot
    :platform: Unix
    :synopsis: Plots graphs of satellite motion

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import matplotlib.pyplot as plt


def plotECI(data):

    x = [row[0] for row in data]
    y = [row[1] for row in data]
    z = [row[2] for row in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, c='r', marker='o')

    plt.show()


def plotGroundTracks(data, colour, m):
    lats = [x[0] for x in data]
    lons = [x[1] for x in data]

    x, y = m(lons, lats)
    m.plot(x, y, marker='o', linestyle='None', markersize=0.5,  color=colour)
