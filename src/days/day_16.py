import logging
from functools import lru_cache

import numpy as np
from aocd.models import Puzzle

import src.module.io  # set the session cookie

puzzle = Puzzle(year=2019, day=16)
inputs = puzzle.input_data


# PART 1


@lru_cache()
def generate_matrix(length: int):
    matrix = []

    logging.info("Starting matrix generation of size %dx%d", length, length)

    for i in range(length):
        logging.debug("Generating row %d/%d", i, length)
        row = [0] * i
        pattern = [1] * (i + 1) + [0] * (i + 1) + [-1] * (i + 1) + [0] * (i + 1)
        mult = (length - i) // len(pattern) + 1
        row += pattern * mult
        matrix.append(row[:length])

    logging.info("Finished matrix generation of size %dx%d", length, length)

    return np.array(matrix)


def apply_pattern(subject: str) -> str:
    vector_in = np.array([int(i) for i in subject])

    logging.info("Start multiplying matrix with vector...")
    vector_out = generate_matrix(len(subject)).dot(vector_in)
    logging.info("Finished multiplying matrix with vector")

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

puzzle.answer_a = iterate_pattern(inputs, 100)[:8]


# PART 2

# It finally clicked:
# - The offset is beyond the half-way point.
# - Everything beyond the half-way point follows the simple rule where the
#   v[i][t+1] = v[i][t] + v[i+1][t+1].
# - The last value always stays the same.
# - For v[i], index before i will ever matter, no matter how many iteration.


def solve(subject: str, iterations: int):
    subject = [int(x) for x in subject]
    for _ in range(iterations):
        for i in range(-2, -len(subject) - 1, -1):
            subject[i] = (subject[i] + subject[i + 1]) % 10

    return "".join([str(x) for x in subject])


offset = int(inputs[:7])
relevant_input = (inputs * 10000)[offset:]
puzzle.answer_b = solve(relevant_input, 100)[:8]
