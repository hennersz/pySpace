#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: plot
    :platform: Unix
    :synopsis: Plots graphs of satellite motion

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def plotECI(data):

    x = [row[0] for row in data]
    y = [row[1] for row in data]
    z = [row[2] for row in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, c='r', marker='o')

    plt.show()
