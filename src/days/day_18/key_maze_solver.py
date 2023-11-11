from typing import Generator

from src.days.day_18.key_maze_node import KeyMazeNode
from src.days.day_18.solution_state import SolutionState
from src.module.a_star.base_solver import BaseSolver


class KeyMazeSolver(BaseSolver[SolutionState, tuple[KeyMazeNode, ...]]):
    """Custom logic for the key maze that does not exist for the A* algorithm."""

    def __init__(self, start_count: int):
        super().__init__()
        self.start_count = start_count

    def get_empty_states(self) -> list[SolutionState]:
        return [SolutionState(tuple(), i) for i in range(self.start_count)]

    @staticmethod
    def update_states(
        state: SolutionState,
        current_node: tuple[KeyMazeNode, ...],
        new_node: tuple[KeyMazeNode, ...],
    ) -> list[SolutionState]:
        for i in range(len(current_node)):
            new_node_i = new_node[i]
            current_node_i = current_node[i]
            if (
                new_node_i.is_key()
                and current_node_i.value == new_node_i.value
                and current_node_i.z != new_node_i.z
            ):
                new_keys = state.unlocked_keys + (new_node_i.value,)
                # Here we explode states, as any of the indices may be the new correct beelining index.
                return [
                    SolutionState(tuple(sorted(new_keys)), j)
                    for j in range(len(current_node))
                ]
        return [state]

    @staticmethod
    def get_neighbors(
        node_state: tuple[SolutionState, tuple[KeyMazeNode, ...]]
    ) -> Generator[tuple[tuple[KeyMazeNode, ...], int], None, None]:
        state, node_tuple = node_state

        for i, node in enumerate(node_tuple):
            # Only produce neighbors for the beelining index.
            if i != state.beelining_index:
                continue

            for neighbor in node.neighbors_with_state(state):
                node_list = []
                for j in range(len(node_tuple)):
                    if i == j:
                        node_list.append(neighbor[0])
                    else:
                        node_list.append(node_tuple[j])
                yield tuple(node_list), 1

    @staticmethod
    def heuristic(
        node: tuple[KeyMazeNode, ...],
        end: tuple[SolutionState, tuple[KeyMazeNode, ...]],
    ) -> float:
        return -sum(n.z for n in node)

    @staticmethod
    def is_destination(
        node: tuple[SolutionState, tuple[KeyMazeNode, ...]],
        end: tuple[KeyMazeNode, ...],
    ) -> bool:
        """We consider the destination reached when we are on the same z level.

        This is a bit hacky, but a way for us to circumvent the fact that we don't know the destination node, just the
        destination z-level.
        """
        return sum(n.z for n in node[1]) == end[0].z

    @staticmethod
    def evaluate_path_length(
        path: list[tuple[SolutionState, tuple[KeyMazeNode, ...]]]
    ) -> int:
        """Evaluate the length of the path."""
        return len(path) - sum(n.z for n in path[0][1])
