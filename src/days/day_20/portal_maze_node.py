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

    # TODO: Neighbours communicates the z delta.
