from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=16)
inputs = puzzle.input_data


SWITCH = {
    0: 0,
    1: 1,
    2: 0,
    3: -1,
}


def generate_pattern(index: int, length: int):
    counter = 1

    for _ in range(length):
        yield SWITCH[(counter % (4 * (index + 1)) // (index + 1))]
        counter += 1


def apply_pattern(subject: str) -> str:
    result = []

    list_subject = [int(i) for i in subject]

    for index in range(len(list_subject)):
        digit = 0

        for x, y in zip(list_subject, generate_pattern(index, len(list_subject))):
            digit += x * y

        digit = str(digit)[-1]
        result.append(digit)

    return "".join(result)


def iterate_pattern(subject: str, iterations: int):
    current = subject

    for _ in range(iterations):
        current = apply_pattern(current)
    return current


assert iterate_pattern("12345678", 4) == "01029498"


# PART 1

puzzle.answer_a = iterate_pattern(inputs, 100)[:8]
