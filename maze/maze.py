from collections.abc import Iterator
from enum import IntEnum


Coord = tuple[int, int]


class Direction(IntEnum):
    """The four walls of a cell, valued as their bit in the §IV.5 encoding."""

    NORTH = 1 # bit 0
    EAST = 2  # bit 1
    SOUTH = 4 # bit 2
    WEST = 8  # bit 3

    @property
    def opposite(self) -> "Direction":
