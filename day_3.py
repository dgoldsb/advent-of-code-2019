from copy import copy

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=3)
inputs = puzzle.input_data


def run_command(c, p):
    if c == 'U':
        p[1] += 1
    elif c == 'D':
        p[1] -= 1
    elif c == 'R':
        p[0] += 1
    elif c == 'L':
        p[0] -= 1

    return p


wire_instructions = []  # in hindsight not necessary to had a variable number of wires
wire_coordinates = []
wire_coordinate_distances = []


for wire_input in inputs.splitlines():
    wire_instructions.append(wire_input.split(","))


for wire in wire_instructions:
    wire_coordinates.append(set())
    wire_coordinate_distances.append(dict())

    pointer = [0, 0]
    distance = 0

    for instruction in wire:
        command = instruction[0]

        for _ in range(int(instruction[1:])):
            pointer = run_command(command, pointer)
            distance += 1

            wire_coordinates[-1].add(tuple(pointer))
            wire_coordinate_distances[-1][tuple(pointer)] = distance


common = wire_coordinates[0].intersection(wire_coordinates[1])


# PART 1

distances = [aoc.manhattan((0, 0), x) for x in common]
puzzle.answer_a = min(distances)


# PART 2

delays = [
    wire_coordinate_distances[0][x] + wire_coordinate_distances[1][x] for x in common
]
puzzle.answer_b = min(delays)
