from collections.abc import Iterator
from enum import IntEnum


Coord = tuple[int, int]


class Direction(IntEnum):
    """The four walls of a cell, valued as their bit in the §IV.5 encoding."""

    NORTH = 1  # bit 0
    EAST = 2   # bit 1
    SOUTH = 4  # bit 2
    WEST = 8   # bit 3

    @property
    def opposite(self) -> "Direction":
        return _OPPOSITE[self]

    @property
    def delta(self) -> Coord:
        return _DELTA[self]


_OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}

_DELTA: dict[Direction, Coord] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}
