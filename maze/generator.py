"""Generating a maze: carving passages into a Maze, reproducibly.

This is the reusable part of the project (§VI). It knows nothing of
configuration files and writes nothing to the console: it is given a
size, a mode and optionally a seed, and hands back a Maze.
"""

import random
from random import Random
from maze.maze import Maze
from maze.maze import Coord
from maze.maze import Direction
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

    def generate(self) -> Maze:
        """Build and return a new maze.

        Every call starts a fresh ``Random`` from the stored seed, so
        calling this twice gives the same maze.

        Returns
        -------
        Maze
            With every walkable cell reachable. In a perfect maze there is
            exactly one path between any two cells.

        Raises
        ------
        NotImplementedError
            For a maze that is not perfect. The step that adds loops and
            removes dead ends is not written yet, and a maze without it
            is a board §IV.4 does not accept, so nothing is returned
            rather than something that looks finished.
        GenerationError
            If the reserved cells split the maze.
        """
        if not self._perfect:
            raise NotImplementedError
        maze = Maze(self._width, self._height)
        self._carve_spanning_tree(maze, Random(self.seed))
        return maze

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

        Raises
        ------
        GenerationError
            If the walk ends before reaching every walkable cell, which
            happens only when the reserved cells split the maze. The count
            comes from ``visited``, so nothing is walked a second time.

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
        walkable = maze.width * maze.height - len(maze.reserved)
        if len(visited) != walkable:
            raise GenerationError(
                'the reserved cells split the maze: '
                f'only {len(visited)} of {walkable} walkable cells '
                'can be reached from (0, 0)'
            )

    def _dead_ends(self, maze: Maze) -> list[Coord]:
        """Return the real dead ends, in row order.

        A real dead end is a cell with exactly one open passage and at
        least one closed wall facing an ordinary cell, so that opening
        that wall would give the cell a second way out. This is how
        ``maze_analyzer.py`` counts them.

        Parameters
        ----------
        maze:
            The maze to inspect. It is not changed.

        Returns
        -------
        list[Coord]
            Top row first, each row left to right. The same maze always
            gives the same list, which keeps a braid driven by it
            reproducible.

        Notes
        -----
        ``Maze.neighbours`` already leaves out positions outside the
        grid and reserved cells, so every cell it offers is an ordinary
        one. A cell with one open passage and two or more of them has a
        wall it could open. With only one, that one is its passage, and
        the cell is enclosed by the border and the "42". Enclosed dead
        ends are counted neither here nor by the analyzer, since no wall
        could remove them.

        Reserved cells have no open passage at all, so they are never
        taken for dead ends.
        """
        dead_ends: list[Coord] = []
        for y in range(maze.height):
            for x in range(maze.width):
                pos = (x, y)
                open_cells = list(maze.open_neighbours(pos))
                adjacent = list(maze.neighbours(pos))
                if len(open_cells) != 1:
                    continue
                if len(adjacent) >= 2:
                    dead_ends.append(pos)
        return dead_ends

    def _closed_walls_in(self, maze: Maze, wx: int, wy: int) -> int:
        """Count the closed walls inside a 3x3 block of cells.

        Parameters
        ----------
        maze:
            The maze to inspect. It is not changed.
        wx, wy:
            The top-left cell of the block. The whole block must lie
            inside the grid.

        Returns
        -------
        int
            From 0 to 12. Only the walls between the nine cells count;
            the walls on the block's outer edge say nothing about how
            wide the area inside it is.

        Notes
        -----
        Each internal wall is counted once, from the cell to its west or
        north: east walls on all three rows but only the left two
        columns, and south walls on all three columns but only the top
        two rows. Counting both directions on every cell of the block
        would count its outer edge as well.
        """
        n = 0
        for y in range(wy, wy + 3):
            for x in range(wx, wx + 2):
                if not maze.is_open((x, y), Direction.EAST):
                    n += 1
        for y in range(wy, wy + 2):
            for x in range(wx, wx + 3):
                if not maze.is_open((x, y), Direction.SOUTH):
                    n += 1
        return n

    def _completes_open_3x3(self, maze: Maze, a: Coord, b: Coord) -> bool:
        """Tell whether opening the wall between a and b completes a 3x3.

        Parameters
        ----------
        maze:
            The maze to inspect. It is not changed.
        a, b:
            Two adjacent cells whose shared wall is still closed.

        Returns
        -------
        bool
            True if some 3x3 block would then have all twelve of its
            internal walls open, which §IV.4 forbids: a corridor may be
            two cells wide, never three.

        Notes
        -----
        Only blocks holding both a and b can change, because only in
        those is the wall between them internal. Such a block starts at
        a column from ``max(x) - 2`` to ``min(x)`` and a row from
        ``max(y) - 2`` to ``min(y)``: six blocks whichever way the wall
        runs, so the check costs the same on any maze. Blocks reaching
        past the grid are skipped.

        Every block considered contains the wall between a and b, and
        that wall is closed. Opening it completes the block exactly when
        it is the block's only closed wall, so there is no need to check
        which wall the remaining closed one is.

        A block holding a reserved cell never completes, since every wall
        of a reserved cell stays closed.
        """
        ax, ay = a
        bx, by = b
        for wy in range(max(ay, by) - 2, min(ay, by) + 1):
            for wx in range(max(ax, bx) - 2, min(ax, bx) + 1):
                if not (
                    maze.contains((wx, wy)) and maze.contains((wx + 2, wy + 2))
                ):
                    continue
                if self._closed_walls_in(maze, wx, wy) == 1:
                    return True
        return False

    def _braid(self, maze: Maze, rng: Random) -> int:
        """Open a wall at each real dead end, and say how many were opened.

        For every real dead end, one closed wall towards an ordinary
        neighbour is chosen at random and opened, so the cell gains a
        second way out. A wall that would complete a 3x3 open area is
        never a candidate.

        Parameters
        ----------
        maze:
            The maze to braid, normally a spanning tree just carved. It
            is changed in place.
        rng:
            The source of every choice, so that the same seed braids the
            same maze.

        Returns
        -------
        int
            The number of walls opened. Starting from a spanning tree,
            which has one passage fewer than it has walkable cells, every
            wall opened adds exactly one independent loop, so this is
            also the number of loops. It can be below two on a small
            board, where one wall may fix two dead ends at once.

        Notes
        -----
        The list of dead ends is made once, and each cell in it is looked
        at once, so the loop always ends. One pass is enough: opening a
        wall only adds passages, so it never turns a cell into a dead
        end, and every dead end there will ever be is already in the
        list.

        The list does go stale, though. When a dead end is fixed by
        opening the wall to a neighbour that was also a dead end, that
        neighbour is fixed too, and it is still in the list. Its open
        passages are counted again when its turn comes, and it is skipped
        if it has more than one, rather than given a loop it does not
        need.

        A dead end whose every candidate would complete a 3x3 open area,
        which §IV.4 forbids, is left as it is. ``maze_analyzer.py``
        tolerates two real dead ends.

        Candidates keep the order ``Maze.neighbours`` yields them in, as
        in the carving, so the same seed gives the same maze.
        """
        open_count = 0
        for dead_end in self._dead_ends(maze):
            open_cells = list(maze.open_neighbours(dead_end))
            if len(open_cells) != 1:
                continue
            open_candidates = []
            for _, candidate in maze.neighbours(dead_end):
                if candidate in open_cells:
                    continue
                if not self._completes_open_3x3(maze, dead_end, candidate):
                    open_candidates.append(candidate)
            if len(open_candidates) >= 1:
                maze.open_passage(dead_end, rng.choice(open_candidates))
                open_count += 1
        return open_count
