"""
AOC-helpers, inspired by GitHub user mcpowers (https://gist.github.com/mcpower/87427528b9ba5cac6f0c679370789661).
"""

import asyncio
import logging
import math
import os
import re
import sys
import typing
from copy import copy
from math import atan2, pi


with open("session_cookie") as f:
    session = f.readline().strip()

os.environ["AOC_SESSION"] = session
sys.setrecursionlimit(100)


# TODO: This can be applied in some old days as well.
def char_array(string: str):
    array = []
    row = []

    for char in string:
        if char == "\n":
            array.append(row)
            row = []
        else:
            row.append(char)

    return array


def lmap(func, *iterables):
    """Thanks mcpowers!"""
    return list(map(func, *iterables))


def make_grid(*dimensions: typing.List[int], fill=None):
    """
    Returns a grid such that 'dimensions' is juuust out of bounds.

    Thanks mcpowers!
    """
    ""
    if len(dimensions) == 1:
        return [fill for _ in range(dimensions[0])]
    next_down = make_grid(*dimensions[1:], fill=fill)
    return [list(next_down) for _ in range(dimensions[0])]


def min_max(l):
    """Thanks mcpowers!"""
    return min(l), max(l)


def max_minus_min(l):
    """Thanks mcpowers!"""
    return max(l) - min(l)


def list_diff(x):
    """Thanks mcpowers!"""
    return [b-a for a, b in zip(x, x[1:])]


def flatten(l):
    """Thanks mcpowers!"""
    return [i for x in l for i in x]


def ints(s: str) -> typing.List[int]:
    """Thanks mserrano!"""
    return lmap(int, re.findall(r"-?\d+", s))


def positive_ints(s: str) -> typing.List[int]:
    """Thanks mserrano!"""
    return lmap(int, re.findall(r"\d+", s))


def floats(s: str) -> typing.List[float]:
    """Thanks mcpowers!"""
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> typing.List[float]:
    """Thanks mcpowers!"""
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> typing.List[str]:
    """Thanks mcpowers!"""
    return re.findall(r"[a-zA-Z]+", s)


#############################
# Intcode related functions #
#############################


class IntcodeEmulator:
    def __init__(self, program, inputs=None, name="default"):
        self._pointer: int = 0
        self._program: typing.List[int] = copy(program)
        self._relative_base = 0
        self._state: typing.List[int] = copy(program)
        self.terminated = False

        self.inputs: asyncio.Queue = inputs
        self.name = name
        self.outputs = asyncio.Queue()

    @property
    def state(self):
        return self._state

    def reset(self):
        self._pointer = 0
        self._relative_base = 0
        self._state = self._program
        self.terminated = False

    async def run(self):
        while not self.terminated:
            output = await self._run_next_opcode()
            if output is not None:
                logging.debug("%s: PUT %s", self.name, output)
                self.outputs.put_nowait(output)

    def _extend_to(self, index):
        if index >= len(self._state):
            extension = [0] * (index - len(self._state) + 1)
            self._state = self._state + extension

    def _get_command_string(self) -> str:
        command = str(self._state[self._pointer])

        while len(command) < 5:
            command = "0" + command

        return command

    def _get_mode(self, index: int) -> int:
        """
        Get the mode for the parameter that is that is <index> away from the pointer.
        """
        return int(self._get_command_string()[3 - index])

    def _get_opcode(self):
        return int(self._get_command_string()[-2:])

    def _get_parameter(self, index: int) -> int:
        """Get the parameter that is <index> away from the pointer."""
        self._extend_to(self._pointer + index)
        p = self._state[self._pointer + index]

        if self._get_mode(index) == 0:
            self._extend_to(p)
            return self._state[p]
        elif self._get_mode(index) == 1:
            return p
        elif self._get_mode(index) == 2:
            self._extend_to(self._pointer + self._relative_base)
            return self._state[self._relative_base + p]
        else:
            raise ValueError(f"Invalid get mode: {self._get_mode(index)}")

    def _store_parameter(self, index: int, value):
        self._extend_to(self._pointer + index)
        p = self._state[self._pointer + index]

        logging.debug("%s: STORE TO %s", self.name, p)
        logging.debug("%s: STORE VALUE %s", self.name, value)

        if self._get_mode(index) == 0:
            self._extend_to(p)
            self._state[p] = value
        elif self._get_mode(index) == 2:
            self._extend_to(self._pointer + self._relative_base)
            self._state[self._relative_base + p] = value
        else:
            raise ValueError(f"Invalid store mode: {self._get_mode(index)}")

    async def _run_next_opcode(self):
        opcode = self._get_opcode()

        if opcode == 1:
            # addition
            result = self._get_parameter(1) + self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 2:
            # multiplication
            result = self._get_parameter(1) * self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 3:
            # input
            inp = await self.inputs.get()
            logging.debug("%s: GET %s", self.name, inp)
            self._store_parameter(1, inp)
            self._pointer += 2
        elif opcode == 4:
            # output
            result = self._get_parameter(1)
            self._pointer += 2
            return result
        elif opcode == 5:
            # jump-if-true
            if bool(self._get_parameter(1)):
                self._pointer = self._get_parameter(2)
            else:
                self._pointer += 3
        elif opcode == 6:
            # jump-if-false
            if not bool(self._get_parameter(1)):
                self._pointer = self._get_parameter(2)
            else:
                self._pointer += 3
        elif opcode == 7:
            # less-than
            result = int(self._get_parameter(1) < self._get_parameter(2))
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 8:
            # equals
            result = int(self._get_parameter(1) == self._get_parameter(2))
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 9:
            # adjust-relative-base
            self._relative_base += self._get_parameter(1)
            self._pointer += 2
        elif opcode == 99:
            # terminate
            logging.debug(f"%s: TERM", self.name)
            self.terminated = True
        else:
            raise ValueError(
                f"{opcode} is not an intcode operator (pointer={self._pointer})"
            )


