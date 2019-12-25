from aocd.models import Puzzle

import aoc


puzzle = Puzzle(year=2019, day=24)


def tuplify(matrix):
    return tuple([tuple(x) for x in matrix])


def evolve_state(matrix):
    len_m = len(matrix)
    len_n = len(matrix[0])

    new_matrix = []
    for m in range(len_m):
        new_row = []
        for n in range(len_n):
            adjacent_bugs = 0
            for m_delta, n_delta in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                try:
                    m_ = m + m_delta
                    n_ = n + n_delta

                    assert m_ >= 0
                    assert n_ >= 0
                    assert m_ < len_m
                    assert n_ < len_n

                    if matrix[m_][n_] == "#":
                        adjacent_bugs += 1
                except AssertionError:
                    pass

            if adjacent_bugs == 1 or (adjacent_bugs == 2 and matrix[m][n] == "."):
                new_row.append("#")
            else:
                new_row.append(".")

        new_matrix.append(new_row)

    return tuplify(new_matrix)


def score_state(matrix):
    power = 0
    score = 0

    len_m = len(matrix)
    len_n = len(matrix[0])

    for m in range(len_m):
        for n in range(len_n):
            if matrix[m][n] == "#":
                score += 2 ** power

            power += 1

    return score


# PART 1

state = tuplify(aoc.char_array(puzzle.input_data))
states = {state}

while True:
    print(state)
    state = evolve_state(state)
    if state in states:
        break
    else:
        states.add(state)

puzzle.answer_a = score_state(state)


# PART 2

# TODO: More Plutonian stuff...
