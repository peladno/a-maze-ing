"""Generating a maze: carving passages into a Maze, reproducibly.

This is the reusable part of the project (§VI). It knows nothing of
configuration files and writes nothing to the console: it is given a
size, a mode and optionally a seed, and hands back a Maze.
"""

import random
from random import Random
from maze.maze import Maze
from maze.maze import Coord
from maze.maze import MazeError


class GenerationError(MazeError):
    """Raised when the requested maze cannot be built.

    The message names the size that was refused and what would be
    accepted, since it may be shown as it stands to whoever asked.
    """


class MazeGenerator:
    """Build a maze from a size, a mode and a seed.

    This is the reusable class §VI requires. The seed in use is always
    readable from ``seed``, so whoever asked for a maze can show it and
    build the same one again.
    """

    def __init__(
        self,
        width: int,
        height: int,
        *,
        perfect: bool = False,
        seed: int | None = None
    ) -> None:
        """Store the request, refusing one no valid maze can satisfy.

        Nothing is built here; that is left to ``generate``.

        Parameters
        ----------
        width, height:
            The size, in cells.
        perfect:
            True for a perfect maze, with exactly one path between any
            two cells. False, the default, for a board with at least two
            independent loops, which is what §IV.4 asks for by default.
        seed:
            The seed to reproduce, or None to have one chosen. Either
            way, the seed in use can be read back from ``seed``.

        Raises
        ------
        GenerationError
            If width or height is below 1, or if a maze that is not
            perfect has no room for two loops.

        Notes
        -----
        A width by height board holds at most
        ``(width - 1) * (height - 1)`` independent loops, one for each
        2x2 block of cells. A maze that is not perfect needs two, so the
        smallest such boards are 3x2 and 2x3. The size is checked first
        on its own, because a negative width and height have a positive
        product and would otherwise pass.

        The rule is checked here and not again when a configuration file
        is read: it is about loops, which is this class's concern, and a
        second copy of it could drift from the first.

        When no seed is given, one is drawn once from the ``random``
        module and kept. That shared generator is used for this single
        draw only; the maze never depends on it, so the kept value is
        all it takes to build the same maze again. The range, 0 to
        2**32, keeps the seed short enough to copy into a configuration
        file.

        Only the seed is stored, not a ``Random`` made from it, so that
        every maze starts from a fresh ``Random`` and asking twice gives
        the same maze.
        """
        if width < 1 or height < 1:
            raise GenerationError(
                'width and height must both be at least 1, '
                f'got {width}x{height}'
            )
        if perfect is False:
            if (width - 1) * (height - 1) < 2:
                raise GenerationError(
                    'a maze that is not perfect needs room for two loops: '
                    f'at least 3x2 or 2x3, got {width}x{height}'
                )
        self._width = width
        self._height = height
        self._perfect = perfect
        if seed is None:
            self._seed = random.randrange(2**32)
        else:
            self._seed = seed

    @property
    def seed(self) -> int:
        """The seed in use, whether it was given or chosen.

        Returns
        -------
        int
            Giving it back as ``seed`` builds the same maze again. Showing
            it is the caller's decision; this class prints nothing.
        """
        return self._seed

    def _carve_spanning_tree(self, maze: Maze, rng: Random) -> None:
        """Carve a spanning tree: every walkable cell joined, no loop.

        The recursive backtracker, written with an explicit stack. From
        the cell on top of the stack, a neighbour not yet visited is
        chosen at random, the wall between them is opened, and the
        neighbour is pushed. When no such neighbour is left, the cell is
        popped and the walk steps back.

        Parameters
        ----------
        maze:
            A maze with every wall closed. It is changed in place.
        rng:
            The source of every choice, so that the same seed carves the
            same maze.

        Notes
        -----
        The walk starts at ``(0, 0)``, which always exists and is never
        reserved: the "42" must leave the corners free. Where it starts
        changes the shape of the maze but not its correctness, since a
        spanning tree reaches every walkable cell from anywhere, as long
        as those cells are connected.

        No loop can form. A wall is opened only towards a cell that has
        not been visited, and so is not yet joined to the rest; joining
        two cells that already are is exactly what would close a loop.
        One wall is therefore opened per walkable cell after the first.
        Reserved cells are never offered by ``Maze.neighbours``, so they
        are never entered.

        The loop ends, in time proportional to the number of cells. A
        cell is pushed only if it is not in ``visited``, and it enters
        ``visited`` in the same step; nothing ever leaves ``visited``.
        Each cell is therefore pushed at most once and popped at most
        once, and every pass through the loop does one or the other.
        ``visited`` is a set so that asking about it does not slow down
        as it grows.

        Candidates are kept in the order ``Maze.neighbours`` yields them.
        Choosing from a collection whose order could vary would let the
        same seed carve a different maze.

        The explicit stack replaces recursion, whose depth would reach
        one call per cell and stop at Python's limit of about 1000.
        """
        start = (0, 0)
        stack: list[Coord] = []
        visited: set[Coord] = set()
        stack.append(start)
        visited.add(start)
        while len(stack) > 0:
            current = stack[-1]
            candidates = []
            for _, neighbour in maze.neighbours(current):
                if neighbour not in visited:
                    candidates.append(neighbour)
            if len(candidates) == 0:
                stack.pop()
                continue
            chosen = rng.choice(candidates)
            maze.open_passage(current, chosen)
            stack.append(chosen)
            visited.add(chosen)
