import numpy as np
from functools import lru_cache

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=16)
inputs = puzzle.input_data


@lru_cache()
def generate_matrix(length: int):
    # TODO: This is too slow.
    switch = {
        0: 0,
        1: 1,
        2: 0,
        3: -1,
    }

    matrix = []
    for i in range(length):
        row = []
        for j in range(length):
            row.append(switch[((j + 1) % (4 * (i + 1)) // (i + 1))])
        matrix.append(row)

    return np.array(matrix)


def apply_pattern(subject: str) -> str:
    vector_in = np.array([int(i) for i in subject])

    vector_out = generate_matrix(len(subject)).dot(vector_in)

    string_out = ""

    for number in vector_out:
        string_out += str(number)[-1]

    return string_out


def iterate_pattern(subject: str, iterations: int):
    current = subject

    for i in range(iterations):
        current = apply_pattern(current)
    return current


assert iterate_pattern("12345678", 4) == "01029498"


# PART 1

puzzle.answer_a = iterate_pattern(inputs, 100)[:8]


# PART 2

def calculate_part_2(subject: str):
    output = iterate_pattern(subject * 10000, 100)
    offset = int(output[:7])
    return output[offset:offset + 8]


print(calculate_part_2("03036732577212944063491565474664"))
#assert calculate_part_2("03036732577212944063491565474664") == "84462026"