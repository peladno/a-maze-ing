from __future__ import annotations
from .renderer import Renderer

from typing import Protocol

from .example_maze import N, W, S, E


class MazeLike(Protocol):
    """Minimum maze interface required by :class:`TerminalRenderer`."""

    width: int
    height: int

    def walls_at(self, pos: tuple[int, int]) -> int:
        """Return the wall bitmask for the cell at ``(x, y)``."""
        ...


class TerminalRenderer(Renderer):
    """Render a maze as a fixed-width ASCII drawing in the terminal."""

    def __init__(self, show_path: bool = False, color_mode: int = 0):
        """Create a renderer with the requested display options.

        Parameters
        ----------
        show_path:
            If ``True``, mark cells in ``maze.shortest_path`` with ``.``.
        color_mode:
            Reserved for selecting wall colours in a future implementation.

        Returns
        -------
        None
            The renderer is configured in place.
        """
        self.show_path = show_path
        self.color_mode = color_mode

    def render(self, maze: MazeLike) -> None:
        """Print the complete maze, including walls and cell markers.

        The wall bitmask uses ``N=1``, ``E=2``, ``S=4`` and ``W=8``;
        a set bit means that the corresponding wall is closed. The optional
        ``entry``, ``exit`` and ``shortest_path`` attributes are used when
        present, but are not required by the maze interface.

        Parameters
        ----------
        maze:
            Object providing ``width``, ``height`` and ``walls_at``.

        Returns
        -------
        None
            The rendered maze is written directly to standard output.
        """
        height = maze.height
        print(self._horizontall_wall(maze, 0, N))

        for y in range(height):
            print(self._vertical_wall(maze, y))

            print(self._horizontall_wall(maze, y, S))

    def _horizontall_wall(
        self, maze: MazeLike, y: int, wall: int
    ) -> str:
        """Build one horizontal border for a maze row.

        Parameters
        ----------
        maze:
            Maze whose cells provide the wall masks.
        y:
            Row index to inspect.
        wall:
            Wall bit to inspect, normally ``N`` or ``S``.

        Returns
        -------
        str
            A border string with one three-character segment per cell and a
            corner at each end.
        """
        line = ""
        for x in range(maze.width):
            cell_mask = maze.walls_at((x, y))
            line += "+---" if cell_mask & wall else "+   "
        return line + "+"

    def _vertical_wall(self, maze: MazeLike, y: int) -> str:
        """Build one row containing cell contents and vertical walls.

        Parameters
        ----------
        maze:
            Maze whose cells should be rendered.
        y:
            Row index to render.

        Returns
        -------
        str
            A fixed-width line containing west/east walls and cell markers.
        """
        line = ""
        for x in range(maze.width):
            cell_mask = maze.walls_at((x, y))
            line += "|" if cell_mask & W else " "
            line += self._cell_content(x, y, maze)

        last_mask = maze.walls_at((maze.width - 1, y))
        return line + ("|" if last_mask & E else " ")

    def _cell_content(self, x: int, y: int, maze: MazeLike) -> str:
        """Return the marker displayed inside one cell.

        Parameters
        ----------
        x, y:
            Coordinates of the cell to inspect.
        maze:
            Maze that may provide ``entry``, ``exit`` and ``shortest_path``.

        Returns
        -------
        str
            A three-character cell marker: ``E`` for entry, ``X`` for exit,
            ``.`` for a visible path cell, or spaces for an empty cell.
        """
        if (x, y) == getattr(maze, "entry", None):
            return " E "

        if (x, y) == getattr(maze, "exit", None):
            return " X "

        if self.show_path and (x, y) in getattr(maze, "shortest_path", ()):
            return " . "
        return "   "


if __name__ == "__main__":
    from .example_maze import DummyMaze

    TerminalRenderer().render(DummyMaze())
