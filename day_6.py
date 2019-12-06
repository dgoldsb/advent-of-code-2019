from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=6)
inputs = puzzle.input_data
orbits = {x.split(")")[1]: x.split(")")[0] for x in inputs.splitlines()}


def find_orbits(orbs, a):
    if a in orbs.keys():
        return [orbs[a]] + find_orbits(orbs, orbs[a])
    else:
        return []


# PART 1

checksum = 0
for key in orbits.keys():
    lst = [key] + find_orbits(orbits, key)

    checksum += len(lst) - 1

puzzle.answer_a = checksum


# PART 2

lst_you = find_orbits(orbits, "YOU")
lst_san = find_orbits(orbits, "SAN")

first_match = None
for key in lst_you:
    if key in lst_san:
        first_match = key
        break

puzzle.answer_b = lst_you.index(first_match) + lst_san.index(first_match)
