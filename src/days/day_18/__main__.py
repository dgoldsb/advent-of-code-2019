"""Day 18: Many-Worlds Interpretation"""
from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.days.day_18.key_maze_builder import KeyMazeBuilder
from src.days.day_18.key_maze_node import KeyMazeNode
from src.days.day_18.key_maze_solver import KeyMazeSolver

puzzle = Puzzle(year=2019, day=18)
inputs = puzzle.input_data

# PART 1

builder = KeyMazeBuilder(inputs)
start = builder.build().pop()
destination = KeyMazeNode(0, 0, builder.count_keys(), "!")
solver = KeyMazeSolver(1)
solution_a = solver.evaluate_path_length(solver.solve((start,), (destination,)))
puzzle.answer_a = solution_a


# PART 2
def turn_into_b_input(a_input):
    b_input = list(a_input)
    line_length = len(inputs.splitlines()[0]) + 1
    start_index = inputs.index("@")
    b_input[start_index - line_length - 1] = "@"
    b_input[start_index - line_length] = "#"
    b_input[start_index - line_length + 1] = "@"
    b_input[start_index - 1] = "#"
    b_input[start_index] = "#"
    b_input[start_index + 1] = "#"
    b_input[start_index + line_length - 1] = "@"
    b_input[start_index + line_length] = "#"
    b_input[start_index + line_length + 1] = "@"
    return "".join(b_input)


builder = KeyMazeBuilder(turn_into_b_input(inputs))
destination = KeyMazeNode(0, 0, builder.count_keys(), "!")
starts = tuple(builder.build())
solution_b = solver.evaluate_path_length(KeyMazeSolver(len(starts)).solve(starts, (destination,)))
puzzle.answer_b = solution_b
