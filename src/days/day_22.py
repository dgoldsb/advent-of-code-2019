from functools import partial
from typing import Callable, Generator

from aocd.models import Puzzle

import src.module.io  # set the session cookie

puzzle = Puzzle(year=2019, day=22)


# PART 1

DECK_SIZE_A = 10007


def cut(d: list[int], cut_by: int):
    new_deck = d[cut_by:] + d[:cut_by]
    del d
    return new_deck


def deal(d, deal_increment=None):
    if deal_increment is None:
        new_deck = d[::-1]
    else:
        new_deck = [None] * len(d)

        for i in range(0, len(d)):
            new_index = (i * deal_increment) % len(d)
            new_deck[new_index] = d[i]

    del d

    return new_deck


def parse_operations() -> Generator[Callable[[list[int]], list[int]], None, None]:
    for line_ in puzzle.input_data.splitlines():
        match line_.split(" "):
            case ["deal", "into", "new", "stack"]:
                yield deal
            case ["cut", cut_by]:
                yield partial(cut, cut_by=int(cut_by))
            case ["deal", "with", "increment", deal_increment]:
                yield partial(deal, deal_increment=int(deal_increment))


deck = list(range(0, DECK_SIZE_A))
for operation in parse_operations():
    deck = operation(deck)
puzzle.answer_a = deck.index(2019)

# PART 2
# Note: I did not get here myself, I in the end resorted to mcpower's explanation for help, treating it more like a
# learning experience.

DECK_SIZE_B = 119315717514047
REPEATS = 101741582076661


def get_modular_inverse(n: int):
    """Assumes `DECK_SIZE_B` is prime to use Euler's theorem."""
    return pow(n, DECK_SIZE_B - 2, DECK_SIZE_B)


def get(offset_: int, increment_: int, i: int):
    """Gets the ith number in a given sequence."""
    return (offset_ + i * increment_) % DECK_SIZE_B


# The increment is the difference between two adjacent numbers.
# Doing the process will multiply increment by `increment_multiplier`.
increment_multiplier = 1

# The offset is the first number in the sequence.
# Doing the process will increment this by `offset_difference` + (the increment before the process started).
offset_difference = 0

for line in puzzle.input_data.splitlines():
    match line.split(" "):
        case ["deal", "into", "new", "stack"]:
            # Reverse sequence: instead of going up, go down.
            increment_multiplier *= -1
            increment_multiplier %= DECK_SIZE_B
            # Then shift 1 left.
            offset_difference += increment_multiplier
            offset_difference %= DECK_SIZE_B
        case ["cut", arg]:
            left_shift = int(arg)
            # shift q left
            offset_difference += left_shift * increment_multiplier
            offset_difference %= DECK_SIZE_B
        case ["deal", "with", "increment", arg]:
            q = int(arg)
            # Difference between two adjacent numbers is multiplied by the inverse of the increment.
            increment_multiplier *= get_modular_inverse(q)
            increment_multiplier %= DECK_SIZE_B


def get_sequence(iterations):
    # Calculate (increment, offset) for the number of iterations of the process.
    # increment = increment_mul^iterations
    increment_ = pow(increment_multiplier, iterations, DECK_SIZE_B)
    # Use geometric series.
    # offset = 0 + offset_diff * (1 + increment_mul + increment_mul^2 + ... + increment_mul^iterations)
    offset_ = (
        offset_difference
        * (1 - increment_)
        * get_modular_inverse((1 - increment_multiplier) % DECK_SIZE_B)
    )
    offset_ %= DECK_SIZE_B
    return increment_, offset_


increment, offset = get_sequence(REPEATS)
puzzle.answer_b = get(offset, increment, 2020)
