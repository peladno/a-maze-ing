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
        """Return the same wall seen from the neighbouring cell.

        Returns
        -------
        Direction
            The direction facing back. Opening a wall on one side must
            clear this one on the other, which is what keeps the two
            records of a shared wall in agreement (§IV.4).
        """
        return _OPPOSITE[self]

    @property
    def delta(self) -> Coord:
        """Return the (x, y) change of stepping one cell this way.

        Returns
        -------
        Coord
            An offset to add to a position, not a position itself.
            ``y`` grows downwards, so NORTH is ``(0, -1)``.
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

        Parameters
        ----------
        width:
            Number of columns.
        height:
            Number of rows.
        reserved:
            Cells that spell the "42" pattern (§IV.4). Nothing ever
            carves them, so they keep all four walls and show up as a
            solid block.

        Raises
        ------
        ValueError
            If ``width`` or ``height`` is below 1.
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
        """Return the number of columns.

        Returns
        -------
        int
            Read-only: the grid is sized once, at construction.
        """
        return self._width

    @property
    def height(self) -> int:
        """Return the number of rows.

        Returns
        -------
        int
            Read-only: the grid is sized once, at construction.
        """
        return self._height

    @property
    def reserved(self) -> frozenset[Coord]:
        """Return the cells reserved for the "42" pattern.

        Returns
        -------
        frozenset[Coord]
            Fixed at construction. Immutable, so a caller cannot grow
            or shrink the pattern after the fact.
        """
        return self._reserved

    def contains(self, pos: Coord) -> bool:
        """Return whether pos is inside the grid.

        Parameters
        ----------
        pos:
            Position to test, as ``(x, y)``.

        Returns
        -------
        bool
            True when both coordinates are within the grid.

        Notes
        -----
        Every accessor guards with this first. Python reads a negative
        index from the end of a list, so an unchecked ``(-1, 0)`` would
        quietly return a real cell instead of failing.
        """
        x, y = pos
        return (0 <= x < self.width and 0 <= y < self.height)

    def is_reserved(self, pos: Coord) -> bool:
        """Return whether this cell is part of the "42" pattern.

        Parameters
        ----------
        pos:
            Position to test, as ``(x, y)``.

        Returns
        -------
        bool
            True when the cell is reserved and must never be carved.

        Notes
        -----
        A position outside the grid simply answers False rather than
        raising. Unlike ``walls_at``, a set lookup cannot return the
        wrong cell, so there is nothing here to guard against.
        """
        return pos in self.reserved

    def walls_at(self, pos: Coord) -> int:
        """Return the 4-bit wall mask of the cell at pos.

        Parameters
        ----------
        pos:
            Position of the cell, as ``(x, y)``.

        Returns
        -------
        int
            A mask in ``0``–``15`` where a **set bit means the wall is
            closed**, so a fresh cell reads 15. This integer is exactly
            the hexadecimal digit written to the output file (§IV.5) —
            the encoder formats it, it does not translate it.

        Raises
        ------
        OutOfBoundsError
            If ``pos`` is outside the grid.
        """
        if not self.contains(pos):
            raise OutOfBoundsError(f"position is outside the grid: {pos}")
        x, y = pos
        return self._grid[y][x]

    def is_open(self, pos: Coord, direction: Direction) -> bool:
        """Return whether the wall on that side of pos is open.

        Parameters
        ----------
        pos:
            Position of the cell, as ``(x, y)``.
        direction:
            Which of the four walls to inspect.

        Returns
        -------
        bool
            True when that wall is open, so the neighbour on that side
            can be walked to.

        Raises
        ------
        OutOfBoundsError
            If ``pos`` is outside the grid. Raised through ``walls_at``,
            which is why this method has no bounds check of its own.

        Notes
        -----
        Asks the same question as ``walls_at`` without the caller having
        to touch bits.
        """
        mask = self.walls_at(pos)
        return ((mask & direction) == 0)

    def open_passage(self, a: Coord, b: Coord) -> None:
        """Open the wall between two orthogonally adjacent cells.

        Parameters
        ----------
        a:
            One of the two cells, as ``(x, y)``.
        b:
            The other cell, which must be its neighbour to the north,
            east, south or west.

        Raises
        ------
        OutOfBoundsError
            If either position is outside the grid.
        NotAdjacentError
            If the two positions are equal, diagonal, or further apart
            than one step.
        MazeError
            If either cell belongs to the reserved "42" pattern, which
            must stay fully closed (§IV.4).

        Notes
        -----
        **This is the only operation that changes a wall.** A wall is
        recorded twice — once on each side — and §IV.4 requires the two
        records to agree, so both cells are updated here or neither is.
        Nothing else in the class writes to the grid, which is what makes
        an inconsistent maze impossible rather than merely unlikely.

        Calling it twice on the same pair is harmless: clearing a bit
        that is already clear leaves the mask unchanged.
        """
        if not self.contains(a):
            raise OutOfBoundsError(f"a is outside the grid: {a}")
        if not self.contains(b):
            raise OutOfBoundsError(f"b is outside the grid: {b}")
        if a == b:
            raise NotAdjacentError(f"a and b are the same cell: {a}")
        if self.is_reserved(a):
            raise MazeError(f'a is reserved for the "42" pattern: {a}')
        if self.is_reserved(b):
            raise MazeError(f'b is reserved for the "42" pattern: {b}')
        ax, ay = a
        bx, by = b
        for d in Direction:
            if (bx - ax, by - ay) == d.delta:
                self._grid[ay][ax] = self._grid[ay][ax] & ~d
                oppo_d = d.opposite
                self._grid[by][bx] = self._grid[by][bx] & ~oppo_d
                return
        raise NotAdjacentError(f"{a} and {b} are not orthogonally adjacent")
