from satelliteSimulator.keplerianPropogation import propogateOrbit
from satelliteSimulator.data import *
from satelliteSimulator.utils import readData

propogateOrbit(jason['R'], jason['V'], 10, 8600)
data = readData('./data/kepProp.csv')
print(data[0])
