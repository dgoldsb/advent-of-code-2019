import asyncio
from copy import copy

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=2)
inputs = aoc.ints(puzzle.input_data)


async def do_part(noun, verb):
    program = copy(inputs)
    program[1] = noun
    program[2] = verb
    emulator = aoc.IntcodeEmulator(program)
    await emulator.run()
    return emulator.state[0]


# PART 1

puzzle.answer_a = asyncio.run(do_part(12, 2))


# PART 2

for noun in range(0, 100):
    for verb in range(0, 100):
        result = asyncio.run(do_part(noun, verb))
        if result == 19690720:
            puzzle.answer_b = 100 * noun + verb
