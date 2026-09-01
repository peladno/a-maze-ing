import pytest
from maze.maze import Direction
from maze.maze import Maze
from maze.maze import _ALL_WALLS
from maze.maze import OutOfBoundsError
from maze.maze import NotAdjacentError
from maze.maze import MazeError


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


def test_open_passage_updates_both_cells() -> None:
    for w, h, d in [
        (1, 0, Direction.NORTH),
        (2, 1, Direction.EAST),
        (1, 2, Direction.SOUTH),
        (0, 1, Direction.WEST)
    ]:
        m = Maze(5, 3)
        m.open_passage((1, 1), (w, h))
        assert m.is_open((1, 1), d)
        assert m.is_open((w, h), d.opposite)


def test_open_passage_raises_when_not_adjacent() -> None:
    m = Maze(5, 3)
    with pytest.raises(NotAdjacentError):
        m.open_passage((3, 2), (1, 1))


def test_open_passage_is_idempotent() -> None:
    m = Maze(5, 3)
    m.open_passage((1, 1), (1, 0))
    m.open_passage((1, 1), (1, 0))
    assert m.is_open((1, 1), Direction.NORTH)
    assert m.is_open((1, 0), Direction.SOUTH)


def test_open_passage_raises_outside_grid() -> None:
    m = Maze(5, 3)
    with pytest.raises(OutOfBoundsError):
        m.open_passage((5, 3), (6, 3))


def test_open_passage_refuses_reserved_cells() -> None:
    with pytest.raises(MazeError):
        m = Maze(5, 3, reserved=frozenset({(1, 1)}))
        m.open_passage((1, 0), (1, 1))


def test_neighbours_stops_at_the_edge() -> None:
    m = Maze(5, 3)
    result1 = tuple(m.neighbours((1, 1)))
    result2 = tuple(m.neighbours((0, 0)))
    assert result1 == (
        (Direction.NORTH, (1, 0)),
        (Direction.EAST, (2, 1)),
        (Direction.SOUTH, (1, 2)),
        (Direction.WEST, (0, 1))
    )
    assert result2 == (
        (Direction.EAST, (1, 0)),
        (Direction.SOUTH, (0, 1))
    )


def test_neighbours_skips_reserved_cells() -> None:
    m = Maze(5, 3, reserved=frozenset({(2, 1), (1, 2)}))
    result = tuple(m.neighbours((1, 1)))
    assert result == (
        (Direction.NORTH, (1, 0)),
        (Direction.WEST, (0, 1))
    )


def test_neighbours_raises_outside_grid() -> None:
    m = Maze(5, 3)
    with pytest.raises(OutOfBoundsError):
        list(m.neighbours((6, 4)))


def test_open_neighbours_only_returns_carved_cells() -> None:
    m = Maze(5, 3)
    before = tuple(m.open_neighbours((1, 1)))
    m.open_passage((1, 1), (1, 2))
    after = tuple(m.open_neighbours((1, 1)))
    assert before == ()
    assert after == ((1, 2), )


def test_rows_has_one_tuple_per_row() -> None:
    m = Maze(5, 3)
    rows = tuple(m.rows())
    assert len(rows) == m.height
    assert len(rows[0]) == m.width
    assert isinstance(rows[0], tuple)


def test_rows_agrees_with_walls_at() -> None:
    m = Maze(5, 3)
    m.open_passage((1, 2), (1, 1))
    m.open_passage((2, 2), (1, 2))
    rows = tuple(m.rows())
    for y in range(m.height):
        for x in range(m.width):
            assert rows[y][x] == m.walls_at((x, y))
