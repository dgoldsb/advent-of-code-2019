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

def parse_instruction(instr: int):
    instr = str(instr)

    if len(instr) < 3:
        return int(instr), (0, 0, 0)

    instr = "0" * (5 - len(instr)) + instr

    return int(instr[-2:]), (int(instr[2]), int(instr[1]), int(instr[0]))


def get_parameter(x: typing.List[int], p: int, m: int):
    v = x[p]
    if m == 0:
        return x[v]
    elif m == 1:
        return v
    else:
        raise ValueError


def run_intcode(x: typing.List[int], p: int, input: int):
    opcode, modes = parse_instruction(x[p])

    if opcode == 1:
        v = get_parameter(x, p + 1, modes[0]) + get_parameter(x, p + 2, modes[1])
        x[x[p + 3]] = v
        return True, x, p+4, None
    elif opcode == 2:
        v = get_parameter(x, p + 1, modes[0]) * get_parameter(x, p + 2, modes[1])
        x[x[p + 3]] = v
        return True, x, p+4, None
    elif opcode == 3:
        x[x[p + 1]] = input
        return True, x, p+2, None
    elif opcode == 4:
        v = get_parameter(x, p + 1, modes[0])
        return True, x, p+2, v
    elif opcode == 5:
        if get_parameter(x, p + 1, modes[0]) > 0:
            p = get_parameter(x, p + 2, modes[1])
        else:
            p += 3
        return True, x, p, None
    elif opcode == 6:
        if get_parameter(x, p + 1, modes[0]) == 0:
            p = get_parameter(x, p + 2, modes[1])
        else:
            p += 3
        return True, x, p, None
    elif opcode == 7:
        v = get_parameter(x, p + 1, modes[0]) < get_parameter(x, p + 2, modes[1])
        x[x[p + 3]] = int(v)
        return True, x, p+4, None
    elif opcode == 8:
        v = get_parameter(x, p + 1, modes[0]) == get_parameter(x, p + 2, modes[1])
        x[x[p + 3]] = int(v)
        return True, x, p+4, None
    elif opcode == 99:
        return False, x, p+1, None
    else:
        raise ValueError(f"{x[p]} is not an intcode operator (pointer={p})")


def run_intcode_program(s: typing.List[int], input: int = None):
    sequence = copy(s)
    cont = True
    pointer = 0
    outputs = []

    while cont:
        cont, sequence, pointer, output = run_intcode(sequence, pointer, input)
        outputs.append(output)

    return sequence, outputs


####################
# Common functions #
####################


def manhattan(x, y):
    dist = 0

    for dim in range(len(x)):
        dist += math.fabs(x[dim] - y[dim])

    return int(dist)
