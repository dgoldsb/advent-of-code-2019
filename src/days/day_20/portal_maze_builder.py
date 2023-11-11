from src.days.day_20.portal_maze_node import PortalMazeNode
from src.module.a_star.base_graph_builder import BaseGraphBuilder
from src.module.constants import UPPERS
from src.module.io import char_array


class PortalMazeBuilder(BaseGraphBuilder[PortalMazeNode]):
    def __init__(self, raw_input: str):
        super().__init__(raw_input)
        self.__node_map = {}
        self.__name_portal_map = {}
        self.__portals = []

    def __build_nodes(self):
        for row_index, row in enumerate(self._raw_input.splitlines()):
            for col_index, field in enumerate(row):
                if field == ".":
                    node = PortalMazeNode(row_index, col_index)
                    self._nodes.append(node)
                    self.__node_map[(row_index, col_index)] = node

    def __parse_portals(self):
        maze = char_array(self._raw_input)

        for x in range(1, len(maze) - 1):
            for y in range(1, len(maze[x]) - 1):
                try:
                    name, loc = self.__parse_portal(x, y, maze)
                    if name in self.__name_portal_map:
                        self.__portals.append((loc, self.__name_portal_map[name]))
                    else:
                        self.__name_portal_map[name] = loc
                except AssertionError:
                    pass

    def __parse_portal(self, x, y, maze):
        assert maze[x][y] in UPPERS

        triple = [None, maze[x][y], None]
        for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            up = maze[x + delta[0]][y + delta[1]]
            down = maze[x - delta[0]][y - delta[1]]

            if up in UPPERS and down == ".":
                triple[0] = up
                triple[2] = (x - delta[0], y - delta[1])
                name_list = sorted(triple[0:2])
                return "".join(name_list), triple[2]
        else:
            raise AssertionError("Not a portal")

    def __connect_nodes(self):
        for node in self._nodes:
            # Connect the nodes in the x and y direction.
            for x, y in [
                (node.x + 1, node.y),
                (node.x - 1, node.y),
                (node.x, node.y + 1),
                (node.x, node.y - 1),
            ]:
                xy_modified_coordinate = (x, y)
                if xy_modified_coordinate in self.__node_map:
                    neighbor = self.__node_map[xy_modified_coordinate]
                    node.add_neighbor(neighbor)

    def _get_starts(self) -> list[PortalMazeNode]:
        return [
            self.__node_map[self.__name_portal_map["AA"]],
            self.__node_map[self.__name_portal_map["ZZ"]],
        ]

    def __connect_portals(self):
        for portal in self.__portals:
            portal_a = self.__node_map[portal[0]]
            portal_b = self.__node_map[portal[1]]
            if portal_a == portal_b:
                continue
            portal_a.add_neighbor(portal_b)
            portal_b.add_neighbor(portal_a)

    def _parse_nodes(self):
        self.__build_nodes()
        self.__parse_portals()
        self.__connect_nodes()
        self.__connect_portals()
