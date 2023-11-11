from typing import Generator

from src.module.a_star.base_node import BaseNode


class PortalMazeNode(BaseNode):
    def __init__(self, x: int, y: int):
        # We persist recursion depth in the state instead of here to avoid generating too many nodes.
        super().__init__(x, y, z=0)

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)

    def __is_direct_neighbor(self, other: "PortalMazeNode") -> bool:
        return ((self.x - other.x) ** 2 == 1) or ((self.y - other.y) ** 2 == 1)

    def get_z_modifier(self, neighbor: "PortalMazeNode") -> int:
        if self.__is_direct_neighbor(neighbor):
            z_modifier = 0
        else:
            if self.x == 2:
                z_modifier = -1  # going up
            elif self.y == 2:
                z_modifier = -1  # going up
            elif neighbor.x == 2:
                z_modifier = 1  # going in
            elif neighbor.y == 2:
                z_modifier = 1  # going in
            elif max(self.x, self.y) > max(neighbor.x, neighbor.y):
                z_modifier = -1  # going up
            elif max(self.x, self.y) < max(neighbor.x, neighbor.y):
                z_modifier = 1  # going in
            else:
                raise ValueError("Could not determine z_modifier")
        return z_modifier
