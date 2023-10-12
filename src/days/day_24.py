from copy import copy

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.io import char_array

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
                score += 2**power

            power += 1

    return score


# PART 1

state = tuplify(char_array(puzzle.input_data))
states = {state}

while True:
    state = evolve_state(state)
    if state in states:
        break
    else:
        states.add(state)

puzzle.answer_a = score_state(state)


# PART 2


DEFAULT_STATE = [
    [".", ".", ".", ".", "."],
    [".", ".", ".", ".", "."],
    [".", ".", "?", ".", "."],
    [".", ".", ".", ".", "."],
    [".", ".", ".", ".", "."],
]


class RecursiveState:
    """
    This is essentially a doubly linked list of parent and child states. This class
    is way messier than I would like it to be, but it works.
    """

    def __init__(self, child=None, parent=None, starting_state=None):
        self._parent = parent
        self._child = child

        self.level = 0
        if parent:
            self.level = self._parent.level - 1
        elif child:
            self.level = self._child.level + 1

        if starting_state:
            starting_state[2][2] = "?"
        self._state = tuplify(starting_state) if starting_state else DEFAULT_STATE

    @property
    def bugs(self):
        bug_count = 0

        for m in range(self.len_m):
            for n in range(self.len_n):
                if self._state[m][n] == "#":
                    bug_count += 1

        if self._child:
            bug_count += self._child.bugs

        return bug_count

    @property
    def head(self):
        if self._child and self.bugs == self._child.bugs and not self._parent:
            print(f"Head is at level {self.level}")
            return self
        elif not self._parent:
            self._parent = RecursiveState(child=self)
            return self._parent.head
        else:
            return self._parent.head

    @property
    def len_m(self):
        return len(self._state)

    @property
    def len_n(self):
        return len(self._state[0])

    def bug(self, m, n):
        if self._state[m][n] == "#":
            return 1
        else:
            return 0

    def bugs_on_side(self, m_delta, n_delta):
        bug_counter = 0

        if m_delta == 0:
            for m in range(5):
                bug_counter += self.bug(m, 2 - 2 * n_delta)
        elif n_delta == 0:
            for n in range(5):
                bug_counter += self.bug(2 - 2 * m_delta, n)

        return bug_counter

    def update(self):
        print(f"Starting update at {self.level}")

        # Copy the state of the child, as it will change mid-execution.
        child = copy(self._child)

        # Create a new matrix, to avoid overwriting the old one while updating.
        new_matrix = []
        for m in range(self.len_m):
            # Create a new row
            new_row = []
            for n in range(self.len_n):
                # If this is the recursive field, we have a special case
                if self._state[m][n] == "?":
                    self._update_child()
                    new_row.append("?")
                else:
                    adjacent_bugs = self._count_adjacent_bugs(m, n, child)

                    if adjacent_bugs == 1 or (
                        adjacent_bugs == 2 and self._state[m][n] == "."
                    ):
                        new_row.append("#")
                    else:
                        new_row.append(".")

            new_matrix.append(new_row)

        del child

        self._state = tuplify(new_matrix)
        print(f"Finished update at {self.level}, now have {self.bugs} bugs")

    def _count_adjacent_bugs(self, m, n, c):
        adjacent_bugs = 0
        for m_delta, n_delta in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            try:
                m_ = m + m_delta
                n_ = n + n_delta

                assert m_ >= 0
                assert n_ >= 0
                assert m_ < self.len_m
                assert n_ < self.len_n

                adjacent_bugs += self.bug(m_, n_)

                if self._state[m_][n_] == "?" and c:
                    adjacent_bugs += c.bugs_on_side(m_delta, n_delta)
            except AssertionError:
                if not self._parent:
                    self._parent = RecursiveState(child=self)

                adjacent_bugs += self._parent.bug(
                    2 + m_delta,
                    2 + n_delta,
                )

        return adjacent_bugs

    def _update_child(self):
        print(f"Looking to update child of level {self.level}")

        if self.bugs > 0 and not self._child:
            self._child = RecursiveState(parent=self)

        if self._child:
            self._child.update()


state = RecursiveState(starting_state=char_array(puzzle.input_data))

for _ in range(200):
    state = state.head
    state.update()

puzzle.answer_b = state.bugs
