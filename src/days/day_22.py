import math
from functools import partial
from typing import Generator, Callable

from aocd.models import Puzzle

import src.module.io  # set the session cookie

puzzle = Puzzle(year=2019, day=22)


# PART 1
DECK_SIZE = 10007


def cut(d, integer):
    new_deck = d[integer:] + d[:integer]
    del d

    return new_deck


def deal(d, increment=None):
    if increment is None:
        new_deck = d[::-1]
    else:
        new_deck = [None] * len(d)

        for i in range(0, len(d)):
            new_index = (i * increment) % len(d)
            new_deck[new_index] = d[i]

    del d

    return new_deck


OPERATIONS = {
    "cut": cut,
    "deal": deal,
}


def parse_operations():
    puzzle = Puzzle(year=2019, day=22)
    inputs = puzzle.input_data.splitlines()

    operations = []
    for line in inputs:
        line_list = line.split(" ")

        op = OPERATIONS[line_list[0]]
        try:
            arg = int(line_list[-1])
        except ValueError:
            arg = None

        operations.append(
            (
                op,
                arg,
            )
        )

    return operations


deck = list(range(0, DECK_SIZE))
for operation in parse_operations():
    deck = operation[0](deck, operation[1])
puzzle.answer_a = deck.index(2019)


# PART 2
def parse_reverse_operations(inputs: list[str]) -> Generator[Callable[[int, int], int], None, None]:
    for line in inputs[::-1]:
        match line.split(" "):
            case ["deal", "into", "new", "stack"]:
                yield reverse_deal_new
            case ["cut", arg]:
                yield partial(reverse_cut, int(arg))
            case ["deal", "with", "increment", arg]:
                yield partial(reverse_deal_increment, int(arg))


def reverse_deal_new(index_: int, deck_size: int):
    """Find the index before doing a deal new operation on a deck of cards of a given size.

    Args:
        index_: The index of the card we want to find the before index of.
        deck_size: The size of the deck.
    """
    # This is essentially a reverse operation.
    return (-1 - index_) % deck_size


assert reverse_deal_new(0, 10) == 9
assert reverse_deal_new(9, 10) == 0
assert reverse_deal_new(4, 10) == 5


def reverse_cut(cut_at: int, index_: int, deck_size: int):
    """Find the index before doing a deal new operation on a deck of cards of a given size.

    Args:
        cut_at: The number of cards to cut, this section of the top is moved to the bottom of the deck.
        index_: The index of the card we want to find the before index of.
        deck_size: The size of the deck.
    """
    if cut_at < 0:
        if index_ < -1 * cut_at:
            return index_ + (deck_size + cut_at)
        else:
            return index_ + cut_at

    if index_ < cut_at:
        return index_ + cut_at
    else:
        return index_ - (deck_size - cut_at)


assert reverse_cut(3, 8, 10) == 1
assert reverse_cut(3, 2, 10) == 5
assert reverse_cut(3, 9, 10) == 2
assert reverse_cut(-4, 5, 10) == 1
assert reverse_cut(-4, 3, 10) == 9
assert reverse_cut(-4, 5, 10) == 1


def reverse_deal_increment(increment_by: int, index_: int, deck_size: int) -> int:
    """Find the index before doing a deal with increment operation on a deck of cards of a given size.

    Args:
        increment_by: The number of cards to increment by.
        index_: The index of the card we want to find the before index of.
        deck_size: The size of the deck.
    """
    # First, we figure out how many "laps" we need to do through the deck before we reach the target index.
    # TODO: Yeah this is wrong.
    target_lap = (increment_by - (index_ % increment_by)) % increment_by

    # Second, we need to know how many cards to deal in the target lap we need to deal before we reach the target index.
    stop_in_target_lap = index_ // increment_by

    # Finally, we need to find the number of cards already dealt in the previous laps.
    numbers_in_previous_laps = 0
    for i in range(target_lap):
        effective_deck_size = deck_size - i
        lap_size = math.ceil(effective_deck_size / increment_by)
        numbers_in_previous_laps += lap_size

    # Add the numbers in the previous laps to the number of cards to deal in the target lap.
    return numbers_in_previous_laps + stop_in_target_lap


assert reverse_deal_increment(7, 2, 10) == 4

assert reverse_deal_increment(3, 0, 10) == 0
assert reverse_deal_increment(3, 1, 10) == 7
assert reverse_deal_increment(3, 2, 10) == 4
assert reverse_deal_increment(3, 3, 10) == 1
assert reverse_deal_increment(3, 4, 10) == 8
assert reverse_deal_increment(3, 5, 10) == 5
assert reverse_deal_increment(3, 6, 10) == 2
assert reverse_deal_increment(3, 7, 10) == 9
assert reverse_deal_increment(3, 8, 10) == 6
assert reverse_deal_increment(3, 9, 10) == 3

test_input = """deal with increment 7
deal into new stack
deal into new stack"""
index = 3
deck_size = 10
for operation in parse_reverse_operations(test_input.splitlines()):
    result = operation(index, deck_size)
    index = result
print(index)
assert index == 9


index = int(puzzle.answer_a)
for operation in parse_reverse_operations(puzzle.input_data.splitlines()):
    index = operation(index, DECK_SIZE)
print(index)
assert index == 2019

# TODO:
#  - Fix reverse_deal_increment
#  - Verify with reversing some test inputs
#  - Verify with reversing the input for A
#  - Figure out the pattern