import asyncio
import logging
from copy import copy
from queue import Queue

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=15)
inputs = ints(puzzle.input_data)


class RepairRoomba:
    def __init__(self, program):
        self._brain = None
        self.destination = None
        self.position = (0, 0)
        self.program = program

    async def _move(self, direction):
        self._brain: IntcodeEmulator

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

    async def run(self, commands, init=None):
        self._brain = IntcodeEmulator(self.program, asyncio.Queue())
        event_loop = asyncio.create_task(self._brain.run())
        did_loop = False
        path = set()

        if init is not None:
            for command in init:
                await self._move(command)

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


bfs_result = bfs()
puzzle.answer_a = len(bfs_result)


# PART 2


def modified_bfs(initialize_commands):
    roomba = RepairRoomba(inputs)
    queue = Queue()

    # Add the initial value.
    queue.put([])

    # Set the longest path.
    longest_path = []

    while not queue.empty():
        path = queue.get()

        if len(path) > len(longest_path):
            longest_path = copy(path)
            print(f"Longest path length: {len(longest_path)}")

        for c in (1, 2, 3, 4):
            new_path = copy(path)
            new_path.append(c)

            arrived, did_loop = asyncio.run(roomba.run(new_path, initialize_commands))

            if not did_loop:
                queue.put(new_path)

    return longest_path


modified_bfs_result = modified_bfs(bfs_result)
puzzle.answer_b = len(modified_bfs_result)
