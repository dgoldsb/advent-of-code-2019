from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionState:
    recursion_depth: int = 0

    def __lt__(self, other):
        return self.recursion_depth < other.recursion_depth
