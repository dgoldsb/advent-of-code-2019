"""Common functions useful in AoC puzzles."""
import math
import typing


def compute_angle(a: typing.Tuple[int, int], b: typing.Tuple[int, int]) -> float:
    """Angle in degrees, starting from the x-axis ("3 o'clock") and moving clockwise."""
    if a == b:
        raise ValueError("Cannot compute angle for identical points.")
    return (math.atan2((b[1] - a[1]), (b[0] - a[0])) * (180 / math.pi) + 90) % 360


def manhattan(x, y):
    dist = 0

    for dim in range(len(x)):
        dist += math.fabs(x[dim] - y[dim])

    return int(dist)


def path_to_root(child_parent_map: typing.Dict, child: typing.Any):
    if child in child_parent_map.keys():
        return [child] + path_to_root(child_parent_map, child_parent_map[child])
    else:
        return [child]
