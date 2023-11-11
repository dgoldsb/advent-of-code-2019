from typing import Generator


class BaseNode:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

        self.__neighbors = []

    def neighbors(self) -> Generator[tuple["BaseNode", int], None, None]:
        # Return the adjacent nodes.
        for neighbor in self.__neighbors:
            yield neighbor, 1

    def add_neighbor(self, neighbor: "BaseNode"):
        self.__neighbors.append(neighbor)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)
