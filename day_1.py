from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=1)
inputs = puzzle.input_data.splitlines()


# PART 1

def find_fuel(weight: int):
    return (weight // 3) - 2


puzzle.answer_a = sum([find_fuel(int(x)) for x in inputs])


# PART 2

def find_recursive_fuel(weight: int):
    if weight < 9:
        return 0
    else:
        fuel = find_fuel(weight)

        return fuel + find_recursive_fuel(fuel)


puzzle.answer_b = sum([find_recursive_fuel(int(x)) for x in inputs])
