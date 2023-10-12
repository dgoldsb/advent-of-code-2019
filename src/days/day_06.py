from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.common_functions import path_to_root

puzzle = Puzzle(year=2019, day=6)
inputs = puzzle.input_data
orbits = {x.split(")")[1]: x.split(")")[0] for x in inputs.splitlines()}


# PART 1

checksum = 0
for key in orbits.keys():
    lst = path_to_root(orbits, key)

    checksum += len(lst) - 1

puzzle.answer_a = checksum


# PART 2

lst_you = path_to_root(orbits, "YOU")
lst_san = path_to_root(orbits, "SAN")

first_match = None
for key in lst_you:
    if key in lst_san:
        first_match = key
        break

puzzle.answer_b = lst_you.index(first_match) + lst_san.index(first_match) - 2
