# example_maze.py
import random
import time
import os
from typing import Optional

N = 1
E = 2
S = 4
W = 8


class DummyMaze:
    """
    Maze de ejemplo compatible con la interfaz de maze.Maze.
    Ahora soporta generación aleatoria con semilla reproducible.
    """

    def __init__(
            self, width: int = 4, height: int = 4, seed: Optional[int] = None
            ) -> None:
        self.width = width
        self.height = height
        self.entry = (0, 0)
        self.exit = (width - 1, height - 1)

        # Decide la semilla
        if seed is None:
            seed = int(time.time() * 1000) ^ int.from_bytes(
                os.urandom(4), "big")
            self._reproducible = False
        else:
            self._reproducible = True

        self.seed = seed
        random.seed(self.seed)

        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                mask = 0
                if random.random() < 0.5:
                    mask |= N
                if random.random() < 0.5:
                    mask |= E
                if random.random() < 0.5:
                    mask |= S
                if random.random() < 0.5:
                    mask |= W
                # TODO uncomment for map with all the walls
                # if y == 0:
                #     mask |= N
                # if y == self.height - 1:
                #     mask |= S
                # if x == 0:
                #     mask |= W
                # if x == self.width - 1:
                #     mask |= E

                row.append(mask)
            self.grid.append(row)

    def walls_at(self, pos: tuple[int, int]) -> int:
        x, y = pos
        return self.grid[y][x]

    def rows(self) -> list[tuple[int, ...]]:
        return [tuple(row) for row in self.grid]

    def __repr__(self) -> str:
        mode = "reproducible" if self._reproducible else "random"
        return (f"<DummyMaze {self.width}x{self.height} "
                f"seed={self.seed} mode={mode}>")
