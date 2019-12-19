import asyncio
from copy import copy

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=13)
inputs = aoc.ints(puzzle.input_data)


PIXEL_MAP = {
    0: " ",
    1: "#",
    2: "x",
    3: "_",
    4: "0",
}


# PART 1

async def render_game():
    emulator = aoc.IntcodeEmulator(program=inputs)
    await emulator.run()

    outputs = []
    while True:
        try:
            outputs.append(emulator.outputs.get_nowait())
        except asyncio.QueueEmpty:
            break

    return outputs


output = asyncio.run(render_game())

counter = 0
for i in range(len(output) // 3):
    pixel = output[(i * 3):(i * 3) + 3]
    if pixel[2] == 2:
        counter += 1

puzzle.answer_a = counter


# PART 2

# TODO: Move and backwards compatibility.
class IntDisplay:
    def __init__(self):
        self.pixels = dict()

    def set_pixel(self, pxl, val):
        self.pixels[pxl] = val

    def draw(self):
        min_x = min(x[0] for x in self.pixels.keys())
        max_x = max(x[0] for x in self.pixels.keys())
        min_y = min(x[1] for x in self.pixels.keys())
        max_y = max(x[1] for x in self.pixels.keys())

        grid = []
        for _ in range(max_y - min_y + 1):
            row = []
            for _ in range(max_x - min_x + 1):
                row.append(" ")
            grid.append(row)

        for pxl, val in self.pixels.items():
            x = pxl[0] - min_x
            y = pxl[1] - min_y
            grid[y][x] = val

        grid = grid[::-1]

        for row in grid:
            print("".join([PIXEL_MAP[x] for x in row]))


class Arcade:
    def __init__(self, cpu: aoc.IntcodeEmulator):
        self._cpu = cpu
        self._display = IntDisplay()
        self._state = {}
        self.inputs = asyncio.Queue()

    @property
    def ball(self):
        return next(self._find(4))

    @property
    def block_count(self):
        return len(list(x for x in self._find(2)))

    @property
    def paddle(self):
        return next(self._find(3))

    @property
    def score(self):
        return self._state[(-1, 0)]

    async def run_command(self, command):
        await self._cpu.inputs.put(command)

        outputs = [await self._cpu.outputs.get()]
        while True:
            try:
                outputs.append(self._cpu.outputs.get_nowait())
            except asyncio.QueueEmpty:
                break

        self._update_state(outputs)

    def render(self):
        for k, v in self._state.items():
            if k[0] >= 0:
                self._display.set_pixel(k, v)

        self._display.draw()

    def _find(self, target):
        for key, value in self._state.items():
            if value == target:
                yield key

    def _update_state(self, outputs):
        """Only changed pixels will be updated."""
        for index in range(len(outputs) // 3):
            triple = outputs[(index * 3):(index * 3) + 3]
            self._state[tuple(triple[0:2])] = triple[2]


async def play_game():
    program = copy(inputs)
    program[0] = 2
    queue = asyncio.Queue()

    emulator = aoc.IntcodeEmulator(program=program, inputs=queue)
    arcade = Arcade(emulator)

    async def solve():
        await arcade.run_command(0)

        while arcade.block_count > 0:
            command = arcade.ball[0] - arcade.paddle[0]
            await arcade.run_command(command)

            print(arcade.score)
            arcade.render()

        puzzle.answer_b = arcade.score
        raise SystemExit

    tasks = [solve(), emulator.run()]

    await asyncio.gather(*tasks)


output = asyncio.run(play_game())
