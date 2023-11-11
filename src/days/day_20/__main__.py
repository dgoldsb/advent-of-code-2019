"""Day 20: Donut Maze"""
from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.days.day_20.portal_maze_builder import PortalMazeBuilder
from src.days.day_20.portal_maze_solver import PortalMazeSolver

# PART 1

puzzle = Puzzle(year=2019, day=20)
inputs = puzzle.input_data
builder = PortalMazeBuilder(inputs)
builder.build()
start, destination = builder.build()
solver = PortalMazeSolver()
puzzle.answer_a = solver.evaluate_path_length(solver.solve(start, destination))

# PART 2
