import asyncio
from functools import partial

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=17)
inputs = aoc.ints(puzzle.input_data)


# PART 1

async def view():
    sensor = aoc.IntcodeEmulator(program=inputs)

    await sensor.run()

    image = []
    while not sensor.outputs.empty():
        image.append(str(chr(sensor.outputs.get_nowait())))

    return image


def is_intersection(p, w) -> bool:
    adj = {
        (p[0] - 1, p[1]),
        (p[0] + 1, p[1]),
        (p[0], p[1] - 1),
        (p[0], p[1] + 1),
    }
    return adj.issubset(w)


def alignment_parameter(p):
    return p[0] * p[1]


pixels = asyncio.run(view())
print("".join(pixels))


r = 0
c = 0
walkway = set()
for pixel in pixels:
    if pixel in ("#", ">", "<", "v", "^"):
        walkway.add((r, c))

    if pixel == "\n":
        r += 1
        c = 0
    else:
        c += 1


puzzle.answer_a = sum(
    map(alignment_parameter, set(filter(partial(is_intersection, w=walkway), walkway)))
)
