"""Finding the shortest path through a maze.

This is part of the reusable module (§VI), next to the generator. Given
a Maze, an entry and an exit, it returns a shortest path as cells, which
a display can mark (§V), and turns those cells into the N, E, S, W
letters of the output file (§IV.5). It prints nothing.
"""

from collections import deque
from maze.maze import Coord, Maze, MazeError, Direction


class SolveError(MazeError):
    """Raised when no path joins the entry and the exit.

    The message names the cells at fault in the ``x,y`` form of a
    configuration file, since it may be shown as it stands to whoever
    chose the entry and the exit.
    """


def shortest_path(maze: Maze, entry: Coord, exit: Coord) -> list[Coord]:
    """Return a shortest path from entry to exit through open walls.

    Parameters
    ----------
    maze:
        The maze to cross. It is not changed.
    entry, exit:
        The cells to start and end on, as ``(x, y)``, both inside the
        grid.

    Returns
    -------
    list[Coord]
        The cells of the path, entry first and exit last, each one step
        from the one before through an open wall. Its length is the
        number of steps plus one, so ``[entry]`` when entry and exit
        are the same cell.

    Raises
    ------
    SolveError
        If the entry or the exit is a cell of the "42", or if the exit
        cannot be reached from the entry.

    Notes
    -----
    A breadth-first search. Cells wait in a queue and are taken from
    its front, so they come out in order of their distance from the
    entry: every cell one step away before any cell two steps away, and
    so on. The first time the exit comes out, no shorter way to it can
    still be waiting, so the path found is a shortest one. A stack, as
    used to carve the maze, would find a path but not always the
    shortest.

    ``parent`` records, for each cell reached, the cell it was reached
    from, and so also serves as the record of cells already reached. A
    cell is recorded when it joins the queue, never again, so no cell is
    queued twice and the search ends. The path is read back from the
    exit by following those records to the entry, whose parent is None,
    and reversed.

    When several shortest paths exist, which is common in a maze with
    loops, the order of ``Maze.neighbours`` decides which one is found.
    Nothing is random, so the same maze always gives the same path.

    The "42" is checked first. Its cells have every wall closed, so a
    search from one would only report the exit unreachable, which would
    not tell anyone what to change.

    Each cell joins the queue at most once and has at most four
    neighbours, so the search takes time proportional to the number of
    cells. A ``deque`` is used because taking the first item of a
    ``list`` moves every other item.
    """
    if maze.is_reserved(entry):
        raise SolveError(
            f"the entry {entry[0]},{entry[1]} is part of the \"42\", "
            "whose cells are closed on every side"
        )
    if maze.is_reserved(exit):
        raise SolveError(
            f"the exit {exit[0]},{exit[1]} is part of the \"42\", "
            "whose cells are closed on every side"
        )
    parent: dict[Coord, Coord | None] = {entry: None}
    line: deque[Coord] = deque([entry])
    path: list[Coord] = []
    while len(line) > 0:
        cell = line.popleft()
        if cell == exit:
            trace_cell: Coord | None = cell
            while trace_cell is not None:
                path.append(trace_cell)
                trace_cell = parent[trace_cell]
            return path[::-1]
        candidates = maze.open_neighbours(cell)
        for coord in candidates:
            if coord not in parent:
                line.append(coord)
                parent[coord] = cell
    raise SolveError(
        f"the exit {exit[0]},{exit[1]} cannot be reached "
        f"from the entry {entry[0]},{entry[1]}"
    )


_LETTER_OF_STEP: dict[Coord, str] = {
    Direction.NORTH.delta: "N",
    Direction.EAST.delta: "E",
    Direction.SOUTH.delta: "S",
    Direction.WEST.delta: "W"
}


def to_directions(path: list[Coord]) -> str:
    """Turn the cells of a path into N, E, S, W letters.

    Parameters
    ----------
    path:
        Cells in order, each one step from the one before, as returned
        by ``shortest_path``.

    Returns
    -------
    str
        One letter per step, the form the last line of the output file
        takes (§IV.5). Empty for a path of a single cell or none.

    Raises
    ------
    KeyError
        If two consecutive cells are not one step apart. A path from
        ``shortest_path`` never is, so this means a bug, and it stops
        here rather than returning a string a letter short.

    Notes
    -----
    Walls play no part here: the letter depends only on how the position
    changes. The steps come from ``Direction.delta``, so ``y`` grows
    downwards and a step to a smaller ``y`` is north.
    """
    result: str = ""
    for a, b in zip(path, path[1:]):
        ax, ay = a
        bx, by = b
        result += _LETTER_OF_STEP[bx - ax, by - ay]
    return result
