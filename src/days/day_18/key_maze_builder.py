from src.days.day_18.key_maze_node import KeyMazeNode
from src.days.day_18.solution_state import SolutionState
from src.module.a_star.base_graph_builder import BaseGraphBuilder


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
            clean_state = SolutionState(tuple(), 0)
            for x, y in [
                (node.x + 1, node.y),
                (node.x - 1, node.y),
                (node.x, node.y + 1),
                (node.x, node.y - 1),
            ]:
                xy_modified_coordinate = (x, y, node.z)
                if xy_modified_coordinate in self.__node_map:
                    neighbour = self.__node_map[xy_modified_coordinate]
                    if neighbour.is_door(clean_state):
                        node.door_neighbours.append((neighbour.value, neighbour))
                    else:
                        node.add_neighbour(neighbour)

    def _get_starts(self) -> list[KeyMazeNode]:
        starts = set()
        for node in self._nodes:
            if node.value == "@" and node.z == 0:
                starts.add(node)
        return list(starts)

    def _parse_nodes(self):
        for z in range(self.count_keys() + 1):
            self.__build_layer(z)
        self.__connect_nodes()
