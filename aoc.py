"""
AOC-helpers, inspired by GitHub user mcpowers (https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661).
"""

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
    """Thanks mcpower!"""
    return list(map(func, *iterables))


def make_grid(*dimensions: typing.List[int], fill=None):
    """
    Returns a grid such that 'dimensions' is juuust out of bounds.

    Thanks mcpower!
    """
    ""
    if len(dimensions) == 1:
        return [fill for _ in range(dimensions[0])]
    next_down = make_grid(*dimensions[1:], fill=fill)
    return [list(next_down) for _ in range(dimensions[0])]


def min_max(l):
    """Thanks mcpower!"""
    return min(l), max(l)


def max_minus_min(l):
    """Thanks mcpower!"""
    return max(l) - min(l)


def list_diff(x):
    """Thanks mcpower!"""
    return [b-a for a, b in zip(x, x[1:])]


def flatten(l):
    """Thanks mcpower!"""
    return [i for x in l for i in x]


def ints(s: str) -> typing.List[int]:
    """Thanks mserrano!"""
    return lmap(int, re.findall(r"-?\d+", s))


def positive_ints(s: str) -> typing.List[int]:
    """Thanks mserrano!"""
    return lmap(int, re.findall(r"\d+", s))


def floats(s: str) -> typing.List[float]:
    """Thanks mcpower!"""
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> typing.List[float]:
    """Thanks mcpower!"""
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> typing.List[str]:
    """Thanks mcpower!"""
    return re.findall(r"[a-zA-Z]+", s)


#############################
# Intcode related functions #
#############################


class IntcodeEmulator:
    __input: int
    __pointer: int
    __program: typing.List[int]
    __state: typing.List[int]
    __terminated: bool

    @property
    def state(self):
        return self.__state

    def reset(self):
        self.__pointer = 0

    def run(self, program: typing.List[int], input_value: int = None):
        self.__input = input_value
        self.__pointer = 0
        self.__program = copy(program)
        self.__state = copy(program)
        self.__terminated = False

        outputs = []

        while not self.__terminated:
            output = self._run_next_opcode()
            outputs.append(output)

        return outputs

    def _get_command_string(self) -> str:
        command = str(self.__state[self.__pointer])

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
        p = self.__state[self.__pointer + index]

        if self._get_mode(index) == 0:
            return self.__state[p]
        elif self._get_mode(index) == 1:
            return p
        else:
            raise ValueError(f"Invalid get mode: {self._get_mode(index)}")

    def _store_parameter(self, index: int, value):
        p = self.__state[self.__pointer + index]

        if self._get_mode(index) == 0:
            self.__state[p] = value
        else:
            raise ValueError(f"Invalid store mode: {self._get_mode(index)}")

    def _run_next_opcode(self):
        opcode = self._get_opcode()

        if opcode == 1:
            # addition
            result = self._get_parameter(1) + self._get_parameter(2)
            self._store_parameter(3, result)
            self.__pointer += 4
        elif opcode == 2:
            # multiplication
            result = self._get_parameter(1) * self._get_parameter(2)
            self._store_parameter(3, result)
            self.__pointer += 4
        elif opcode == 3:
            # input
            self._store_parameter(1, self.__input)
            self.__pointer += 2
        elif opcode == 4:
            # output
            result = self._get_parameter(1)
            self.__pointer += 2
            return result
        elif opcode == 5:
            # jump-if-true
            if bool(self._get_parameter(1)):
                self.__pointer = self._get_parameter(2)
            else:
                self.__pointer += 3
        elif opcode == 6:
            # jump-if-false
            if not bool(self._get_parameter(1)):
                self.__pointer = self._get_parameter(2)
            else:
                self.__pointer += 3
        elif opcode == 7:
            # less-than
            result = self._get_parameter(1) < self._get_parameter(2)
            self._store_parameter(3, result)
            self.__pointer += 4
        elif opcode == 8:
            # equals
            result = self._get_parameter(1) == self._get_parameter(2)
            self._store_parameter(3, result)
            self.__pointer += 4
        elif opcode == 99:
            # terminate
            self.__terminated = True
        else:
            raise ValueError(
                f"{opcode} is not an intcode operator (pointer={self.__pointer})"
            )


####################
# Common functions #
####################


def manhattan(x, y):
    dist = 0

    for dim in range(len(x)):
        dist += math.fabs(x[dim] - y[dim])

    return int(dist)
