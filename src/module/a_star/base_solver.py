from heapq import heappush, heappop
from typing import TypeVar, Generic, Generator

from src.module.a_star.base_node import BaseNode
from src.module.a_star.base_state import BaseState

NodeType = TypeVar("NodeType", bound=BaseNode)
StateType = TypeVar("StateType", bound=BaseState)
NodeStateType = tuple[StateType, NodeType]


class BaseSolver(Generic[StateType, NodeType]):
    """Solve graph with A* algorithm."""

    @staticmethod
    def _reconstruct_path(
        node_state: NodeStateType, came_from: dict[NodeStateType, NodeStateType]
    ) -> list[NodeStateType]:
        """Reconstruct the path from the end node to the start node."""
        path = []

        # Loop until we have reached the start node.
        while node_state in came_from:
            # Add the node to the path.
            path.append(node_state)

            # Get the parent node.
            node_state = came_from[node_state]

        # Return the path.
        return path

    @staticmethod
    def evaluate_path_length(path: list[NodeStateType]) -> int:
        """Evaluate the length of the path."""
        return len(path)

    @staticmethod
    def get_neighbors(
        node_state: NodeStateType,
    ) -> Generator[tuple[NodeType, int], None, None]:
        """Get the neighbors of the current node."""
        _, node = node_state
        for neighbor in node.neighbors():
            yield neighbor, 1

    def get_empty_states(self) -> list[StateType]:
        raise NotImplementedError()

    @staticmethod
    def update_states(
        state: StateType, current_node: NodeType, new_node: NodeType
    ) -> list[StateType]:
        raise NotImplementedError()

    @staticmethod
    def heuristic(node: NodeType, end: NodeStateType) -> float:
        raise NotImplementedError

    @staticmethod
    def is_destination(node: NodeStateType, end: NodeType) -> bool:
        return node[1] == end

    def solve(self, start: NodeType, end: NodeType) -> list[NodeStateType]:
        """Solve the graph with A* algorithm."""
        # Initialize the open and closed lists.
        open_list: list[tuple[float, NodeStateType]] = []
        open_set: set[NodeStateType] = set()
        closed_set: set[NodeStateType] = set()

        # Initialize the came from, g score and f score.
        came_from: dict[NodeStateType, NodeStateType] = {}
        g_score: dict[NodeStateType, float] = {}
        f_score: dict[NodeStateType, float] = {}

        # Add the start node to the open list.
        starting_states = [(state, start) for state in self.get_empty_states()]
        for starting_state in starting_states:
            heappush(open_list, (0.0, starting_state))
            open_set.add(starting_state)
            g_score[starting_state] = 0.0
            f_score[starting_state] = 0.0

        # Loop until the open list is empty.
        while open_list:
            current_node_state = heappop(open_list)[1]
            open_set.remove(current_node_state)
            current_state, current_node = current_node_state

            # Check if we have reached the end node.
            if self.is_destination(current_node_state, end):
                return self._reconstruct_path((current_state, current_node), came_from)

            # Add the current node to the closed list.
            closed_set.add((current_state, current_node))

            # Loop through the neighbors of the current node.
            for neighbor, distance in self.get_neighbors(current_node_state):
                for neighbor_state in self.update_states(
                    current_state, current_node, neighbor
                ):
                    neighbor_node_state = (neighbor_state, neighbor)

                    # Check if the neighbor is already in the closed list.
                    if neighbor in closed_set:
                        continue

                    # Calculate the tentative g score.
                    tentative_g_score = g_score[current_node_state] + distance
                    tentative_f_score = tentative_g_score + self.heuristic(
                        neighbor, end
                    )

                    # Check if the neighbor is already in the open list.
                    if tentative_g_score >= g_score.get(
                        neighbor_node_state, float("inf")
                    ):
                        continue

                    # Update the came from and scores.
                    came_from[neighbor_node_state] = current_node_state
                    g_score[neighbor_node_state] = tentative_g_score
                    f_score[neighbor_node_state] = tentative_f_score

                    if neighbor_node_state not in open_set:
                        heappush(open_list, (tentative_f_score, neighbor_node_state))
                        open_set.add(neighbor_node_state)

        raise RuntimeError("Could not find a path")
