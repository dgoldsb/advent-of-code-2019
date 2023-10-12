"""Pathfindiing related algorithms."""
import typing

from src.module.common_functions import manhattan


class Node:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z  # level

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"


class Portal:
    def __init__(
        self, name, a: typing.Tuple[int, int], b: typing.Tuple[int, int], recursive
    ):
        self.name = name
        self.entrance = Node(*a)
        self.exit = Node(*b)
        self.recursive = recursive

    def enter(self, a: Node):
        z_delta = 1 if self.recursive else 0

        if a.x == self.entrance.x and a.y == self.entrance.y:
            new_node = Node(self.exit.x, self.exit.y, a.z + z_delta)

            if new_node.z < 45:
                return new_node
        elif a.x == self.exit.x and a.y == self.exit.y:
            new_node = Node(self.entrance.x, self.entrance.y, a.z - z_delta)

            # Cannot go lower than the first level.
            if new_node.z >= 0:
                return new_node

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
                if node.x == x2 and node.y == y2:
                    yield Node(x2, y2, pos.z)

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
    start: typing.Tuple,
    end: typing.Tuple,
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
    start: typing,
    end: typing,
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
