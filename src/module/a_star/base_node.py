from typing import Generator


class BaseNode:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

        self.__neighbours = []

    def neighbors(self) -> Generator[tuple["BaseNode", int], None, None]:
        # Return the adjacent nodes.
        for neighbour in self.__neighbours:
            yield neighbour, 1

    def add_neighbour(self, neighbour: "BaseNode"):
        self.__neighbours.append(neighbour)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)
