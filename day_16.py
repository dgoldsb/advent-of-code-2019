import logging
import numpy as np
import sys
from functools import lru_cache

from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=16)
inputs = puzzle.input_data


@lru_cache()
def generate_matrix(length: int):
    # TODO: This is 10GB for the full thing, fuck.
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


# PART 1

puzzle.answer_a = iterate_pattern(inputs, 100)[:8]


# PART 2

def calculate_part_2(subject: str):
    output = iterate_pattern(subject * 10000, 100)
    offset = int(output[:7])
    return output[offset:offset + 8]


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
print(calculate_part_2("03036732577212944063491565474664"))
#assert calculate_part_2("03036732577212944063491565474664") == "84462026"