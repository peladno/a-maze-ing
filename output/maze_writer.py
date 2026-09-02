"""Module for serializing maze structures and metadata to file."""

from __future__ import annotations

from typing import TYPE_CHECKING

from display.renderer import MazeLike

if TYPE_CHECKING:
    from maze.maze import Coord


class MazeWriter:
    """Encodes and writes a maze to an output file in hexadecimal format."""

    @staticmethod
    def write(
        maze: MazeLike,
        entry: Coord,
        exit: Coord,
        shortest_path: str,
        filepath: str,
    ) -> None:
        """Write the encoded maze grid and metadata to a file.

        Parameters
        ----------
        maze:
            Maze object providing ``width``, ``height``, and ``walls_at``.
        entry:
            Coordinates ``(x, y)`` of the entry cell.
        exit:
            Coordinates ``(x, y)`` of the exit cell.
        shortest_path:
            String representing the path direction sequence (e.g., ``"ESSS"``).
        filepath:
            Destination file path where the output will be saved.

        Returns
        -------
        None
            The encoded text is written directly to the file at ``filepath``.
        """
        content = MazeWriter.encode(maze, entry, exit, shortest_path)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def encode(
        maze: MazeLike,
        entry: Coord,
        exit: Coord,
        shortest_path: str,
    ) -> str:
        """Return the formatted string representation of the maze and metadata.

        The grid portion consists of hexadecimal wall masks for each cell,
        row by row. The metadata portion contains entry coordinates, exit
        coordinates, and the shortest path string.

        Parameters
        ----------
        maze:
            Maze object providing ``width``, ``height``, and ``walls_at``.
        entry:
            Coordinates ``(x, y)`` of the entry cell.
        exit:
            Coordinates ``(x, y)`` of the exit cell.
        shortest_path:
            String representing the path direction sequence (e.g., ``"ESSS"``).

        Returns
        -------
        str
            The complete encoded output text ready for writing to file.
        """
        height = maze.height
        width = maze.width

        grid_lines = []

        for y in range(height):
            row_chars = ""
            for x in range(width):
                mask = maze.walls_at((x, y))
                row_chars += f"{mask:x}"

            grid_lines.append(row_chars)

        grid_part = "\n".join(grid_lines) + "\n"
        metadata_part = (
            f"\n{entry[0]},{entry[1]}\n{exit[0]},{exit[1]}\n{shortest_path}\n"
        )

        return grid_part + metadata_part


# if __name__ == "__main__":
#     from display.example_maze import DummyMaze

#     dummy_maze = DummyMaze(width=4, height=4, seed=42)

#     output_text = MazeWriter.encode(
#         maze=dummy_maze,
#         entry=(0, 0),
#         exit=(3, 3),
#         shortest_path="ESSS",
#     )

#     print("--- Result encode() ---")
#     print(output_text)
#     print("------------------------------------")

#     MazeWriter.write(
#         maze=dummy_maze,
#         entry=(0, 0),
#         exit=(3, 3),
#         shortest_path="ESSS",
#         filepath="test_output.txt",
#     )
#     print("File 'test_output.txt' successfully generated.")
