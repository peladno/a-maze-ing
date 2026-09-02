"""Integration and unit tests for output/maze_writer.py.

Verifies output encoding format, hexadecimal wall bitmask conversions,
and file writing operations performed by MazeWriter.
"""

from __future__ import annotations

from pathlib import Path

from maze.maze import Maze
from output.maze_writer import MazeWriter


def test_maze_writer_encode_structure() -> None:
    """Verify that MazeWriter.encode produces correct grid and metadata.

    Returns
    -------
    None
        Asserts that line count, hex grid rows, and metadata match.
    """
    maze = Maze(width=2, height=2)
    entry = (0, 0)
    exit = (1, 1)
    path = "SE"

    encoded = MazeWriter.encode(maze, entry, exit, path)

    lines = encoded.splitlines()
    assert len(lines) == 6
    assert lines[0] == "ff"
    assert lines[1] == "ff"
    assert lines[2] == ""
    assert lines[3] == "0,0"
    assert lines[4] == "1,1"
    assert lines[5] == "SE"


def test_maze_writer_encode_hex_formatting() -> None:
    """Verify that cell wall bitmasks format as lowercase hex (0-f).

    Returns
    -------
    None
        Asserts that fully closed bitmask 15 formats as 'ff'.
    """
    maze = Maze(width=2, height=2)
    encoded = MazeWriter.encode(maze, (0, 0), (1, 1), "E")

    first_line = encoded.splitlines()[0]
    assert first_line == "ff"


def test_maze_writer_write_file(
    tmp_path: Path,
) -> None:
    """Verify that MazeWriter.write creates and writes content to disk.

    Parameters
    ----------
    tmp_path:
        Pytest temporary directory fixture for file I/O operations.

    Returns
    -------
    None
        Asserts that the file is created and contains the encoded output.
    """
    maze = Maze(width=2, height=2)
    entry = (0, 0)
    exit = (1, 1)
    path = "SE"
    target_file = tmp_path / "maze_output.txt"

    MazeWriter.write(maze, entry, exit, path, str(target_file))

    assert target_file.exists()
    content = target_file.read_text(encoding="utf-8")
    expected_content = MazeWriter.encode(maze, entry, exit, path)
    assert content == expected_content
