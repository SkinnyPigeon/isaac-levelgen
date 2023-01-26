import random
import math
from typing import Dict, List
from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response


conn = Neo4jConnection(uri="neo4j://localhost:7687", 
                       user="neo4j",              
                       pwd="password")


def room_count(floor: int, xl: bool, curse: bool, void: bool = False) -> int:
    """
    If the floor is not XL or Added in Afterbirth † The Void:
        NumberOfRooms = 3.33 × FloorDepth + 5-6 (maximum of 20)
    If the floor is an XL floor:
        NumberOfRooms = 1.8 × (3.33 × FloorDepth + 5-6) (maximum of 45)
    If the floor is The Void:
        NumberOfRooms = 50-59
    2-3 more rooms are added if playing on Hard Mode
    4 more rooms are added if the floor has Curse of the Lost.

    Parameters:
        floor (int): The floor number to generate the room count for
        xl (bool): Is there Curse of the Labarynth
        curse (bool): Is there Curse of the lost
        void (bool): Is it the void
    Returns:
        rooms (int): The number of rooms for that floor
    """
    rooms = 3.33 * floor + random.randint(5, 6) + random.randint(2, 3)
    if not xl:
        if rooms >= 20:
            rooms = 20
        if not curse:
            return math.floor(rooms)
        return math.floor(rooms) + 4
    if xl:
        rooms = rooms * 1.8
        if rooms >= 45:
            return 45
        return math.floor(rooms)
    if void:
        return random.randint(50, 59)


def dead_ends(floor: int, xl: bool, void: bool, voodoo: bool = False):
    """
    All floors have at least 5 dead ends
    1 dead end is added to all floors except the first floor.
    1 dead end is added to XL floors.
    2 dead ends are added to The Void.
    1 dead end is added if the player has Voodoo Head

    Parameters:
        floor (int): The floor number to generate the dead ends count for
        xl (bool): Is there Curse of the Labarynth
        void (bool): Is it the void
        voodoo (bool): Does the player have Voodoo Head
    Returns:
        ends (int): The number of dead ends for that floor

    """
    ends = 5
    if floor == 1:
        return ends
    ends += 1 
    if voodoo:
        ends += 1
    if xl:
        return ends + 1
    if void:
        return ends + 2
    return ends


def reset() -> None:
    """Resets the graph"""
    relationships = "MATCH (a)-[b]->(c) DELETE b"
    rooms = "MATCH (n) DELETE n"
    conn.query(relationships)
    conn.query(rooms)


FLOOR = 1
XL = False
CURSE = False
VOID = False

rooms = room_count(FLOOR, XL, CURSE, VOID)
ends = dead_ends(FLOOR, XL, VOID)


reset()

print(rooms)
print(ends)

layout = {room + 1: {"type": "standard"} for room in range(rooms)}


def construct_rooms(rooms: int) -> None:
    for room in range(rooms):
        conn.query(f"CREATE (r:room {{id: {room + 1}, type: 'standard'}})")


def reassign_rooms(rooms: int, special_rooms: List) -> List:
    choices = [i + 1 for i in range(rooms)]
    rooms_to_change = random.sample(choices, k=len(special_rooms))
    for room, index in zip(special_rooms, rooms_to_change):
        query = f"MATCH (r:room {{id: {index}}}) REMOVE r:room SET r:{room}, r.type = '{room}'"
        layout[index]["type"] = room
        conn.query(query)
    return rooms_to_change



def special_rooms(dead_ends: int) -> List:
    special_rooms = ["boss", "shop", "item"]
    for _ in range(dead_ends - len(special_rooms)):
        special_rooms.append("dead_end")
    return special_rooms


special_room_list = special_rooms(ends)


construct_rooms(rooms)
changed_rooms = reassign_rooms(rooms, special_room_list)
print(layout)


print(changed_rooms)

def pick_direction() -> str:
    return random.sample(["north", "south", "east", "west"], k=1)[0]


def opposite_direction(direction: str) -> str:
    if direction == "north":
        return "south"
    elif direction == "south":
        return "north"
    elif direction == "east":
        return "west"
    elif direction == "west":
        return "east"


def get_standard_rooms(layout: Dict) -> List:
    return [room for room in layout.keys() if layout[room]["type"] == "standard"]


print(get_standard_rooms(layout))

def join_rooms(layout: Dict) -> None:
    standard_rooms = get_standard_rooms(layout)
    first_room = 0
    last_direction = None
    for i, room in enumerate(standard_rooms):
        direction = pick_direction()
        if i == 0:
            first_room = room
        print(direction)
        print(i)
        print(room)


# GIVE THEM COORDS TO SEE IF THEY HAVE CONNECITONS. I.E. AS A LOOP IS FORMING N-W-S-E, THE N&E SHOULD END UP HAVING COORDS
            

join_rooms(layout)
# conn.query("CREATE (r:room)")
# conn.query("CREATE (r:room)-[j:join]->(s:shop)")

# reset()