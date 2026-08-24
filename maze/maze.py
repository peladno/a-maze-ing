from collections.abc import Iterator
from enum import IntEnum

# (x, y) — x is the column, y is the row, origin top-left. Decision 3.2 = A.
Coord = tuple[int, int]


class Direction(IntEnum):
    """The four walls of a cell, valued as their bit in the §IV.5 encoding."""

    NORTH = 1   # bit 0
    EAST = 2    # bit 1
    SOUTH = 4   # bit 2
    WEST = 8    # bit 3

    @property
    def opposite(self) -> "Direction":
        raise NotImplementedError("Not implemented yet")

    @property
    def delta(self) -> Coord:
        raise NotImplementedError("Not implemented yet")


class MazeError(Exception):
    """Base class for every error this module raises (decision 3.9 = A)."""


class OutOfBoundsError(MazeError):
    """Raised when a coordinate is outside the maze."""


class NotAdjacentError(MazeError):
    """Raised when two cells are not orthogonally adjacent."""


class Maze:
    """A rectangular grid of cells, each stored as a 4-bit wall mask.

    Every wall starts closed. The only way to open one is open_passage().
    """

    def __init__(
        self,
        width: int,
        height: int,
        reserved: frozenset[Coord] = frozenset(),
    ) -> None: ...

    # --- shape ---------------------------------------------------------
    @property
    def width(self) -> int:
        raise NotImplementedError("Not implemented yet")

    @property
    def height(self) -> int:
        raise NotImplementedError("Not implemented yet")

    @property
    def reserved(self) -> frozenset[Coord]:
        raise NotImplementedError("Not implemented yet")

    # --- reading -------------------------------------------------------
    def contains(self, pos: Coord) -> bool:
        raise NotImplementedError("Not implemented yet")

    def is_reserved(self, pos: Coord) -> bool:
        raise NotImplementedError("Not implemented yet")

    def walls_at(self, pos: Coord) -> int:
        raise NotImplementedError("Not implemented yet")

    def is_open(self, pos: Coord, direction: Direction) -> bool:
        raise NotImplementedError("Not implemented yet")

    def neighbours(self, pos: Coord) -> Iterator[tuple[Direction, Coord]]:
        raise NotImplementedError("Not implemented yet")

    def open_neighbours(self, pos: Coord) -> Iterator[Coord]:
        raise NotImplementedError("Not implemented yet")

    def rows(self) -> Iterator[tuple[int, ...]]:
        raise NotImplementedError("Not implemented yet")

    # --- the only mutator ----------------------------------------------
    def open_passage(self, a: Coord, b: Coord) -> None:
        raise NotImplementedError("Not implemented yet")
