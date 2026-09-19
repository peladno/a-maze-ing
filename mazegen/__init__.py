"""Standalone maze generation and solver package for A-Maze-ing.

This package provides a reusable generator and solver interface per
Subject Section IV/VI. It allows external applications to instantiate
a generator with custom dimensions and parameters, access the generated
cell wall bitmasks, and compute the optimal shortest path.

Examples
--------
>>> from mazegen import MazeGenerator, shortest_path, to_directions
>>> generator = MazeGenerator(width=10, height=10, perfect=False, seed=42)
>>> maze = generator.generate()
>>> path_cells = shortest_path(maze, (0, 0), (9, 9))
>>> directions = to_directions(path_cells)
"""

from __future__ import annotations

from maze.generator import GenerationError, MazeGenerator
from maze.maze import Coord, Direction, Maze, MazeError
from maze.solver import SolveError, shortest_path, to_directions

__all__ = [
    "Coord",
    "Direction",
    "GenerationError",
    "Maze",
    "MazeError",
    "MazeGenerator",
    "SolveError",
    "shortest_path",
    "to_directions",
]
