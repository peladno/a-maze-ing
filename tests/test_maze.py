import pytest
from maze.maze import Direction
from maze.maze import Maze
from maze.maze import _ALL_WALLS


def test_opposite_is_symmetric() -> None:
    for d in Direction:
        assert d.opposite.opposite is d


def test_delta() -> None:
    for d in Direction:
        x, y = (0, 0)
        dx, dy = d.delta
        x += dx
        y += dy
        dx, dy = d.opposite.delta
        x += dx
        y += dy
        assert (x, y) == (0, 0)


def test_init() -> None:
    m = Maze(5, 3)
    assert m.width == 5
    assert m.height == 3
    for h in range(m.height):
        for w in range(m.width):
            assert m._grid[h][w] == _ALL_WALLS


def test_valueerror() -> None:
    for w, h in [(0, 3), (3, 0), (-1, 5)]:
        with pytest.raises(ValueError):
            Maze(w, h)
