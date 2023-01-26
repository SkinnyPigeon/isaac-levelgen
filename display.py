from typing import List
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


from grid_coords import levelgen, calc_route_to_boss, calc_coords_to_boss

rooms, roomcs = levelgen()
route = calc_route_to_boss(rooms)
rooms.reverse()
route.reverse()


routecs = calc_coords_to_boss(rooms, route, roomcs)
print(rooms)
print(route)
print(roomcs)
print(routecs)


def plotlevel(roomcs: List, routecs: List):
    pass
