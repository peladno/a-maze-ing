import pytest
from maze.maze import Direction
from maze.maze import Maze
from maze.maze import _ALL_WALLS
from maze.maze import OutOfBoundsError


def test_opposite_is_symmetric() -> None:
    for d in Direction:
        assert d.opposite.opposite is d


def test_delta_and_opposite_cancel_out() -> None:
    for d in Direction:
        x, y = (0, 0)
        dx, dy = d.delta
        x += dx
        y += dy
        dx, dy = d.opposite.delta
        x += dx
        y += dy
        assert (x, y) == (0, 0)


def test_new_maze_has_given_size_and_all_walls_closed() -> None:
    m = Maze(5, 3)
    assert m.width == 5
    assert m.height == 3
    for h in range(m.height):
        for w in range(m.width):
            assert m.walls_at((w, h)) == _ALL_WALLS


def test_invalid_size_raises_value_error() -> None:
    for w, h in [(0, 3), (3, 0), (-1, 5)]:
        with pytest.raises(ValueError):
            Maze(w, h)


def test_contains_only_accepts_positions_inside_grid() -> None:
    m = Maze(5, 3)
    assert m.contains((0, 0))
    assert m.contains((4, 2))
    assert not m.contains((5, 0))
    assert not m.contains((0, 3))
    assert not m.contains((-1, 0))
    assert not m.contains((4, 3))


def test_walls_at_raises_outside_grid() -> None:
    m = Maze(5, 3)
    for w, h in [(5, 0), (0, 3), (-1, 0), (4, 3)]:
        with pytest.raises(OutOfBoundsError):
            m.walls_at((w, h))


def test_new_maze_has_no_open_wall() -> None:
    m = Maze(5, 3)
    for d in Direction:
        assert not m.is_open((1, 2), d)
