from typing import List
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from grid_coords import levelgen, calc_route_to_boss, calc_coords_to_boss


def plotlevel(roomcs: List, routecs: List) -> None:
    """Displays the level generated by the algorithm complete with the optimal path.
    
    Parameters:
        roomcs (List): The coodinates of the rooms to plot
        routecs (List): The coordinates of the route to plot
    """
    _, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(0,15)
    ax.set_ylim(0,15)
    for i, coords in enumerate(roomcs):
        if i == 0:
            color = "green"
            label = "Starting Room"
        elif i == len(roomcs) - 1:
            color = "red"
            label = "Boss Room"
        else:
            color = "white"
            label = "Normal Room"
        ax.add_patch(Rectangle(
            (coords[0], coords[1]),
            1, 1,
            color=color,
            ec="black",
            label=label,
        ))
    routexs = [coords[0] + 0.5 for coords in routecs]
    routeys = [coords[1] + 0.5 for coords in routecs]
    ax.plot(routexs, routeys, linestyle="-", color="black", label="Route")
    handles, labels = ax.get_legend_handles_labels()
    cleaned = dict(zip(labels, handles))
    ax.legend(cleaned.values(), cleaned.keys())
    plt.show()


if __name__ == "__main__":
    rooms, roomcs = levelgen()
    route = calc_route_to_boss(rooms)
    rooms.reverse()
    route.reverse()
    routecs = calc_coords_to_boss(rooms, route, roomcs)
    plotlevel(roomcs, routecs)