"""Main entry point for the A-Maze-ing maze generator application."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from display.input_handler import run_interactive_session
from display.terminal_renderer import TerminalRenderer
from maze.config import load_config, ConfigError
from maze.generator import MazeGenerator
from maze.maze import Coord, Maze, MazeError
from maze.solver import shortest_path, to_directions
from output import maze_writer


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the application.

    Parameters
    ----------
    argv:
        Optional list of argument strings (defaults to ``sys.argv[1:]``).

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments containing ``config_file``.
    """
    parser = argparse.ArgumentParser(
        description="A-Maze-ing: Maze generator, solver, and visualizer."
    )
    parser.add_argument(
        "config_file",
        type=str,
        help="Path to the maze configuration file (e.g., config.txt).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the main A-Maze-ing application pipeline.

    Parameters
    ----------
    argv:
        Optional list of command-line arguments.

    Returns
    -------
    int
        Exit status code (0 for success, non-zero for error).
    """
    args = parse_arguments(argv)
    config_path = Path(args.config_file)

    if not config_path.is_file():
        print(f"Error: Configuration file '{config_path}' not found.",
              file=sys.stderr)
        return 1

    print(f"Loading configuration from '{config_path}'...")

    try:
        config = load_config(config_path)

        maze_generator = MazeGenerator(
            width=config.width,
            height=config.height,
            perfect=config.perfect,
            seed=config.seed)

        print(f"Seed: {maze_generator.seed}")
        maze = maze_generator.generate()

        if len(maze.reserved) == 0:
            print("Warning: The '42' pattern was "
                  "omitted because the maze size is too small.",
                  file=sys.stderr)

        path_cells = shortest_path(maze, config.entry, config.exit)
        directions = to_directions(path_cells)

        maze_writer.MazeWriter.write(maze=maze,
                                     entry=config.entry,
                                     exit=config.exit,
                                     shortest_path=directions,
                                     filepath=config.output_file)

        def regenerate() -> tuple[Maze, list[Coord]]:
            generator = MazeGenerator(
                width=config.width,
                height=config.height,
                perfect=config.perfect,
                seed=None,
            )
            print(f"New seed: {generator.seed}")
            new_maze = generator.generate()
            if len(new_maze.reserved) == 0:
                print(
                    "Warning: The '42' pattern was omitted "
                    "because the maze size is too small.",
                    file=sys.stderr,
                )
            new_path = shortest_path(new_maze, config.entry, config.exit)
            new_dirs = to_directions(new_path)
            maze_writer.MazeWriter.write(
                maze=new_maze,
                entry=config.entry,
                exit=config.exit,
                shortest_path=new_dirs,
                filepath=config.output_file,
            )
            return new_maze, new_path

        renderer = TerminalRenderer(
            show_path=False,
            color_mode=0,
            entry=config.entry,
            exit=config.exit,
            shortest_path=path_cells,
        )
        run_interactive_session(renderer, maze, on_regenerate=regenerate)

    except (ConfigError, MazeError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
