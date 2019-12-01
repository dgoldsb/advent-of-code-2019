from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=1)
inputs = puzzle.input_data.splitlines()


# PART 1

puzzle.answer_a = sum([(int(x) // 3) - 2 for x in inputs])


# PART 2

def find_fuel(weight: int):
    if weight < 9:
        return 0
    else:
        fuel = (weight // 3) - 2

        return fuel + find_fuel(fuel)


puzzle.answer_b = sum([find_fuel(int(x)) for x in inputs])
