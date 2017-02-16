#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: plot
    :platform: Unix
    :synopsis: Plots graphs of satellite motion

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def plotECI(data):

    x = [row[0] for row in data]
    y = [row[1] for row in data]
    z = [row[2] for row in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, c='r', marker='o')

    plt.show()

def plotGroundTracks(data):
    lats = [x[1] for x in data]
    lons = [x[2] for x in data] 
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
		llcrnrlon=-180,urcrnrlon=180)
    x,y = m(lons, lats)
    m.plot(x,y,marker='o',linestyle='None', markersize=0.5,  color='k')
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')

    # draw parallels and meridians.
    m.drawparallels(np.arange(-90.,91.,30.))
    m.drawmeridians(np.arange(-180.,181.,60.))
    m.drawmapboundary(fill_color='aqua')
    plt.title("Ground Tracks")
    plt.show()
