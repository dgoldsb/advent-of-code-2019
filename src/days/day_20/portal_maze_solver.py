from typing import Generator

from src.days.day_20.portal_maze_node import PortalMazeNode
from src.days.day_20.solution_state import SolutionState
from src.module.a_star.base_solver import BaseSolver


class PortalMazeSolver(BaseSolver[SolutionState, PortalMazeNode]):
    """Custom logic for the portal maze that does not exist for the A* algorithm."""

    def __init__(self, recursive: bool = False):
        self.__recursive = recursive

    def get_empty_states(self) -> list[SolutionState]:
        return [SolutionState()]

    def update_states(
        self,
        state: SolutionState,
        current_node: PortalMazeNode,
        new_node: PortalMazeNode,
    ) -> list[SolutionState]:
        if self.__recursive:
            new_state = SolutionState(
                state.recursion_depth + current_node.get_z_modifier(new_node)
            )
            if new_state.recursion_depth < 0:
                return []
            return [
                SolutionState(
                    state.recursion_depth + current_node.get_z_modifier(new_node)
                )
            ]
        return [state]

    @staticmethod
    def get_neighbors(
        node_state: tuple[SolutionState, PortalMazeNode]
    ) -> Generator[tuple[PortalMazeNode, int], None, None]:
        yield from node_state[1].neighbors()

    @staticmethod
    def heuristic(node: PortalMazeNode, end: (SolutionState, PortalMazeNode)) -> float:
        return 0.0

    @staticmethod
    def is_destination(
        node: tuple[SolutionState, PortalMazeNode], end: PortalMazeNode
    ) -> bool:
        """We consider the destination reached when we are on the same z level.

        This is a bit hacky, but a way for us to circumvent the fact that we don't know the destination node, just the
        destination z-level.
        """
        return node[1] == end and node[0].recursion_depth == 0
