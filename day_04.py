from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=4)
inputs = puzzle.input_data
password_range = range(*[int(x) for x in inputs.split("-")])


# PART 1

def is_valid(pwd: str):
    pair_present = False
    non_decreasing = True

    previous_digit = None
    for digit in pwd:
        if previous_digit is not None:
            if int(digit) < int(previous_digit):
                non_decreasing = False

            if digit == previous_digit:
                pair_present = True
        previous_digit = digit

    return pair_present and non_decreasing


assert is_valid("111111")
assert not is_valid("223450")
assert not is_valid("123789")

valid_count = 0
for password in password_range:
    if is_valid(str(password)):
        valid_count += 1

puzzle.answer_a = valid_count


# PART 2

def is_valid(pwd: str):
    pair_present = False
    non_decreasing = True

    previous_digit = None
    streak = 1
    for digit in pwd:
        if previous_digit is not None:
            if int(digit) < int(previous_digit):
                non_decreasing = False

            if digit == previous_digit:
                streak += 1
            else:
                if streak == 2:
                    pair_present = True
                streak = 1
        previous_digit = digit

    if streak == 2:
        pair_present = True

    return pair_present and non_decreasing


assert is_valid("111122")
assert not is_valid("111111")
assert not is_valid("223450")
assert not is_valid("123789")

valid_count = 0
for password in password_range:
    if is_valid(str(password)):
        valid_count += 1

puzzle.answer_b = valid_count
