from maze.maze import Direction


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
