import asyncio
from copy import copy
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


row = 0
col = 0
walkway = set()
for pixel in pixels:
    if pixel in ("#", ">", "<", "v", "^"):
        walkway.add((row, col))

    if pixel == "\n":
        row += 1
        col = 0
    else:
        col += 1


puzzle.answer_a = sum(
    map(alignment_parameter, set(filter(partial(is_intersection, w=walkway), walkway)))
)


# PART 2

async def run_roomba(m, a, b, c):
    program = copy(inputs)
    program[0] = 2
    roomba = aoc.IntcodeEmulator(program=program, inputs=asyncio.Queue())

    def trans(seq):
        assert len(seq) <= 20
        return ",".join(seq) + "\n"

    commands = trans(m) + trans(a) + trans(b) + trans(c) + "n\n"
    for command in commands:
        roomba.inputs.put_nowait(ord(command))

    await roomba.run()

    outputs = []
    while not roomba.outputs.empty():
        outputs.append(roomba.outputs.get_nowait())

    print("".join([str(chr(p)) for p in outputs[:-1]]))

    return outputs[-1]


# This was easiest solved by hand so far, with the assumption that the robot always
# drives until it encounters a corner.
path = [
    "L,6", "R,12", "L,4", "L,6",
    "R,6", "L,6", "R,12",
    "R,6", "L,6", "R,12",
    "L,6", "L,10", "L,10", "R,6",
    "L,6", "R,12", "L,4", "L,6",
    "R,6", "L,6", "R,12",
    "L,6", "L,10", "L,10", "R,6",
    "L,6", "R,12", "L,4", "L,6",
    "R,6", "L,6", "R,12",
    "L,6", "L,10", "L,10", "R,6",
]

macro_a = ["L,6", "R,12", "L,4", "L,6"]
macro_b = ["R,6", "L,6", "R,12"]
macro_c = ["L,6", "L,10", "L,10", "R,6"]
main = ["A", "B", "B", "C", "A", "B", "C", "A", "B", "C"]

puzzle.answer_b = asyncio.run(run_roomba(main, macro_a, macro_b, macro_c))
