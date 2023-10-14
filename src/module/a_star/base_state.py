from dataclasses import dataclass


@dataclass(frozen=True)
class BaseState:
    """State of the routing."""
