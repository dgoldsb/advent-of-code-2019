from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=20)
inputs = puzzle.input_data

UPPERS = [chr(c) for c in range(65, 91)]

# Get the maze.
maze = aoc.char_array(inputs)


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


def get_portals(m):
    global stage
    for x in range(1, len(maze) - 1):
        for y in range(1, len(maze[x]) - 1):
            try:
                name, loc = parse_portal(x, y, m)
                if name:
                    try:
                        yield aoc.Portal(name, stage[name], loc)
                    except KeyError:
                        stage[name] = loc
            except AssertionError:
                pass


portals = list(get_portals(maze))
distance = aoc.a_star_distance(maze, stage["AA"], stage["ZZ"], ".", portals)
puzzle.answer_a = distance
