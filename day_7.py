import itertools

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=7)
inputs = aoc.ints(puzzle.input_data)


# PART 1

signals = []
for permutation in itertools.permutations(range(5)):
    inp = 0
    for phase_setting in permutation:
        emulator = aoc.IntcodeEmulator()
        outputs = emulator.run(inputs, inputs=iter([phase_setting, inp]))
        inp = outputs[0]

    signals.append(inp)

puzzle.answer_a = max(signals)


# PART 2
