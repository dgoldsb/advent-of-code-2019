import asyncio
from copy import copy

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=2)
inputs = ints(puzzle.input_data)


async def run_intcode_program(noun, verb):
    program = copy(inputs)
    program[1] = noun
    program[2] = verb
    emulator = IntcodeEmulator(program)
    await emulator.run()
    return emulator.state[0]


# PART 1
puzzle.answer_a = asyncio.run(run_intcode_program(12, 2))


# PART 2

for noun in range(0, 100):
    for verb in range(0, 100):
        result = asyncio.run(run_intcode_program(noun, verb))
        if result == 19690720:
            puzzle.answer_b = 100 * noun + verb
