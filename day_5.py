import asyncio

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=5)
inputs = aoc.ints(puzzle.input_data)


async def do_part(i: int):
    queue = asyncio.Queue()
    queue.put_nowait(i)
    emulator = aoc.IntcodeEmulator(program=inputs, inputs=queue)
    await emulator.run()

    while True:
        result = emulator.outputs.get_nowait()
        if result != 0:
            return result


# PART 1

puzzle.answer_a = asyncio.run(do_part(1))


# PART 2

puzzle.answer_b = asyncio.run(do_part(5))
