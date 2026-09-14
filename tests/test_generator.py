import pytest
from random import Random
from maze.generator import MazeGenerator
from maze.generator import GenerationError
from maze.maze import Maze, Direction, Coord
from maze.maze import _ALL_WALLS


def test_seed_given_is_kept() -> None:
    gen = MazeGenerator(20, 15, perfect=False, seed=42)
    assert gen.seed == 42
    gen = MazeGenerator(20, 15, perfect=False, seed=0)
    assert gen.seed == 0


def test_seed_absent_is_generated() -> None:
    gen = MazeGenerator(20, 15, perfect=False)
    assert isinstance(gen.seed, int)
    gen01 = MazeGenerator(20, 15, perfect=False)
    gen02 = MazeGenerator(20, 15, perfect=False)
    assert gen01.seed != gen02.seed


def test_options_are_keyword_only() -> None:
    with pytest.raises(TypeError):
        MazeGenerator(20, 15, True)  # type: ignore[call-arg]


def test_size_below_one_is_refused() -> None:
    with pytest.raises(GenerationError):
        MazeGenerator(0, 15, perfect=False)
    with pytest.raises(GenerationError):
        MazeGenerator(-1, -1, perfect=False)
    with pytest.raises(GenerationError):
        MazeGenerator(0, 15, perfect=True)


def test_too_small_for_default_mode() -> None:
    with pytest.raises(GenerationError):
        MazeGenerator(2, 2)
    with pytest.raises(GenerationError):
        MazeGenerator(1, 5)


def test_smallest_default_boards_are_accepted() -> None:
    MazeGenerator(3, 2)
    MazeGenerator(2, 3)


def test_single_row_is_fine_when_perfect() -> None:
    MazeGenerator(1, 5, perfect=True)


def _count_passages(m: Maze) -> int:
    n = 0
    for y in range(m.height):
        for x in range(m.width):
            if x + 1 < m.width and m.is_open((x, y), Direction.EAST):
                n += 1
            if y + 1 < m.height and m.is_open((x, y), Direction.SOUTH):
                n += 1
    return n


def _count_reachable(m: Maze) -> int:
    start = (0, 0)
    stack: list[Coord] = []
    visited: set[Coord] = set()
    stack.append(start)
    visited.add(start)
    while len(stack) > 0:
        current = stack.pop()
        for neighbour in m.open_neighbours(current):
            if neighbour not in visited:
                stack.append(neighbour)
                visited.add(neighbour)
    return len(visited)


def test_carve_opens_one_passage_fewer_than_cells() -> None:
    m = Maze(5, 3)
    gen = MazeGenerator(m.width, m.height, perfect=True)
    gen._carve_spanning_tree(m, Random(0))
    assert _count_passages(m) == m.width * m.height - 1


def test_carve_reaches_every_cell() -> None:
    m = Maze(5, 3)
    gen = MazeGenerator(m.width, m.height, perfect=True)
    gen._carve_spanning_tree(m, Random(0))
    assert _count_reachable(m) == m.width * m.height


def test_carve_same_seed_same_maze() -> None:
    m1 = Maze(5, 3)
    m2 = Maze(5, 3)
    gen = MazeGenerator(m1.width, m1.height, perfect=True)
    gen._carve_spanning_tree(m1, Random(0))
    gen = MazeGenerator(m2.width, m2.height, perfect=True)
    gen._carve_spanning_tree(m2, Random(0))
    rows1 = tuple(m1.rows())
    rows2 = tuple(m2.rows())
    assert rows1 == rows2


def test_carve_single_row() -> None:
    m = Maze(1, 5)
    gen = MazeGenerator(m.width, m.height, perfect=True)
    gen._carve_spanning_tree(m, Random(0))
    assert _count_passages(m) == m.width * m.height - 1
    assert _count_reachable(m) == m.width * m.height


def test_carve_large_maze() -> None:
    m = Maze(300, 300)
    gen = MazeGenerator(m.width, m.height, perfect=True)
    gen._carve_spanning_tree(m, Random(0))
    assert _count_reachable(m) == m.width * m.height


def test_carve_leaves_reserved_cells_closed() -> None:
    m = Maze(3, 3, reserved=frozenset({(1, 1)}))
    gen = MazeGenerator(m.width, m.height, perfect=True)
    gen._carve_spanning_tree(m, Random(0))
    walkable = m.width * m.height - len(m.reserved)
    assert _count_passages(m) == walkable - 1
    assert _count_reachable(m) == walkable
    assert m.walls_at((1, 1)) == _ALL_WALLS
