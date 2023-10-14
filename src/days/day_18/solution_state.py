from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionState:
    unlocked_keys: tuple[str, ...]
    # We need to let one robot "beeline" to a key at the time, no other may move.
    # This prevents the search space from exploding.
    beelining_index: int

    def __lt__(self, other):
        return len(self.unlocked_keys) < len(other.unlocked_keys)
