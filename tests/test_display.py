"""Integration and unit tests for display/terminal_renderer.py.

Verifies terminal rendering functionality, option validation, horizontal and
vertical wall formatting, cell marker placement, and standard output.
"""

from __future__ import annotations
import pytest

from typing import TYPE_CHECKING
from maze.maze import Maze
from display import TerminalRenderer, WALL_COLORS

if TYPE_CHECKING:
    from maze.maze import Coord


def test_terminal_renderer_init_valid() -> None:
    """Verify initializing TerminalRenderer with valid display options.

    Returns
    -------
    None
        Asserts that show_path and color_mode properties are set correctly.
    """
    renderer = TerminalRenderer(show_path=True, color_mode=1)
    assert renderer.show_path is True
    assert renderer.color_mode == 1


def test_terminal_renderer_init_invalid_color_mode() -> None:
    """Verify that invalid color_mode values raise a ValueError.

    Returns
    -------
    None
        Asserts that out-of-range color_mode values raise ValueError.
    """
    with pytest.raises(ValueError):
        TerminalRenderer(color_mode=-1)

    with pytest.raises(ValueError):
        TerminalRenderer(color_mode=len(WALL_COLORS))


def test_terminal_renderer_horizontal_wall() -> None:
    """Verify horizontal wall string construction for a grid row.

    Returns
    -------
    None
        Asserts the generated ASCII segment matching cell wall masks.
    """
    renderer = TerminalRenderer(color_mode=0)
    maze = Maze(width=2, height=2)

    # N wall (1) in row 0: cell 0 mask 9 (N bit set), cell 1 mask 3 (N bit set)
    wall_str = renderer._horizontal_wall(maze, y=0, wall=1)
    assert wall_str == "+---+---+"


def test_terminal_renderer_cell_content() -> None:
    """Verify cell marker formatting for entry, exit, path, and empty cells.

    Returns
    -------
    None
        Asserts presence of 'E', 'X', and '.' markers under display options.
    """
    maze = Maze(width=2, height=2)
    setattr(maze, "entry", (0, 0))
    setattr(maze, "exit", (1, 1))
    shortest_path: tuple[Coord, ...] = ((0, 0), (0, 1), (1, 1))
    setattr(maze, "shortest_path", shortest_path)

    renderer_with_path = TerminalRenderer(show_path=True, color_mode=0)
    renderer_no_path = TerminalRenderer(show_path=False, color_mode=0)

    # Entry cell
    assert "E" in renderer_with_path._cell_content(0, 0, maze)
    # Exit cell
    assert "X" in renderer_with_path._cell_content(1, 1, maze)
    # Path cell (0, 1) when show_path=True
    assert "." in renderer_with_path._cell_content(0, 1, maze)
    # Path cell (0, 1) when show_path=False
    assert "." not in renderer_no_path._cell_content(0, 1, maze)


def test_terminal_renderer_render_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify that render() prints the complete ASCII maze to stdout.

    Parameters
    ----------
    capsys:
        Pytest standard output and standard error capture fixture.

    Returns
    -------
    None
        Asserts line count and start pattern written to standard output.
    """
    renderer = TerminalRenderer(show_path=True, color_mode=0)
    maze = Maze(width=2, height=2)
    maze.open_passage((0, 0), (1, 0))

    renderer.render(maze)

    captured = capsys.readouterr()
    lines = captured.out.splitlines()

    # 2 rows -> 1 top border + 2 * (1 vertical row + 1 bottom border) = 5 lines
    assert len(lines) == 5
    assert lines[0].startswith("+")
