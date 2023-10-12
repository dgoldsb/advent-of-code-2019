import asyncio
import typing

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=21)


class SpringDroid:
    def __init__(self, spring_script: typing.List[typing.Tuple[str, str, str]]):
        self.spring_script = spring_script

    async def run(self, walk=True):
        intcode_script = ints(Puzzle(year=2019, day=21).input_data)
        droid = IntcodeEmulator(intcode_script, asyncio.Queue())

        # Provide the inputs.
        run_instr = "WALK" if walk else "RUN"
        input_string = "\n".join(
            [" ".join(x) for x in self.spring_script + [(f"{run_instr}\n",)]]
        )

        for character in input_string:
            droid.inputs.put_nowait(ord(character))

        await droid.run()

        outputs = []
        while not droid.outputs.empty():
            outputs.append(droid.outputs.get_nowait())

        return outputs


def draw_image(integers):
    image = [chr(x) for x in integers]
    print("".join(image))


# PART 1

s = [
    ("NOT", "A", "T"),
    ("OR", "T", "J"),
    ("NOT", "B", "T"),
    ("OR", "T", "J"),
    ("NOT", "C", "T"),
    ("OR", "T", "J"),
    ("AND", "D", "J"),
]
d = SpringDroid(s)
outputs = asyncio.run(d.run())
puzzle.answer_a = outputs[-1]


# PART 2

s = [
    ("NOT", "A", "T"),
    ("OR", "T", "J"),
    ("NOT", "B", "T"),
    ("OR", "T", "J"),
    ("NOT", "C", "T"),
    ("OR", "T", "J"),
    # Check if there is place to stand after the landing.
    ("NOT", "E", "T"),
    ("NOT", "T", "T"),
    # Check if there is a place to jump to after landing.
    ("OR", "H", "T"),
    # If neither is true we hold off.
    ("AND", "T", "J"),
    # Check if there is a place to land.
    ("AND", "D", "J"),
]
d = SpringDroid(s)
outputs = asyncio.run(d.run(False))
puzzle.answer_b = outputs[-1]
