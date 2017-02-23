#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: main
    :platform: Unix
    :synopsis: Main file to run the simulator from

.. moduleauthor:: Henry Mortimer <henry@morti.net>

"""

from satelliteSimulator.propogation.rk4 import rk4MonoPropogation,\
                                                rk4j2Propogation
from satelliteSimulator.propogation.keplerianPropogation import propogateOrbit
from satelliteSimulator.data import Jason, GPSIIR, Galileo
from satelliteSimulator.utils import writeData, readECIData, readGrndTrckData
from satelliteSimulator.analysis.groundTracks import getGroundTracks
from satelliteSimulator.plot import plotGroundTracks
from satelliteSimulator.converters.eci2ecef import ECI2ECEF
from satelliteSimulator.analysis.visibility import isVisible
from satelliteSimulator.analysis.differences import HCLDiff, ENUDiff
import argparse
import matplotlib.pyplot as plt
import sys
from itertools import zip_longest, islice




def getArgs():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    prop = subparsers.add_parser('propogate')
    prop.add_argument('satellite', type=str, choices=['Jason', 'GPSIIR', 'Galileo'])
    prop.add_argument('algorithm', type=str, choices=['kep', 'rk4', 'j2'])
    prop.add_argument('days', type=float, default=1)
    prop.add_argument('-o','--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    diff = subparsers.add_parser('difference')
    diffAlg = diff.add_mutually_exclusive_group(required=True)
    diffAlg.add_argument('--hcl', action='store_true')
    diffAlg.add_argument('--enu', nargs=2, metavar=('lat', 'lon'))
    diff.add_argument('-i1', '--infile1', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    diff.add_argument('-i2', '--infile2', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    diff.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    grndTrck = subparsers.add_parser('groundTrack')
    grndTrck.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    grndTrck.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    grndTrck.add_argument('stations', nargs="+", type=float, metavar='lat lon angle')

    plot = subparsers.add_parser('plot')
    plot.add_argument('-i', '--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_usage()
        sys.exit(-1)
    else:
        return args


def propogate(args):
    if args.satellite == 'Jason':
        sat = Jason
    elif args.satellite == 'GPSIIR':
        sat = GPSIIR
    else:
        sat = Galileo

    if args.algorithm == 'kep':
        alg = propogateOrbit
    elif args.algorithm == 'rk4':
        alg = rk4MonoPropogation
    else:
        alg = rk4j2Propogation

    data = alg(sat['R'], sat['V'], 10, int(8640*args.days), sat['time'])

    writeData(data, args.outfile)


def difference(args):
    set1 = readECIData(args.infile1)
    set2 = readECIData(args.infile2)

    diffs = []

    if args.hcl:
        for r, k in zip(set1, set2):
            diff = HCLDiff((r[0], r[1]), (k[0], k[1]))
            diffs.append([r[2]] + diff)
    else:
        for r, k in zip(set1, set2):
            diff = ENUDiff((r[0], r[1]), (k[0], k[1]), args.enu, r[2])
            diffs.append([r[2]] + diff)

    writeData(diffs, args.outfile)


def triples(lst):
    for x12 in zip_longest(islice(lst, 0, None, 3), islice(lst, 1, None, 3), islice(lst, 2, None, 3)):
        yield x12


def groundTracks(args):
    data = readECIData(args.infile)
    ecefData = []

    for step in data:
        ecefData.append(ECI2ECEF(step[0], step[1], step[2]))

    stations = list(triples(args.stations))
    groundTracks = getGroundTracks([x[0] for x in ecefData], stations)

    writeData(groundTracks, args.outfile)


def plot(args):
    data = readGrndTrckData(args.infile)
    plotGroundTracks(data)
    plt.show()


def main():
    # rk4 = rk4MonoPropogation(Galileo['R'], Galileo['V'], 10, 8640*100, Galileo['time'])
    # rk4j2 = rk4j2Propogation(Galileo['R'], Galileo['V'], 10, 8640*100, Galileo['time'])
    # kep = propogateOrbit(Galileo['R'], Galileo['V'], 10, 8640*100, Galileo['time'])
    # diffs1 = []
    # diffs2 = []
    # for r, k in zip(rk4, rk4j2):
    #     diffs1.append((r[2],)+HCLDiff((r[0], r[1]), (k[0], k[1])))
    # for r, k in zip(rk4, rk4j2):
    #     diffs2.append((r[2],)+ENUDiff((r[0], r[1]), (k[0], k[1]), (51, -0.5), r[2]))

    # plt.scatter([x[0] for x in diffs2], [x[1] for x in diffs2], marker='.', color='k', s=1)
    # plt.scatter([x[0] for x in diffs2], [x[2] for x in diffs2], marker='.', color='b', s=1)
    # plt.scatter([x[0] for x in diffs2], [x[3] for x in diffs2], marker='.', color='r', s=1)

    # plt.show()

    # m = initMap()
    # ecefData = []
    # for step in rk4j2:
    #     ecefData.append(ECI2ECEF(step[0], step[1], step[2]))

    # groundTracks = getGroundTracks([x[0] for x in ecefData if isVisible(x[0], 51.32, -0.5, 5)])
    # plotGroundTracks(groundTracks, 'y', m)
    # groundTracks = getGroundTracks([x[0] for x in ecefData if not isVisible(x[0], 51.32, -0.5, 5)])
    # plotGroundTracks(groundTracks, 'k', m)
    # plt.title("Ground Tracks")
    # plt.show()

    args = getArgs()
    if args.cmd == 'propogate':
        propogate(args)
    elif args.cmd == 'difference':
        difference(args)
    elif args.cmd == 'groundTrack':
        groundTracks(args)
    elif args.cmd == 'plot':
        plot(args)


if __name__ == '__main__':
    main()
