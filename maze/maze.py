"""The maze grid: cells, their walls, and the operation that opens them.

Each cell is stored as a 4-bit mask following subject §IV.5: bit 0 is
North, 1 is East, 2 is South, 3 is West, and a set bit means the wall is
closed.
"""

from collections.abc import Iterator
from enum import IntEnum


# (x, y): x is the column, y is the row, origin top-left (decision 3.2).
Coord = tuple[int, int]


class Direction(IntEnum):
    """The four walls of a cell, valued as their bit in the §IV.5 encoding."""

    NORTH = 1  # bit 0
    EAST = 2   # bit 1
    SOUTH = 4  # bit 2
    WEST = 8   # bit 3

    @property
    def opposite(self) -> "Direction":
        """Return the same wall seen from the neighbouring cell."""
        return _OPPOSITE[self]

    @property
    def delta(self) -> Coord:
        """Return the (x, y) change of stepping one cell this way.

        y grows downwards, so NORTH is (0, -1). This is an offset to add
        to a position, not a position itself.
        """
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

_ALL_WALLS = 15


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        reserved: frozenset[Coord] = frozenset()
    ) -> None:
        if width < 1 or height < 1:
            raise ValueError(
                'width or height below 1: '
                f'width = {width}, height = {height}'
                )
        grid = [[_ALL_WALLS] * width for _ in range(height)]
        self._grid = grid
        self._width = width
        self._height = height
        self._reserved = reserved

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def reserved(self) -> frozenset[Coord]:
        return self._reserved
