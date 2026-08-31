"""Temporary dummy maze implementation for display prototyping and testing."""

from __future__ import annotations

from collections.abc import Iterator
import os
import random
import time
from typing import Optional

from maze.maze import Coord

N = 1
E = 2
S = 4
W = 8


class DummyMaze:
    """Temporary dummy maze structure compatible with the Maze interface.

    Generates random cell wall bitmasks for display prototyping while the
    real Maze generator is under implementation.
    """

    def __init__(
        self,
        width: int = 4,
        height: int = 4,
        reserved: frozenset[Coord] = frozenset(),
        seed: Optional[int] = None,
    ) -> None:
        """Initialize a dummy maze with random wall bitmasks.

        Parameters
        ----------
        width:
            Grid width in cells.
        height:
            Grid height in cells.
        reserved:
            Set of reserved cell coordinates.
        seed:
            Optional seed for random generation.
        """
        self._width = width
        self._height = height
        self._reserved = reserved
        self.entry = (0, 0)
        self.exit = (width - 1, height - 1)

        if seed is None:
            seed = int(time.time() * 1000) ^ int.from_bytes(
                os.urandom(4), "big"
            )
            self._reproducible = False
        else:
            self._reproducible = True

        self.seed = seed
        random.seed(self.seed)

        self.grid: list[list[int]] = []
        for y in range(self._height):
            row: list[int] = []
            for x in range(self._width):
                mask = 0
                if random.random() < 0.5:
                    mask |= N
                if random.random() < 0.5:
                    mask |= E
                if random.random() < 0.5:
                    mask |= S
                if random.random() < 0.5:
                    mask |= W
                row.append(mask)
            self.grid.append(row)

    @property
    def width(self) -> int:
        """Return the maze width in cells."""
        return self._width

    @property
    def height(self) -> int:
        """Return the maze height in cells."""
        return self._height

    @property
    def reserved(self) -> frozenset[Coord]:
        """Return the set of reserved cell coordinates."""
        return self._reserved

    def contains(self, pos: Coord) -> bool:
        """Check whether coordinate pos is within grid bounds."""
        x, y = pos
        return 0 <= x < self._width and 0 <= y < self._height

    def is_reserved(self, pos: Coord) -> bool:
        """Check whether coordinate pos is reserved."""
        return pos in self._reserved

    def walls_at(self, pos: Coord) -> int:
        """Return the 4-bit wall bitmask at coordinate pos."""
        x, y = pos
        return self.grid[y][x]

    def rows(self) -> Iterator[tuple[int, ...]]:
        """Yield rows of cell wall bitmasks."""
        for row in self.grid:
            yield tuple(row)

    def __repr__(self) -> str:
        """Return a string representation of the DummyMaze."""
        mode = "reproducible" if self._reproducible else "random"
        return (
            f"<DummyMaze {self._width}x{self._height} "
            f"seed={self.seed} mode={mode}>"
        )
