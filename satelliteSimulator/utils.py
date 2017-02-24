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
from distutils.util import strtobool


def normaliseAngle(angle):
    """Normalises an angle to between 0 and 2 pi

    Args:
        angle (float): Angle in radians

    Returns:
        float. An angle in radians between 0 and 2 * math.pi

    """
    return angle % (2*math.pi)


def normalisedAtan2(numerator, denominator):
    """Atan2 but value is between 0 and 2 pi

    Args:
        numerator (float): value for the numerator of atan2

        denominator (float): value for the denominator of atan2

    Returns:
        float. Normalised result of atan2
    """
    result = math.atan2(numerator, denominator)
    if result < 0:
        result += 2 * math.pi
    return result


def writeData(data, csvfile):
    """Writes data to a file as CSV
    
    Args:
        data: Array: The data to be written.
        
        csvfile: File handle.
        
    Returns:
        None
    """
    writer = csv.writer(csvfile)
    for row in data:
        writer.writerow(flattenTuple(row))


def flattenTuple(tpl):
    """Flattens out any sub arrays or tuples in a tuple
    for writing to csv.
    
    Args:
        tpl: Tuple.
    
    Returns:
        Array: The flattened tuple.
    """
    res = []
    for xs in tpl:
        try:
            for x in xs:
                res.append(x)
        except TypeError:
            res.append(xs)
    return res


def readData(csvfile):
    """Reads data from a csv file and parses all data as floats
    
    Args:
        csvfile: File handle
        
    Returns:
        Array: List of parsed lines
    """
    result = []
    reader = csv.reader(csvfile)
    for row in reader:
        parsedData = []
        for item in row:
            parsedData.append(float(item))
        result.append(parsedData)
    return result


def readECIData(csvfile):
    """Parses ECI data from a CVS file
    
    Args:
        csvfile: File handle
        
    Returns:
        Array: List containing position vector, velocity vector 
        and time.
    """
    result = []
    reader = csv.reader(csvfile)
    for row in reader:
        R = [float(row[0]), float(row[1]), float(row[2])]
        V = [float(row[3]), float(row[4]), float(row[5])]
        time = float(row[6])
        result.append((R, V, time))
    return result


def readGrndTrckData(csvfile):
    """Parses ground track data from a csv file.
    
    Args:
        csvfile: File handle.
        
    Returns:
        Array: List of lat lon height and if its visible 
        from a tracking station.
    """
    results = []
    reader = csv.reader(csvfile)
    for row in reader:
        results.append((float(row[0]), float(row[1]), float(row[2]), strtobool(row[3])))
    return results
