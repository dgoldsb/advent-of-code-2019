"""
AOC-helpers, inspired by GitHub user mcpowers (https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661).
"""

import asyncio
import math
import os
import re
import sys
import typing
from copy import copy


with open("session_cookie") as f:
    session = f.readline().strip()

os.environ["AOC_SESSION"] = session
sys.setrecursionlimit(100000)


def lmap(func, *iterables):
    """Thanks mcpowers!"""
    return list(map(func, *iterables))


def make_grid(*dimensions: typing.List[int], fill=None):
    """
    Returns a grid such that 'dimensions' is juuust out of bounds.

    Thanks mcpowers!
    """
    ""
    if len(dimensions) == 1:
        return [fill for _ in range(dimensions[0])]
    next_down = make_grid(*dimensions[1:], fill=fill)
    return [list(next_down) for _ in range(dimensions[0])]


def min_max(l):
    """Thanks mcpowers!"""
    return min(l), max(l)


def max_minus_min(l):
    """Thanks mcpowers!"""
    return max(l) - min(l)


def list_diff(x):
    """Thanks mcpowers!"""
    return [b-a for a, b in zip(x, x[1:])]


def flatten(l):
    """Thanks mcpowers!"""
    return [i for x in l for i in x]


def ints(s: str) -> typing.List[int]:
    """Thanks mserrano!"""
    return lmap(int, re.findall(r"-?\d+", s))


def positive_ints(s: str) -> typing.List[int]:
    """Thanks mserrano!"""
    return lmap(int, re.findall(r"\d+", s))


def floats(s: str) -> typing.List[float]:
    """Thanks mcpowers!"""
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> typing.List[float]:
    """Thanks mcpowers!"""
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> typing.List[str]:
    """Thanks mcpowers!"""
    return re.findall(r"[a-zA-Z]+", s)


#############################
# Intcode related functions #
#############################


class IntcodeEmulator:
    def __init__(self, program, inputs=None, name="default"):
        self._pointer: int = 0
        self._program: typing.List[int] = copy(program)
        self._state: typing.List[int] = copy(program)
        self._terminated = False

        self.inputs: asyncio.Queue = inputs
        self.name = name
        self.outputs = asyncio.Queue()

    @property
    def state(self):
        return self._state

    def reset(self):
        self._pointer = 0

    async def run(self):
        while not self._terminated:
            output = await self._run_next_opcode()
            if output is not None:
                print(f"{self.name} PUT {output}")
                self.outputs.put_nowait(output)

    def _get_command_string(self) -> str:
        command = str(self._state[self._pointer])

        while len(command) < 5:
            command = "0" + command

        return command

    def _get_mode(self, index: int) -> int:
        """
        Get the mode for the parameter that is that is <index> away from the pointer.
        """
        return int(self._get_command_string()[3 - index])

    def _get_opcode(self):
        return int(self._get_command_string()[-2:])

    def _get_parameter(self, index: int) -> int:
        """Get the parameter that is <index> away from the pointer."""
        p = self._state[self._pointer + index]

        if self._get_mode(index) == 0:
            return self._state[p]
        elif self._get_mode(index) == 1:
            return p
        else:
            raise ValueError(f"Invalid get mode: {self._get_mode(index)}")

    def _store_parameter(self, index: int, value):
        p = self._state[self._pointer + index]

        if self._get_mode(index) == 0:
            self._state[p] = value
        else:
            raise ValueError(f"Invalid store mode: {self._get_mode(index)}")

    async def _run_next_opcode(self):
        opcode = self._get_opcode()

        if opcode == 1:
            # addition
            result = self._get_parameter(1) + self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 2:
            # multiplication
            result = self._get_parameter(1) * self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 3:
            # input
            inp = await self.inputs.get()
            print(f"{self.name} GET {inp}")
            self._store_parameter(1, inp)
            self._pointer += 2
        elif opcode == 4:
            # output
            result = self._get_parameter(1)
            self._pointer += 2
            return result
        elif opcode == 5:
            # jump-if-true
            if bool(self._get_parameter(1)):
                self._pointer = self._get_parameter(2)
            else:
                self._pointer += 3
        elif opcode == 6:
            # jump-if-false
            if not bool(self._get_parameter(1)):
                self._pointer = self._get_parameter(2)
            else:
                self._pointer += 3
        elif opcode == 7:
            # less-than
            result = self._get_parameter(1) < self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 8:
            # equals
            result = self._get_parameter(1) == self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 99:
            # terminate
            print(f"{self.name} TERM")
            self._terminated = True
        else:
            raise ValueError(
                f"{opcode} is not an intcode operator (pointer={self._pointer})"
            )


####################
# Common functions #
####################


def manhattan(x, y):
    dist = 0

    for dim in range(len(x)):
        dist += math.fabs(x[dim] - y[dim])

    return int(dist)


def path_to_root(child_parent_map: typing.Dict, child: typing.Any):
    if child in child_parent_map.keys():
        return [child] + path_to_root(child_parent_map, child_parent_map[child])
    else:
        return [child]
