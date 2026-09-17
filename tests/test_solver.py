import pytest
from maze.maze import Maze, Direction, Coord
from maze.generator import MazeGenerator
from maze.solver import shortest_path, to_directions, SolveError


def _build(
    width: int,
    height: int,
    passages: list[tuple[Coord, Coord]]
) -> Maze:
    m = Maze(width, height)
    for a, b in passages:
        m.open_passage(a, b)
    return m


def _traced_maze() -> Maze:
    return _build(3, 3, [
        ((0, 0), (1, 0)),
        ((1, 0), (1, 1)),
        ((1, 1), (2, 1)),
        ((2, 1), (2, 0)),
        ((0, 0), (0, 1)),
        ((0, 1), (0, 2)),
        ((0, 2), (1, 2)),
        ((1, 2), (2, 2)),
        ((2, 2), (2, 1))
    ])


def _distance(m: Maze, start: Coord, goal: Coord) -> int:
    far = m.width * m.height
    dist = {(x, y): far for y in range(m.height) for x in range(m.width)}
    dist[start] = 0
    changed = True
    while changed:
        changed = False
        for cell in dist:
            for neighbour in m.open_neighbours(cell):
                if dist[cell] + 1 < dist[neighbour]:
                    dist[neighbour] = dist[cell] + 1
                    changed = True
    return dist[goal]


def _generated_cases() -> list[tuple[Maze, Coord, Coord]]:
    cases = []
    for perfect in (True, False):
        for width, height in ((20, 15), (9, 7)):
            for seed in range(10):
                gen = MazeGenerator(width, height, perfect=perfect, seed=seed)
                m = gen.generate()
                right = width - 1
                bottom = height - 1
                cases.append((m, (0, 0), (right, bottom)))
                cases.append((m, (right, 0), (0, bottom)))
    return cases


def test_shortest_path_of_the_traced_maze() -> None:
    m = _traced_maze()
    path = shortest_path(m, (0, 0), (2, 0))
    assert path == [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0)]


def test_path_of_a_single_cell() -> None:
    m = _traced_maze()
    assert shortest_path(m, (1, 1), (1, 1)) == [(1, 1)]
    assert to_directions([(1, 1)]) == ""
    assert to_directions([]) == ""


def test_to_directions_of_the_traced_path() -> None:
    path = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0)]
    assert to_directions(path) == "ESEN"
    assert to_directions([(1, 0), (0, 0)]) == "W"


def test_to_directions_rejects_cells_not_one_step_apart() -> None:
    with pytest.raises(KeyError):
        to_directions([(0, 0), (2, 0)])
    with pytest.raises(KeyError):
        to_directions([(0, 0), (1, 1)])


def test_path_follows_open_walls() -> None:
    step = {d.name[0]: d for d in Direction}
    for m, entry, exit in _generated_cases():
        path = shortest_path(m, entry, exit)
        letters = to_directions(path)
        assert path[0] == entry
        assert path[-1] == exit
        assert len(letters) == len(path) - 1
        x, y = entry
        for letter in letters:
            d = step[letter]
            assert m.is_open((x, y), d)
            dx, dy = d.delta
            x, y = x + dx, y + dy
        assert (x, y) == exit


def test_path_is_shortest() -> None:
    for m, entry, exit in _generated_cases():
        path = shortest_path(m, entry, exit)
        assert len(path) - 1 == _distance(m, entry, exit)


def test_same_maze_same_path() -> None:
    for m, entry, exit in _generated_cases():
        assert shortest_path(m, entry, exit) == shortest_path(m, entry, exit)


def test_reserved_entry_or_exit_raises() -> None:
    m = MazeGenerator(20, 15, seed=0).generate()
    assert m.is_reserved((8, 7))
    with pytest.raises(SolveError) as excinfo:
        shortest_path(m, (8, 7), (19, 14))
    assert "entry 8,7" in str(excinfo.value)
    assert '"42"' in str(excinfo.value)
    with pytest.raises(SolveError) as excinfo:
        shortest_path(m, (0, 0), (8, 7))
    assert "exit 8,7" in str(excinfo.value)
    assert '"42"' in str(excinfo.value)


def test_unreachable_exit_raises() -> None:
    m = _build(3, 2, [((0, 0), (1, 0)), ((0, 0), (0, 1))])
    with pytest.raises(SolveError) as excinfo:
        shortest_path(m, (0, 0), (2, 1))
    message = str(excinfo.value)
    assert "exit 2,1 cannot be reached from the entry 0,0" in message


def test_solving_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    m = _traced_maze()
    to_directions(shortest_path(m, (0, 0), (2, 0)))
    result = capsys.readouterr()
    assert result.out == ""
    assert result.err == ""
