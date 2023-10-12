import asyncio
from collections import defaultdict
from enum import Enum

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=11)
inputs = ints(puzzle.input_data)


class Direction(Enum):
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"


TURN_LEFT = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP,
}
TURN_RIGHT = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}


class PaintRobot:
    def __init__(self):
        self._brain = IntcodeEmulator(program=inputs)
        self._direction = Direction.UP
        self._location = (0, 0)

        self.black = set()
        self.white = set()

        self.history = defaultdict(lambda: 0)

    async def run(self):
        # Make sure the queues are created in the same event loop.
        self._brain.inputs = asyncio.Queue()
        self._brain.outputs = asyncio.Queue()

        tasks = [self._brain.run(), self._run_event_loop()]

        await asyncio.gather(*tasks)

    async def _run_event_loop(self):
        while not self._brain.terminated:
            await self._step()

    async def _step(self):
        await self._brain.inputs.put(self._current_color())
        color = await self._brain.outputs.get()
        direction = await self._brain.outputs.get()

        self._paint(color)
        self._turn(direction)
        self._move()

    def _current_color(self):
        if self._location in self.white:
            return 1
        else:
            return 0

    def _turn(self, direction: int):
        if direction == 0:
            self._direction = TURN_LEFT[self._direction]
        elif direction == 1:
            self._direction = TURN_RIGHT[self._direction]

    def _move(self):
        if self._direction == Direction.UP:
            self._location = (self._location[0], self._location[1] + 1)
        elif self._direction == Direction.DOWN:
            self._location = (self._location[0], self._location[1] - 1)
        elif self._direction == Direction.RIGHT:
            self._location = (self._location[0] + 1, self._location[1])
        elif self._direction == Direction.LEFT:
            self._location = (self._location[0] - 1, self._location[1])

    def _paint(self, color: int):
        self.history[self._location] += 1

        if color == 0:
            self.black.add(self._location)
            try:
                self.white.remove(self._location)
            except KeyError:
                pass
        elif color == 1:
            try:
                self.black.remove(self._location)
            except KeyError:
                pass
            self.white.add(self._location)


async def run_paint_robot(start_color: int):
    robot = PaintRobot()

    if start_color == 0:
        robot.black.add((0, 0))
    elif start_color == 1:
        robot.white.add((0, 0))

    await robot.run()

    return robot


# PART 1

paint_robot = asyncio.run(run_paint_robot(0))
puzzle.answer_a = len(paint_robot.history)


# PART 2

paint_robot = asyncio.run(run_paint_robot(1))

min_x = min(x[0] for x in paint_robot.white.union(paint_robot.black))
min_y = min(x[1] for x in paint_robot.white.union(paint_robot.black))
max_x = max(x[0] for x in paint_robot.white.union(paint_robot.black))
max_y = max(x[1] for x in paint_robot.white.union(paint_robot.black))

grid = []
for _ in range(max_y - min_y + 1):
    row = []
    for _ in range(max_x - min_x + 1):
        row.append(".")
    grid.append(row)

for coord in paint_robot.white:
    x = coord[0] - min_x
    y = coord[1] - min_y
    grid[y][x] = "#"

grid = grid[::-1]

for row in grid:
    print("".join(row))
