from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=22)


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

        operations.append((op, arg,))

    return operations


# PART 1

deck = list(range(0, DECK_SIZE))

for operation in parse_operations():
    deck = operation[0](deck, operation[1])

puzzle.answer_a = deck.index(2019)


# PART 2
# We need to reverse engineer this one, first of all. We need to track card at index
# 2020 to where it is after one shuffle cycle. We can see each shuffle cycle as a
# constant operation, so here too we need to figure out a cycle.

def r_deal_new(index, deck_size):
    return (-1 - index) % deck_size


def r_deal(index, deck_size, increment):
    pass


def r_cut(index, deck_size, integer):
    return (index + integer) % deck_size


# TODO: Apparently this is not doable without diving into modular arithmatic,
#  saving this for later...
