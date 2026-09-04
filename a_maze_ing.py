"""Main entry point for the A-Maze-ing maze generator application."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


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

    # TODO (Partner side A):
    # 1. config = load_config(config_path)
    # 2. maze = generate_maze(config)
    # 3. shortest_path = solve_maze(maze, config.entry, config.exit)

    # TODO (Integrated pipeline):
    # 4. MazeWriter.write(maze, config.entry, config.exit,
    #                     shortest_path, config.output_file)
    # 5. renderer = TerminalRenderer(show_path=False, color_mode=0)
    # 6. run_interactive_session(renderer, maze)

    return 0


if __name__ == "__main__":
    sys.exit(main())
