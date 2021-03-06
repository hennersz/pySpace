#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: plot
    :platform: Unix
    :synopsis: Plots graphs of satellite motion

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from mpl_toolkits.basemap import Basemap
import numpy as np


def plotECI(data):
    """Plots ECI co-ordinates in 3d

    Args:
        data: Array: A list of XYZ coordinates (km)

    Returns
        Nothing.
    """
    x = [row[0] for row in data]
    y = [row[1] for row in data]
    z = [row[2] for row in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, c='r', marker='o')

    plt.show()


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


def plotGroundTracks(data):
    """Plots ground tracks on a 2d projection of earth.

    Args:
        data: Array: A list of latitudes and longitude in degrees

        colour: string: A matplotlib colour code for the colour of the
        points plotted

        m: A Basemap projection object.

    Returns:
        None.
    """
    m = initMap()

    vlats = [x[0] for x in data if x[3]]
    vlons = [x[1] for x in data if x[3]]
    hlats = [x[0] for x in data if not x[3]]
    hlons = [x[1] for x in data if not x[3]]

    vx, vy = m(vlons, vlats)
    hx, hy = m(hlons, hlats)

    m.plot(vx, vy, marker='o', linestyle='None', markersize=0.5,  color='y')
    m.plot(hx, hy, marker='o', linestyle='None', markersize=0.5,  color='k')
    plt.title('Ground Tracks')
    plt.show()


def plotDifferences(data):
    """Plots the differences between two orbits
    
    Args:
        data:Array: A list of tuples contianing time then differences
        in 3 directions
        
    Returns:
        None
    """
    plt.scatter([x[0] for x in data], [x[1] for x in data], marker='.', color='k', s=1)
    plt.scatter([x[0] for x in data], [x[2] for x in data], marker='.', color='b', s=1)
    plt.scatter([x[0] for x in data], [x[3] for x in data], marker='.', color='r', s=1)

    plt.title('Differences')
    plt.show()


def plotPassData(data):
    """Plots data about the total pass time for stations on a
    projection of Earth.
    
    Args:
        data: Array: A list of tuples containing lat lon and pass time.
        
    Returns:
        None.
    """
    m = initMap()

    times = [x[2] for x in data]
    x = [i[0] for i in data]
    y = [i[1] for i in data]

    lat, lon = m(x, y)

    m.scatter(lon, lat, marker='o', c=times, zorder=10, cmap='hot')
    plt.colorbar()

    plt.show()
