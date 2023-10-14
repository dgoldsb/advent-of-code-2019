from typing import Generator, Optional

from src.days.day_18.solution_state import SolutionState
from src.module.a_star.base_node import BaseNode


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
