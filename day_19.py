import asyncio
from functools import lru_cache

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=19)
inputs = aoc.ints(puzzle.input_data)


async def _run(x, y):
    assert x >= 0
    assert y >= 0

    emulator = aoc.IntcodeEmulator(inputs, asyncio.Queue())
    emulator.inputs.put_nowait(x)
    emulator.inputs.put_nowait(y)

    await emulator.run()

    return emulator.outputs.get_nowait()


@lru_cache(10 ** 4)
def in_tractor_beam(x, y):
    return asyncio.run(_run(x, y))


# PART 1
#puzzle.answer_a = sum([in_tractor_beam(x, y) for x in range(50) for y in range(50)])


# PART 2
def valid_10_by_10(x, y):
    return (
        bool(in_tractor_beam(x, y)) and
        bool(in_tractor_beam(x + 9, y)) and
        bool(in_tractor_beam(x, y + 9)) and
        bool(in_tractor_beam(x + 9, y + 9))
    )


def part_2():
    for x in range(110):
        for y in range(110):
            if valid_10_by_10(x, y):
                return x, y


part_2 = part_2()
puzzle.answer_b = part_2[0] * 10 ** 4 + part_2[1]


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

for x_ in range(10):
    for y_ in range(10):
        if image[part_2[0] + x_][part_2[1] + y_] != "#":
            raise RuntimeError
        image[part_2[0] + x_][part_2[1] + y_] = "0"


print("\n".join(["".join(row) for row in image]))
