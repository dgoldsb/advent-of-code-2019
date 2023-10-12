import asyncio
import itertools

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=7)
inputs = ints(puzzle.input_data)


# PART 1


async def part_1():
    signals = []
    for permutation in itertools.permutations(range(5)):
        inp = 0
        for phase_setting in permutation:
            queue = asyncio.Queue()

            queue.put_nowait(phase_setting)
            queue.put_nowait(inp)

            emulator = IntcodeEmulator(program=inputs, inputs=queue)
            await emulator.run()
            inp = emulator.outputs.get_nowait()

        signals.append(inp)

    return max(signals)


puzzle.answer_a = asyncio.run(part_1())


# PART 2


async def part_2():
    signals = []
    for permutation in itertools.permutations(range(5, 10)):
        amps = []

        # Add amps.
        for i in range(len(permutation)):
            amps.append(IntcodeEmulator(program=inputs, name=f"PID {i}"))

        # Update inputs.
        for i in range(len(permutation)):
            amps[i].inputs = amps[(4 + i) % len(permutation)].outputs

        # Create initial state.
        for i in range(len(permutation)):
            amps[i].inputs.put_nowait(permutation[i])
        amps[0].inputs.put_nowait(0)

        tasks = [amp.run() for amp in amps]

        await asyncio.gather(*tasks)

        signals.append(await amps[-1].outputs.get())

    return max(signals)


puzzle.answer_b = asyncio.run(part_2())
