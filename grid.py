import random
import statistics
from typing import List

DIRECTIONS = [-10, 10, -1, 1]
START = 50
MAX = 10


def enough_neighbours(cell: int, rooms: List[int]) -> bool:
    """Checks whether the neighbour already has more than one neighbour attached.
    
    Parameters:
        cell (int): The cell to check the neighbours of
        rooms (List): The list of current rooms in the level
    Returns:
        enough_neighbours (bool): Whether there are enough neighbours
    """
    count = 0
    for d in DIRECTIONS:
        if cell + d in rooms:
            count += 1
    if count > 1:
        return True
    return False


def levelgen() -> List[int]:
    """Generates a list of rooms for the level based on the description found
    here: https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/

    Returns:
        rooms (List): A list of rooms for the level
    """
    current = START
    rooms = [current]
    while len(rooms) < MAX:
        for room in rooms:
            if len(rooms) > MAX:
                print("FINISHED")
                print("----------------")
                break
            print("----------------")
            print(f"WORKING ON ROOM: {room}")
            for d in DIRECTIONS:
                if len(rooms) > MAX:
                    print("ENOUGH ROOMS")
                    break
                neighbour = room + d
                print(f"CALCULATING NEIGHBOUR: {neighbour}")
                if neighbour in rooms:
                    print("NEIGHBOUR IN ROOM")
                    continue
                if enough_neighbours(neighbour, rooms):
                    print("ENOUGH NEIGHBOURS")
                    continue
                if random.choice([0,1]) == 0:
                    print("RANDOM CHANCE")
                    continue
                else:
                    print(f"ADDING NEIGHBOUR: {neighbour}")
                    rooms.append(neighbour)
    return rooms


def calc_route_to_boss(rooms: List[int]) -> List[int]:
    """Calculates the route from the boss room to the start room.

    Parameters:
        rooms (List): The list of rooms from the levelgen function
    Returns:
        route (List): The route from boss room to start room
    """
    rooms.reverse()
    print(rooms)
    ds = DIRECTIONS.copy()
    solved = False
    i = 0
    while not solved:
        random.shuffle(ds)
        route = [rooms[0]]
        for room in route:
            for d in ds:
                if room + d in rooms and room + d not in route:
                    route.append(room + d)
                    if route[-1] == rooms[-1]:
                        return route
                    else:
                        break
        i += 1
        if i % 100 == 0:
            break


def run_mcs() -> float:
    """Runs a Monte Carlo Simulation to calculate the average
    number of rooms the player must pass through on the shortest
    trip to the boss
    """
    res = []
    for _ in range(10000):
        rooms = levelgen()
        route = calc_route_to_boss(rooms)
        if route:
            res.append(len(route))
    return statistics.mean(res)


print(f"AVERAGE NUMBER OF ROOMS TO BOSS: {run_mcs()}")