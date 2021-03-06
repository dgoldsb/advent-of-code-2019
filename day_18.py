from collections import defaultdict
from functools import lru_cache

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=18)
inputs = puzzle.input_data

# Get the maze.
maze = aoc.char_array(inputs)

# Find the relevant locations.
valid_keys = [chr(x) for x in range(ord("a"), ord("z") + 1) if chr(x) in inputs]
DOOR_LOCATIONS = {k.upper(): aoc.find_in_maze(k.upper(), maze) for k in valid_keys}
DOOR_LOCATIONS_INVERSE = {v: k for k, v in DOOR_LOCATIONS.items()}
KEY_LOCATIONS = {k: aoc.find_in_maze(k, maze) for k in valid_keys}
start_location = aoc.find_in_maze("@", maze)

# Make the keys and the starting location walkable.
for loc in list(KEY_LOCATIONS.values()) + list(DOOR_LOCATIONS.values()) + [start_location]:
    if loc is not None:
        maze[loc[0]][loc[1]] = "."

MAZE = maze

# Cache all path lengths.
@lru_cache(len(valid_keys) ** 2)
def find_path_length(lc, tg):
    return aoc.a_star_distance(MAZE, lc, tg, ".")


# Cache all the keys needed to unlock each target.
BLOCKERS = defaultdict(lambda: set())

for key in valid_keys:
    path = aoc.a_star_route(MAZE, start_location, KEY_LOCATIONS[key], ".")
    for loc in path:
        try:
            BLOCKERS[key].add(DOOR_LOCATIONS_INVERSE[loc].lower())
        except KeyError:
            pass


# Use the cached results to do part 1.
# TODO: We are repeating generic base cases a lot, dynamic programming?
@lru_cache(10 ** 6)
def part_1(start, missing):
    if len(missing) == 1:
        key = list(missing)[0]
        return [(find_path_length(start, KEY_LOCATIONS[key]), key)]
    else:
        paths = []
        for key in missing:
            obtained = set(valid_keys) - set(missing)
            if BLOCKERS[key].difference(obtained):
                continue

            path_part = [(find_path_length(start, KEY_LOCATIONS[key]), key)]

            new_missing = list(missing)
            new_missing.remove(key)
            path_rest = part_1(KEY_LOCATIONS[key], tuple(new_missing))

            if path_rest is None:
                continue

            paths.append(path_part + path_rest)

        shortest_path = None
        shortest_length = 10 ** 4
        for pt in paths:
            try:
                if sum([x[0] for x in path]) < shortest_length:
                    shortest_path = pt
                    shortest_length = sum([x[0] for x in pt])
            except TypeError:
                pass

        return shortest_path


print(BLOCKERS)
answer = part_1(start_location, tuple(valid_keys))
print(answer)
print(sum([x[0] for x in answer]))
