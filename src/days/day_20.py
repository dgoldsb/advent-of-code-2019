import typing

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.io import char_array
from src.module.pathfinding import Node, Portal, a_star_distance

puzzle = Puzzle(year=2019, day=20)
inputs = puzzle.input_data
inputs = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
                                              """

UPPERS = [chr(c) for c in range(65, 91)]

# Get the maze.
maze = char_array(inputs)


def is_outer(loc, m):
    return loc[0] < 4 or loc[1] < 4 or loc[0] > (len(m) - 4) or loc[1] > (len(m[0]) - 4)


def parse_portal(x, y, m):
    assert m[x][y] in UPPERS

    triple = [None, m[x][y], None]
    for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        up = m[x + delta[0]][y + delta[1]]
        down = m[x - delta[0]][y - delta[1]]

        if up in UPPERS and down == ".":
            triple[0] = up
            triple[2] = (x - delta[0], y - delta[1])
            name_list = sorted(triple[0:2])
            return "".join(name_list), triple[2]
    else:
        return None, None


stage = {}


def get_portals(m, recursive=False):
    global stage
    for x in range(1, len(maze) - 1):
        for y in range(1, len(maze[x]) - 1):
            try:
                name, loc = parse_portal(x, y, m)
                if name:
                    try:
                        if is_outer(loc, m):
                            yield Portal(name, stage[name], loc, recursive)
                        else:
                            yield Portal(name, loc, stage[name], recursive)

                    except KeyError:
                        stage[name] = loc
            except AssertionError:
                pass


# PART 1

portals = list(get_portals(maze))
distance = a_star_distance(maze, stage["AA"], stage["ZZ"], ".", portals)
print(f"Answer a is {distance}")
# puzzle.answer_a = distance

# PART 2

portals = list(get_portals(maze, recursive=True))
distance = a_star_distance(
    maze,
    (stage["AA"][0], stage["AA"][1], 0),
    (stage["ZZ"][0], stage["ZZ"][1], 0),
    ".",
    portals,
)
# puzzle.answer_b = distance
print(f"Answer b is {distance}")
