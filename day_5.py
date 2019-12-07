from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=5)
inputs = aoc.ints(puzzle.input_data)


# PART 1

emulator = aoc.IntcodeEmulator()
outputs = emulator.run(inputs, inputs=iter([1]))
failed_tests = set(outputs) - {0, None}
puzzle.answer_a = list(failed_tests)[0]


# PART 2

emulator = aoc.IntcodeEmulator()
outputs = emulator.run(inputs, inputs=iter([5]))
failed_tests = set(outputs) - {0, None}
puzzle.answer_b = list(failed_tests)[0]
