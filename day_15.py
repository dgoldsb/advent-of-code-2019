import asyncio
import logging
from copy import copy
from queue import Queue

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=15)
inputs = aoc.ints(puzzle.input_data)


class RepairRoomba:
    def __init__(self, program):
        self._brain = None
        self.destination = None
        self.position = (0, 0)
        self.program = program

    async def _move(self, direction):
        self._brain: aoc.IntcodeEmulator

        logging.debug("Moving in direction %d", direction)
        await self._brain.inputs.put(direction)
        output = await self._brain.outputs.get()
        logging.debug("Received return value %s", output)

        if output in (1, 2):
            if direction == 1:
                self.position = (self.position[0] + 1, self.position[1])
            elif direction == 2:
                self.position = (self.position[0] - 1, self.position[1])
            elif direction == 3:
                self.position = (self.position[0], self.position[1] - 1)
            elif direction == 4:
                self.position = (self.position[0], self.position[1] + 1)
            else:
                raise ValueError

        if output == 2:
            self.destination = self.position

        return output

    async def run(self, commands):
        self._brain = aoc.IntcodeEmulator(self.program, asyncio.Queue())
        event_loop = asyncio.create_task(self._brain.run())
        did_loop = False
        path = set()

        for command in commands:
            path.add(self.position)

            await self._move(command)

            did_loop = did_loop or self.position in path

        event_loop.cancel()

        return self.destination == self.position, did_loop


# PART 1

def bfs():
    roomba = RepairRoomba(inputs)
    queue = Queue()

    # Add the initial value.
    queue.put([])

    while not queue.empty():
        path = queue.get()

        for c in (1, 2, 3, 4):
            new_path = copy(path)
            new_path.append(c)

            arrived, did_loop = asyncio.run(roomba.run(new_path))

            if arrived:
                return new_path
            if not did_loop:
                queue.put(new_path)


result = bfs()
print(result)