####################
# Common functions #
####################

def compute_angle(a: typing.Tuple[int, int], b: typing.Tuple[int, int]) -> float:
    """Angle in degrees, starting from the x-axis ("3 o'clock") and moving clockwise."""
    if a == b:
        raise ValueError("Cannot compute angle for identical points.")
    return (atan2((b[1] - a[1]), (b[0] - a[0])) * (180 / pi) + 90) % 360


def manhattan(x, y):
    dist = 0

    for dim in range(len(x)):
        dist += math.fabs(x[dim] - y[dim])

    return int(dist)


def path_to_root(child_parent_map: typing.Dict, child: typing.Any):
    if child in child_parent_map.keys():
        return [child] + path_to_root(child_parent_map, child_parent_map[child])
    else:
        return [child]


###########################
# Maze Related Algorithms #
###########################
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 1  # level

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"


class Portal:
    def __init__(self, name, a: typing.Tuple[int, int], b: typing.Tuple[int, int]):
        self.name = name
        self.entrance = Node(*a)
        self.exit = Node(*b)

    def enter(self, a: Node):
        if a == self.entrance:
            return self.exit
        elif a == self.exit:
            return self.entrance
        else:
            return None


class AStarGraph:
    """https://rosettacode.org/wiki/A*_search_algorithm#Python"""
    def __init__(
            self,
            walkables: typing.List[Node],
            portals: typing.List[Portal],
    ):
        self.portals = portals if portals else []
        self.walkables = walkables

        for portal in self.portals:
            assert portal.entrance in self.walkables
            assert portal.exit in self.walkables

    @staticmethod
    def heuristic(start: Node, goal: Node):
        return manhattan((start.x, start.y, start.z), (goal.x, goal.y, goal.z))

    def get_vertex_neighbours(self, pos: Node):
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x2 = pos.x + dx
            y2 = pos.y + dy

            for node in self.walkables:
                if node.x == x2 and node.y == y2 and node.z == pos.z:
                    yield node

        for portal in self.portals:
            exit = portal.enter(pos)
            if exit:
                print(f"Jump in {portal.name} to {exit})")
                yield exit


def a_star(start, end, graph):
    """https://rosettacode.org/wiki/A*_search_algorithm#Python"""
    # Actual movement cost to each position from the start position.
    g = {start: 0}
    # Estimated movement cost of start to end going via this position.
    f = {start: graph.heuristic(start, end)}

    closed_vertices = set()
    open_vertices = {start}
    came_from = {}

    while len(open_vertices) > 0:
        # Get the vertex in the open list with the lowest F score.
        current = None
        current_f_score = None
        for pos in open_vertices:
            if current is None or f[pos] < current_f_score:
                current_f_score = f[pos]
                current = pos

        # Check if we have reached the goal.
        if current == end:
            # Retrace our route backward.
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, f[end]  # Done!

        # Mark the current vertex as closed.
        open_vertices.remove(current)
        closed_vertices.add(current)

        # Update scores for vertices near the current position.
        for neighbour in graph.get_vertex_neighbours(current):
            if neighbour in closed_vertices:
                continue  # We have already processed this node exhaustively.
            candidate_g = g[current] + 1  # Add the weight of moving to this neighbor.

            if neighbour not in open_vertices:
                open_vertices.add(neighbour)  # Discovered a new vertex.
            elif candidate_g >= g[neighbour]:
                continue  # This G score is worse than previously found.

            # Adopt this G score.
            came_from[neighbour] = current
            g[neighbour] = candidate_g
            h = graph.heuristic(neighbour, end)
            f[neighbour] = g[neighbour] + h

    return None


def a_star_route(
        maze: typing.List[typing.List[typing.Union[int, typing.Any]]],
        start: typing.Tuple[int, int],
        end: typing.Tuple[int, int],
        walkable: typing.Any = 0,
        portals: typing.List[Portal] = None,
):
    walkables = []
    for row_index, row in enumerate(maze):
        for col_index, field in enumerate(row):
            if field == walkable:
                walkables.append(Node(row_index, col_index))

    graph = AStarGraph(walkables, portals)
    route = a_star(Node(*start), Node(*end), graph)
    if route:
        return route[0]
    else:
        return []


def a_star_distance(
        maze: typing.List[typing.List[typing.Union[int, typing.Any]]],
        start: typing.Tuple[int, int],
        end: typing.Tuple[int, int],
        walkable: typing.Any = 0,
        portals: typing.List[Portal] = None,
) -> typing.Union[int, None]:
    route = a_star_route(maze, start, end, walkable, portals)
    return len(route) - 1 if route else None


def find_in_maze(target, maze):
    """Returns first occurence."""
    for row_index, row in enumerate(maze):
        for col_index, field in enumerate(row):
            if field == target:
                return row_index, col_index
