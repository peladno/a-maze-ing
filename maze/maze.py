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


class MazeError(Exception):
    """Base class for every error this module raises."""


class OutOfBoundsError(MazeError):
    """Raised when a coordinate is outside the grid."""


class NotAdjacentError(MazeError):
    """Raised when two cells asked to share a wall are not neighbours."""


# Every wall closed: NORTH | EAST | SOUTH | WEST. A cell starts here.
_ALL_WALLS = (
    Direction.NORTH
    | Direction.EAST
    | Direction.SOUTH
    | Direction.WEST
    )


class Maze:
    """A rectangular grid of cells, each held as a 4-bit wall mask.

    Every wall starts closed. open_passage is the only operation that
    opens one, and it updates both neighbouring cells, so the two
    records of a shared wall cannot disagree (§IV.4).
    """

    def __init__(
        self,
        width: int,
        height: int,
        reserved: frozenset[Coord] = frozenset()
    ) -> None:
        """Create a maze of the given size with every wall closed.

        reserved holds the cells that spell "42" (§IV.4). Nothing ever
        carves them, so they keep all four walls and show up as a solid
        block.
        """
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
        """Return the number of columns."""
        return self._width

    @property
    def height(self) -> int:
        """Return the number of rows."""
        return self._height

    @property
    def reserved(self) -> frozenset[Coord]:
        """Return the cells reserved for the "42" pattern."""
        return self._reserved

    def contains(self, pos: Coord) -> bool:
        """Return whether pos is inside the grid.

        Accessors guard with this first: Python reads a negative index
        from the end of a list, so an unchecked (-1, 0) would quietly
        return a real cell instead of failing.
        """
        x, y = pos
        return (0 <= x < self.width and 0 <= y < self.height)

    def is_reserved(self, pos: Coord) -> bool:
        """Return whether this cell is part of the "42" pattern.

        A position outside the grid simply answers False. Unlike
        walls_at, a set lookup cannot return the wrong cell, so there is
        nothing here to guard against.
        """
        return pos in self.reserved

    def walls_at(self, pos: Coord) -> int:
        """Return the 4-bit wall mask of the cell at pos.

        A set bit means the wall is closed, so a fresh cell reads 15.
        This integer is exactly the hexadecimal digit W13 writes to the
        output file (§IV.5). Raises OutOfBoundsError for a position
        outside the grid.
        """
        if not self.contains(pos):
            raise OutOfBoundsError("The position is out of bounds.")
        x, y = pos
        return self._grid[y][x]

    def is_open(self, pos: Coord, direction: Direction) -> bool:
        """Return whether the wall on that side of pos is open.

        Asks the same question as walls_at without the caller touching
        bits. Raises OutOfBoundsError, through walls_at, for a position
        outside the grid.
        """
        mask = self.walls_at(pos)
        return ((mask & direction) == 0)
