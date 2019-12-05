from copy import copy

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=5)
inputs = aoc.ints(puzzle.input_data)


# PART 1

program = copy(inputs)
_, output = aoc.run_intcode_program(program, 1)
failed_tests = set(output) - {0, None}
puzzle.answer_a = list(failed_tests)[0]


# PART 2

program = copy(inputs)
_, output = aoc.run_intcode_program(program, 5)
failed_tests = set(output) - {0, None}
puzzle.answer_b = list(failed_tests)[0]
