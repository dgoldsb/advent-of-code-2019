"""Day 18: Many-Worlds Interpretation"""
import typing
from collections import defaultdict
from copy import copy
from functools import lru_cache
from typing import Generator
from heapq import heappush, heappop, heapify

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.io import char_array
from src.module.pathfinding import a_star_distance

puzzle = Puzzle(year=2019, day=18)
inputs = puzzle.input_data


class IndexNotFoundError(Exception):
    pass


# TODO: Remove repeated char_array, need to know indexes of keys and doors.
# TODO: get_vertex_neighbours is slow
# TODO: queue over list


class Maze:
    def __init__(self, key_coordinates: dict[str, tuple[int, int]], door_coordinates: dict[str, tuple[int, int]], maze: list[list[str]]):
        self.__raw_maze = raw_maze
        self.__array_maze = char_array(raw_maze)

    @classmethod
    def from_string(cls, string: str):
        return cls(string)

    def find_first_index(self, char: str) -> typing.Tuple[int, int]:
        for row_index, row in enumerate(self.__array_maze):
            for col_index, field in enumerate(row):
                if field == char:
                    return row_index, col_index
        raise IndexNotFoundError(f"Could not find {char} in maze")

    def as_array(self) -> typing.List[typing.List[str]]:
        return self.__array_maze

    def __str__(self):
        return self.__raw_maze


@lru_cache(maxsize=10**6)
def cached_a_star_distance(
    raw_maze: str, start: str, end: str
) -> typing.Union[int, None]:
    # TODO: more aggressive caching, we have so few distances, but the doors make this hard.
    maze = Maze(raw_maze)
    return a_star_distance(
        maze=Maze(copy(raw_maze).replace(start, ".").replace(end, ".")).as_array(),
        start=maze.find_first_index(start),
        end=maze.find_first_index(end),
        walkable=".",
    )


class MazeUniverse:
    """Assume you are at @."""

    def __init__(self, maze: Maze, steps_taken: int, keys_found=0):
        self.__maze = maze
        self.steps_taken = steps_taken
        self.keys_found = keys_found

    def __lt__(self, other):
        if self.keys_found != other.keys_found:
            return self.keys_found > other.keys_found

        return self.steps_taken < other.steps_taken

    def __hash__(self):
        return hash(str(self.__maze))

    def _keys(self) -> Generator[str, None, None]:
        for char in "abcdefghijklmnopqrstuvwxyz":
            if char in str(self.__maze):
                yield char

    def _find_reachable_keys(self) -> Generator[str, None, None]:
        for key in self._keys():
            try:
                distance = cached_a_star_distance(
                    raw_maze=str(self.__maze), start="@", end=key
                )
                if distance is not None:
                    yield key
            except IndexNotFoundError:
                pass

    def spawn_new_universes(self) -> Generator["MazeUniverse", None, None]:
        for key in self._find_reachable_keys():
            # Count the steps taken.
            additional_steps_taken = cached_a_star_distance(
                raw_maze=str(self.__maze), start="@", end=key
            )

            # Move you to the key.
            new_raw_maze = str(self.__maze)
            new_raw_maze = new_raw_maze.replace("@", ".")
            new_raw_maze = new_raw_maze.replace(key, "@")
            new_raw_maze = new_raw_maze.replace(key.upper(), ".")

            yield MazeUniverse(
                Maze(new_raw_maze),
                self.steps_taken + additional_steps_taken,
                self.keys_found + 1,
            )

    @property
    def completed(self) -> bool:
        """Completed when all keys are found."""
        return not list(self._keys())


class MazeSolver:
    def __init__(self, start_maze_universe: MazeUniverse):
        self.__live_universes = []
        heappush(self.__live_universes, start_maze_universe)
        self.__solutions = []
        self.__seen = {start_maze_universe}
        self.__lowest = None  # TODO: to default dict
        self.__most_keys = 0  # lazy way of getting the number of keys

    def __is_valid(self, universe: MazeUniverse) -> bool:
        if self.__lowest is None:
            return True

        steps_taken = universe.steps_taken
        best_solution = self.__lowest

        average_steps_per_key = steps_taken / self.__most_keys
        keys_left = self.__most_keys - universe.keys_found

        # steps_below_best_solution = (steps_taken + average_steps_per_key * keys_left) < best_solution
        steps_below_best_solution = steps_taken < best_solution

        # TODO: More heuristic pruning.
        # TODO: EVEN MORE, keep the best per number of keys found. Add some knobs to turn.
        return steps_below_best_solution

    def __clean_live_universes(self):
        self.__live_universes = list(filter(self.__is_valid, self.__live_universes))
        heapify(self.__live_universes)

    def solve(self) -> int:
        while self.__live_universes:
            universe = heappop(self.__live_universes)
            if universe.completed:
                if self.__lowest is None or universe.steps_taken < self.__lowest:
                    self.__lowest = universe.steps_taken
                    self.__most_keys = universe.keys_found
                    print(f"New lowest: {self.__lowest}")
                    print(f"Total of {len(self.__live_universes)} live universes left")
                    self.__clean_live_universes()
                    print(f"Total of {len(self.__live_universes)} live universes left")
            else:
                for new_universe in universe.spawn_new_universes():
                    if new_universe not in self.__seen and self.__is_valid(
                        new_universe
                    ):
                        self.__seen.add(new_universe)
                        heappush(self.__live_universes, new_universe)

        return self.__lowest


inputs = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""
# PART 1
print(MazeSolver(MazeUniverse(Maze(inputs), 0)).solve())
