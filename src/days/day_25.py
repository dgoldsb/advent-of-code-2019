import asyncio
import itertools
from copy import copy

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import AsciiComputer
from src.module.io import ints

puzzle = Puzzle(year=2019, day=25)


async def run_game(moves):
    """
    Step 1: Play the game and collect all collectable items.
    Step 2: Dump this and use these instructions as the starting point.
    Step 3: Use itertools to find out the things to drop to get past the checkpoint.
    """
    computer = AsciiComputer(ints(Puzzle(year=2019, day=25).input_data))

    return await computer.run(moves)


moves = iter(
    [
        # TODO: Put instructions to gather items here.
    ]
)
moves = asyncio.run(run_game(moves))

items = [
    # TODO: Put items here.
]
combinations = itertools.combinations(items)

for combination in combinations:
    m = copy(moves)
    for item in combination:
        m.append(f"drop {item}")
    m.append("exit")

    asyncio.run(run_game(m))


# TODO: Go back and use ASCII computer in other problems.
