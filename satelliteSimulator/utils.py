#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: utils
    :platform: Unix
    :synopsis: A collection of helper functions

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

import math
import csv

def normaliseAngle(angle):
    """Normalises an angle to between 0 and 2 pi

    Args: 
        angle (float): Angle in radians

    Returns:
        float. An angle in radians between 0 and 2 * math.pi

    """
    return angle % (2*math.pi)

def normailisedAtan2(numerator, denominator):
    """Atan2 but value is between 0 and 2 pi
    
    Args:
        numerator (float): value for the numerator of atan2

        denominator (float): value for the denominator of atan2

    Returns:
        float. Normalised result of atan2
    """
    result = math.atan2(numerator,denominator)
    if result < 0:
        result += 2 * math.pi
    return result

def writeData(data, fileName):
    with open(fileName, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def readData(fileName):
    result = []
    with open(fileName, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            parsedData = []
            for item in row:
                parsedData.append(float(item))
            result.append(parsedData)
    return result
