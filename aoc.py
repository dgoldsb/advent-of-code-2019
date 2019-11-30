"""
AOC-helpers, inspired by GitHub user mcpowers (https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661).
"""

import os
import re
import sys
import typing


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
