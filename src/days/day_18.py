"""Day 18: Many-Worlds Interpretation"""
from dataclasses import dataclass
from typing import Generator, Optional

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.a_star.base_graph_builder import BaseGraphBuilder
from src.module.a_star.base_node import BaseNode
from src.module.a_star.base_solver import BaseSolver

puzzle = Puzzle(year=2019, day=18)
inputs = puzzle.input_data


@dataclass(frozen=True)
class SolutionState:
    unlocked_keys: tuple[str, ...]

    def __lt__(self, other):
        return len(self.unlocked_keys) < len(other.unlocked_keys)


class KeyMazeNode(BaseNode):
    def __init__(self, x: int, y: int, z: int, value: str):
        super().__init__(x, y, z)

        # Persist the value of this node. It may be a key or door!
        self.value = value

        # Some special neighbours.
        self.z_neighbour: Optional["KeyMazeNode"] = None
        self.door_neighbours: list[tuple[str, "KeyMazeNode"]] = []

    def is_key(self) -> bool:
        """Is there still a key on this node?"""
        return self.value in "abcdefghijklmnopqrstuvwxyz"

    def is_door(self, state: SolutionState) -> bool:
        """Is there still a door on this node?"""
        return self.value in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and self.value.lower() not in state.unlocked_keys

    def neighbors_with_state(self, state: SolutionState) -> Generator[tuple["KeyMazeNode", int], None, None]:
        # If this node is a key and the key was not picked up, we need to go in the z direction.
        if self.is_key():
            if self.value not in state.unlocked_keys:
                yield self.z_neighbour, 0
                return

        # Return the adjacent doors, only if the key was picked up.
        for door, neighbour in self.door_neighbours:
            if not neighbour.is_door(state):
                yield neighbour, 1

        yield from super().neighbors()


class KeyMazeBuilder(BaseGraphBuilder[KeyMazeNode]):
    def __init__(self, raw_input: str):
        super().__init__(raw_input)
        self.__node_map = {}

    def count_keys(self):
        return sum(1 for char in self._raw_input if char.islower())

    def __build_layer(self, z: int):
        for row_index, row in enumerate(self._raw_input.splitlines()):
            for col_index, field in enumerate(row):
                if field != "#":
                    node = KeyMazeNode(row_index, col_index, z, field)
                    self._nodes.append(node)
                    self.__node_map[(row_index, col_index, z)] = node
                    
    def __connect_nodes(self):
        for node in self._nodes:
            # Connect the nodes in the z direction.
            z_modified_coordinate = (node.x, node.y, node.z + 1)
            if z_modified_coordinate in self.__node_map:
                node.z_neighbour = self.__node_map[z_modified_coordinate]

            # Connect the nodes in the x and y direction.
            clean_state = SolutionState(tuple())
            for x, y in [(node.x + 1, node.y), (node.x - 1, node.y), (node.x, node.y + 1), (node.x, node.y - 1)]:
                xy_modified_coordinate = (x, y, node.z)
                if xy_modified_coordinate in self.__node_map:
                    neighbour = self.__node_map[xy_modified_coordinate]
                    if neighbour.is_door(clean_state):
                        node.door_neighbours.append((neighbour.value, neighbour))
                    else:
                        node.add_neighbour(neighbour)
                    
    def _get_start(self) -> KeyMazeNode:
        for node in self._nodes:
            if node.value == "@":
                return node
        raise RuntimeError("Could not find start node")
    
    def _parse_nodes(self):
        for z in range(self.count_keys() + 1):
            self.__build_layer(z)
        self.__connect_nodes()


class KeyMazeSolver(BaseSolver[SolutionState, KeyMazeNode]):
    """Custom logic for the key maze that does not exist for the A* algorithm."""

    @staticmethod
    def get_empty_state() -> SolutionState:
        return SolutionState(tuple())

    @staticmethod
    def update_state(state: SolutionState, current_node: KeyMazeNode, new_node: KeyMazeNode) -> SolutionState:
        if new_node.is_key() and current_node.value == new_node.value:
            new_keys = state.unlocked_keys + (new_node.value,)
            return SolutionState(tuple(sorted(new_keys)))
        return state

    @staticmethod
    def get_neighbours(node_state: tuple[SolutionState, KeyMazeNode]) -> Generator[tuple[KeyMazeNode, int], None, None]:
        state, node = node_state
        yield from node.neighbors_with_state(state)

    @staticmethod
    def heuristic(node: KeyMazeNode, end: (SolutionState, KeyMazeNode)) -> float:
        return - node.z

    @staticmethod
    def is_destination(node: KeyMazeNode, end: KeyMazeNode) -> bool:
        """We consider the destination reached when we are on the same z level."""
        return node.z == end.z


# PART 1

builder = KeyMazeBuilder(inputs)
start = builder.build()
destination = KeyMazeNode(0, 0, builder.count_keys(), "!")
solver = KeyMazeSolver()
puzzle.answer_a = solver.evaluate_path_length(solver.solve(start, destination))

# PART 2

updated_inputs = inputs.splitlines()

