"""Temporary dummy maze implementation inheriting from the real Maze class."""

from __future__ import annotations

import os
import random
import time
from typing import Optional

from maze.maze import Coord, Maze, MazeError


class DummyMaze(Maze):
    """Dummy maze structure inheriting from the real Maze class.

    Generates random passages using ``open_passage()`` for display prototyping
    and testing while using the authoritative ``Maze`` implementation.
    """

    def __init__(
        self,
        width: int = 4,
        height: int = 4,
        reserved: frozenset[Coord] = frozenset(),
        seed: Optional[int] = None,
    ) -> None:
        """Initialize a dummy maze using the Maze base class.

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
        super().__init__(width=width, height=height, reserved=reserved)

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

        # Randomly open passages using open_passage to maintain wall coherence
        for y in range(self.height):
            for x in range(self.width):
                cell = (x, y)
                for _direction, npos in self.neighbours(cell):
                    if random.random() < 0.5:
                        try:
                            self.open_passage(cell, npos)
                        except MazeError:
                            pass

    def __repr__(self) -> str:
        """Return a string representation of the DummyMaze."""
        mode = "reproducible" if self._reproducible else "random"
        return (
            f"<DummyMaze {self.width}x{self.height} "
            f"seed={self.seed} mode={mode}>"
        )
