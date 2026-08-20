# from .colors import WALL, PATH, ENTRY, EXIT, PATTERN42, RESET

from typing import Any


class TerminalRenderer:
    """
    ASCII renderer for the maze.
    Uses 2x2 characters per cell.
    """

    def __init__(self, show_path: bool = False, color_mode: int = 0):
        self.show_path = show_path
        self.color_mode = color_mode

    def render(self, maze: Any) -> None:  # Change Maze type when is available
        """
        Render the maze in the terminal.
        Maze API needed:
            - maze.width
            - maze.height
            - maze.get_cell(x, y)
            - maze.entry
            - maze.exit
            - maze.shortest_path (optional)
        """
        # TODO: implement once Maze exists
        raise NotImplementedError

    def _north_wall(self, cell_mask: int) -> str:
        """Return the ASCII for the north wall."""
        # TODO: implement when bitmask is final
        return "+─"

    def _west_wall(self, cell_mask: int) -> str:
        """Return the ASCII for the west wall."""
        return "│ "

    def _cell_content(self, x: int, y: int, maze: Any) -> str:
        # Change Maze type when is available
        """Return the character inside the cell."""
        # TODO: implement when Maze exists
        return " "
