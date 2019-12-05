from copy import copy

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=2)
inputs = aoc.ints(puzzle.input_data)


# PART 1

program = copy(inputs)
program[1] = 12
program[2] = 2
emulator = aoc.IntcodeEmulator()
emulator.run(program)
puzzle.answer_a = emulator.state[0]


# PART 2

for noun in range(0, 100):
    for verb in range(0, 100):
        program = copy(inputs)
        program[1] = noun
        program[2] = verb
        emulator = aoc.IntcodeEmulator()
        emulator.run(program)
        if emulator.state[0] == 19690720:
            puzzle.answer_b = 100 * noun + verb
