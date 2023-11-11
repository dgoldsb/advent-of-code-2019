from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionState:
    recursion_depth: int = 0
