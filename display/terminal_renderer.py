"""Terminal ASCII renderer for maze visualization."""

from __future__ import annotations

from collections.abc import Collection
from maze.maze import Coord, Direction
from .colors import ENTRY, EXIT, PATH, RESET, WALL_COLORS, PATTERN42
from .renderer import MazeLike, Renderer

N = Direction.NORTH
E = Direction.EAST
S = Direction.SOUTH
W = Direction.WEST


class TerminalRenderer(Renderer):
    """Render a maze as a fixed-width ASCII drawing in the terminal."""

    def __init__(
        self,
        show_path: bool = False,
        color_mode: int = 0,
        entry: Coord | None = None,
        exit: Coord | None = None,
        shortest_path: Collection[Coord] | None = None,
    ) -> None:
        """Create a renderer with the requested display options.

        Parameters
        ----------
        show_path:
            If ``True``, mark cells in ``shortest_path`` with ``.``.
        color_mode:
            Wall colour mode: ``0`` disables colour, while ``1`` to ``3``
            select the configured ANSI wall colours.
        entry:
            Optional ``(x, y)`` coordinates of the maze entry.
        exit:
            Optional ``(x, y)`` coordinates of the maze exit.
        shortest_path:
            Optional collection of ``(x, y)`` coordinates forming the solution
            path.

        Returns
        -------
        None
            The renderer is configured in place.
        """
        if color_mode not in range(len(WALL_COLORS)):
            raise ValueError(
                f"color_mode must be between 0 and {len(WALL_COLORS) - 1}"
            )

        self.show_path = show_path
        self.color_mode = color_mode
        self.entry = entry
        self.exit = exit
        self.shortest_path: set[Coord] | None = (
            set(shortest_path) if shortest_path is not None else None
        )

    def render(
        self,
        maze: MazeLike,
        shortest_path: Collection[Coord] | None = None,
    ) -> None:
        """Print the complete maze, including walls and cell markers.

        The wall bitmask uses ``N=1``, ``E=2``, ``S=4`` and ``W=8``;
        a set bit means that the corresponding wall is closed. The
        ``entry``, ``exit`` and ``shortest_path`` attributes configured
        on the renderer or attached to ``maze`` are used when present.

        Parameters
        ----------
        maze:
            Object providing ``width``, ``height`` and ``walls_at``.
        shortest_path:
            Optional collection of ``(x, y)`` coordinates to update
            the solution path displayed by the renderer.

        Returns
        -------
        None
            The rendered maze is written directly to standard output.
        """
        if shortest_path is not None:
            self.shortest_path = set(shortest_path)
        height = maze.height
        print(self._horizontal_wall(maze, 0, N))

        for y in range(height):
            print(self._vertical_wall(maze, y))

            print(self._horizontal_wall(maze, y, S))

    def _horizontal_wall(
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
            line += self._wall_color("+")
            line += self._wall_color("---") if cell_mask & wall else "   "
        return line + self._wall_color("+")

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
            line += self._wall_color("|") if cell_mask & W else " "
            line += self._cell_content(x, y, maze)

        last_mask = maze.walls_at((maze.width - 1, y))
        return line + (
            self._wall_color("|") if last_mask & E else " "
        )

    def _wall_color(self, text: str) -> str:
        """Apply the selected ANSI colour to a wall fragment."""
        color = WALL_COLORS[self.color_mode]
        return f"{color}{text}{RESET}" if color else text

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
        pos = (x, y)
        entry = self.entry if self.entry is not None else getattr(
            maze, "entry", None
        )
        exit_coord = self.exit if self.exit is not None else getattr(
            maze, "exit", None
        )
        path = (
            self.shortest_path
            if self.shortest_path is not None
            else getattr(maze, "shortest_path", set())
        )

        if pos == entry:
            return f"{ENTRY} E {RESET}"

        if pos == exit_coord:
            return f"{EXIT} X {RESET}"

        if self.show_path and pos in path:
            return f"{PATH} . {RESET}"

        if hasattr(maze, "is_reserved") and maze.is_reserved(pos):
            return f"{PATTERN42}███{RESET}"

        return "   "
