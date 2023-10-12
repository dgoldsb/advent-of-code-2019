import asyncio
from functools import lru_cache

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=19)
inputs = ints(puzzle.input_data)


async def _run(x, y):
    assert x >= 0
    assert y >= 0

    emulator = IntcodeEmulator(inputs, asyncio.Queue())
    emulator.inputs.put_nowait(x)
    emulator.inputs.put_nowait(y)

    await emulator.run()

    return emulator.outputs.get_nowait()


@lru_cache(10**4)
def in_tractor_beam(x, y):
    return asyncio.run(_run(x, y))


# PART 1
puzzle.answer_a = sum([in_tractor_beam(x, y) for x in range(50) for y in range(50)])


# FUN INTERMEZZO
image = []
for x_ in range(120):
    row = []

    for y_ in range(120):
        if in_tractor_beam(x_, y_) == 1:
            row.append("#")
        else:
            row.append(".")
    image.append(row)

print("\n".join(["".join(row) for row in image]))


# PART 2
def valid_square(x, y, size):
    return (
        bool(in_tractor_beam(x, y))
        and bool(in_tractor_beam(x + size - 1, y))
        and bool(in_tractor_beam(x, y + size - 1))
    )


def part_2():
    fv = 0
    for x in range(1000):
        found_first = False
        for y in range(fv, 1000):
            if bool(in_tractor_beam(x, y)):
                if not found_first:
                    fv = y
                    found_first = True

                if valid_square(x, y, 100):
                    return x, y
            else:
                if found_first:
                    print(f"Width of {y - fv} at x={x}")
                    break


part_2 = part_2()
puzzle.answer_b = part_2[0] * 10**4 + part_2[1]
