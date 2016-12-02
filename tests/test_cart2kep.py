from context import satelliteSimulator #gets all of my local packages
from satelliteSimulator import cart2kep
import pytest



def test_normalisedAtan2():
    assert cart2kep.normailisedAtan2(1,1) == 0.7853981633974483
    assert cart2kep.normailisedAtan2(1,-1) == 2.356194490192345
    assert cart2kep.normailisedAtan2(-1, 1) == 5.497787143782138
    assert cart2kep.normailisedAtan2(-1, -1) == 3.9269908169872414


