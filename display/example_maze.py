# Bitmask directions
from maze.cell import E, N, S, W


class DummyMaze:
    """
    Maze mínimo para probar el TerminalRenderer.
    No depende del generador real.
    """

    def __init__(self) -> None:
        self.width = 4
        self.height = 4
        self.entry = (0, 0)
        self.exit = (3, 3)

        # Maze perfecto 4x4 — paredes coherentes
        self.grid = [
            # y = 0
            [E | S | W,     W | S,         S | E,         S | W],
            # y = 1
            [N | E,         N | W | S,     N | S,         N | W | S],
            # y = 2
            [E | S,         W | N,         N | E | S,     W | S],
            # y = 3
            [N | E | W,     N | W,         N | E,         N | W],
        ]

    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]
