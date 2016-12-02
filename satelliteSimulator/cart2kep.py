from .data import jason
import numpy as np
import math

def cart2kep(R, V):
   h̅ = np.cross(R,V)

def normailisedAtan2(y,x):
    result = math.atan2(y,x)
    if result < 0:
        result += 2 * math.pi
    return result


