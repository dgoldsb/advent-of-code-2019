import asyncio

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=9)
inputs = ints(puzzle.input_data)
# TODO: Fix this


async def do_part(inp):
    queue = asyncio.Queue()
    queue.put_nowait(inp)
    emulator = IntcodeEmulator(program=inputs, inputs=queue)
    await emulator.run()

    return emulator.outputs.get_nowait()


# PART 1

puzzle.answer_a = asyncio.run(do_part(1))


# PART 2

puzzle.answer_b = asyncio.run(do_part(2))
