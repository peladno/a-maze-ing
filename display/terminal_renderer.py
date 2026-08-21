# from .colors import WALL, PATH, ENTRY, EXIT, PATTERN42, RESET
from display.example_maze import DummyMaze
from maze.cell import N, W
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
        height = maze.height
        width = maze.width

        for y in range(height):
            for x in range(width):
                cell_mask = maze.get_cell(x, y)
                print(cell_mask)

    def _north_wall(self, cell_mask: int) -> str:
        """Return the ASCII for the north wall."""
        if cell_mask & N:
            return "+─"
        else:
            return "+ "

    def _west_wall(self, cell_mask: int) -> str:
        """Return the ASCII for the west wall."""
        if cell_mask & W:
            return "│ "
        else:
            return " "

    def _cell_content(self, x: int, y: int, maze: Any) -> str:
        # Change Maze type when is available
        """Return the character inside the cell."""
        if (x, y) == maze.entry:
            return "E "

        if (x, y) == maze.exit:
            return "X "

        if self.show_path is True:
            if (x, y) in maze.shortest_path:
                return ". "
        return "  "


if __name__ == "__main__":
    maze = DummyMaze()
    renderer = TerminalRenderer()

    renderer.render(maze)
