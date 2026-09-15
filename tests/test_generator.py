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


def test_generate_returns_a_perfect_maze() -> None:
    gen = MazeGenerator(5, 3, perfect=True)
    m = gen.generate()
    assert _count_passages(m) == m.width * m.height - 1
    assert _count_reachable(m) == m.width * m.height


def test_generate_twice_gives_the_same_maze() -> None:
    gen = MazeGenerator(5, 3, perfect=True)
    m1 = gen.generate()
    m2 = gen.generate()
    rows1 = tuple(m1.rows())
    rows2 = tuple(m2.rows())
    assert rows1 == rows2


def test_generate_default_mode_is_playable() -> None:
    for seed in range(20):
        gen = MazeGenerator(20, 15, seed=seed)
        m = gen.generate()
        walkable = m.width * m.height
        assert _count_reachable(m) == walkable
        assert _count_passages(m) - (walkable - 1) >= 2
        assert len(gen._dead_ends(m)) <= 2


def test_generate_default_mode_has_no_3x3_open_area() -> None:
    for seed in range(20):
        gen = MazeGenerator(20, 15, seed=seed)
        m = gen.generate()
        for y in range(m.height - 2):
            for x in range(m.width - 2):
                assert gen._closed_walls_in(m, x, y) >= 1


def test_generate_smallest_boards_have_two_loops() -> None:
    for width, height in ((3, 2), (2, 3)):
        for seed in range(50):
            gen = MazeGenerator(width, height, seed=seed)
            m = gen.generate()
            walkable = m.width * m.height
            assert _count_reachable(m) == walkable
            assert _count_passages(m) - (walkable - 1) == 2


def test_generate_default_mode_same_seed_same_maze() -> None:
    gen1 = MazeGenerator(20, 15, seed=7)
    gen2 = MazeGenerator(20, 15, seed=7)
    rows1 = tuple(gen1.generate().rows())
    assert tuple(gen1.generate().rows()) == rows1
    assert tuple(gen2.generate().rows()) == rows1


def test_carve_detects_a_split_maze() -> None:
    m = Maze(3, 3, reserved=frozenset({(0, 1), (1, 1), (2, 1)}))
    gen = MazeGenerator(m.width, m.height, perfect=True)
    with pytest.raises(GenerationError) as excinfo:
        gen._carve_spanning_tree(m, Random(0))
    assert "only 3 of 6" in str(excinfo.value)


def test_generate_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    gen = MazeGenerator(5, 3, perfect=True, seed=0)
    gen.generate()
    result = capsys.readouterr()
    assert result.out == ""
    assert result.err == ""


def test_dead_ends_of_a_tree() -> None:
    m = Maze(3, 3)
    gen = MazeGenerator(m.width, m.height, perfect=True)
    tree = [
        ((0, 0), (0, 1)),
        ((0, 1), (1, 1)),
        ((1, 1), (1, 2)),
        ((1, 2), (0, 2)),
        ((1, 2), (2, 2)),
        ((2, 2), (2, 1)),
        ((2, 1), (2, 0)),
        ((2, 0), (1, 0))
    ]
    for a, b in tree:
        m.open_passage(a, b)
    assert gen._dead_ends(m) == [(0, 0), (1, 0), (0, 2)]


def test_dead_end_facing_only_reserved_is_not_counted() -> None:
    m = Maze(3, 3, reserved=frozenset({(1, 0)}))
    gen = MazeGenerator(m.width, m.height, perfect=True)
    tree = [
        ((0, 0), (0, 1)),
        ((0, 1), (1, 1)),
        ((1, 1), (2, 1)),
        ((2, 1), (2, 0)),
        ((1, 1), (1, 2)),
        ((1, 2), (0, 2)),
        ((1, 2), (2, 2))
    ]
    for a, b in tree:
        m.open_passage(a, b)
    assert gen._dead_ends(m) == [(0, 2), (2, 2)]


def test_braided_maze_has_no_dead_ends() -> None:
    m = Maze(3, 3)
    gen = MazeGenerator(m.width, m.height, perfect=True)
    tree = [
        ((0, 0), (0, 1)),
        ((0, 1), (1, 1)),
        ((1, 1), (1, 2)),
        ((1, 2), (0, 2)),
        ((1, 2), (2, 2)),
        ((2, 2), (2, 1)),
        ((2, 1), (2, 0)),
        ((2, 0), (1, 0)),
        ((0, 0), (1, 0)),
        ((0, 2), (0, 1)),
    ]
    for a, b in tree:
        m.open_passage(a, b)
    assert gen._dead_ends(m) == []


def _open_all_but(
    width: int,
    height: int,
    closed: frozenset[tuple[Coord, Coord]] = frozenset(),
    reserved: frozenset[Coord] = frozenset()
) -> Maze:
    m = Maze(width, height, reserved=reserved)
    for y in range(m.height):
        for x in range(m.width):
            pairs = []
            a = (x, y)
            if x + 1 < width:
                pairs.append((a, (x + 1, y)))
            if y + 1 < height:
                pairs.append((a, (x, y + 1)))
            for pair in pairs:
                if pair in closed:
                    continue
                a, b = pair
                if m.is_reserved(a) or m.is_reserved(b):
                    continue
                m.open_passage(a, b)
    return m


def test_closed_walls_in_counts_the_twelve() -> None:
    m_closed = Maze(3, 3)
    gen_closed = MazeGenerator(m_closed.width, m_closed.height)
    m_open = _open_all_but(3, 3)
    gen_open = MazeGenerator(m_open.width, m_open.height)
    assert gen_closed._closed_walls_in(m_closed, 0, 0) == 12
    assert gen_open._closed_walls_in(m_open, 0, 0) == 0


def test_last_wall_of_a_3x3_completes_it() -> None:
    a = (1, 1)
    b = (2, 1)
    m = _open_all_but(3, 3, closed=frozenset({(a, b)}))
    gen = MazeGenerator(m.width, m.height)
    assert gen._completes_open_3x3(m, a, b)


def test_vertical_wall_completes_a_3x3() -> None:
    a = (1, 1)
    b = (1, 2)
    m = _open_all_but(3, 3, closed=frozenset({(a, b)}))
    gen = MazeGenerator(m.width, m.height)
    assert gen._completes_open_3x3(m, a, b)


def test_two_closed_walls_do_not_complete_a_3x3() -> None:
    a = (1, 1)
    b = (1, 2)
    c = (1, 0)
    d = (2, 0)
    m = _open_all_but(3, 3, closed=frozenset({(a, b), (c, d)}))
    gen = MazeGenerator(m.width, m.height)
    assert not gen._completes_open_3x3(m, a, b)
    assert not gen._completes_open_3x3(m, c, d)


def test_no_3x3_fits_on_a_3_by_2_board() -> None:
    a = (0, 1)
    b = (1, 1)
    m = _open_all_but(3, 2, closed=frozenset({(a, b)}))
    gen = MazeGenerator(m.width, m.height)
    assert not gen._completes_open_3x3(m, a, b)


def test_windows_outside_the_grid_are_skipped() -> None:
    a = (0, 0)
    b = (1, 0)
    m = _open_all_but(4, 4, closed=frozenset({(a, b)}))
    gen = MazeGenerator(m.width, m.height)
    assert gen._completes_open_3x3(m, a, b)


def test_reserved_cell_never_completes_a_3x3() -> None:
    a = (1, 1)
    b = (2, 1)
    m = _open_all_but(
        5,
        5,
        closed=frozenset({(a, b)}),
        reserved=frozenset({(2, 2)})
    )
    gen = MazeGenerator(m.width, m.height)
    assert not gen._completes_open_3x3(m, a, b)


def test_braid_fixes_the_traced_tree() -> None:
    m = Maze(3, 3)
    gen = MazeGenerator(m.width, m.height, perfect=True, seed=0)
    tree = [
        ((0, 0), (0, 1)),
        ((0, 1), (1, 1)),
        ((1, 1), (1, 2)),
        ((1, 2), (0, 2)),
        ((1, 2), (2, 2)),
        ((2, 2), (2, 1)),
        ((2, 1), (2, 0)),
        ((2, 0), (1, 0))
    ]
    for a, b in tree:
        m.open_passage(a, b)
    assert gen._braid(m, Random(gen.seed)) == 2
    assert gen._dead_ends(m) == []


def test_braid_one_wall_can_fix_two_dead_ends() -> None:
    m = Maze(3, 2)
    gen = MazeGenerator(m.width, m.height, perfect=True, seed=0)
    tree = [
        ((0, 0), (1, 0)),
        ((1, 0), (2, 0)),
        ((2, 0), (2, 1)),
        ((2, 1), (1, 1)),
        ((1, 1), (0, 1))
    ]
    for a, b in tree:
        m.open_passage(a, b)
    assert gen._braid(m, Random(gen.seed)) == 1
    assert gen._dead_ends(m) == []


def test_braid_returns_the_walls_it_opened() -> None:
    gen = MazeGenerator(20, 15, perfect=True, seed=0)
    m = gen.generate()
    passages_before = _count_passages(m)
    result = gen._braid(m, Random(gen.seed))
    passages_after = _count_passages(m)
    assert result == passages_after - passages_before


def test_braid_skips_a_wall_that_would_complete_a_3x3() -> None:
    m = _open_all_but(3, 3, closed=frozenset({((0, 0), (1, 0))}))
    gen = MazeGenerator(m.width, m.height, perfect=True, seed=0)
    assert gen._braid(m, Random(gen.seed)) == 0
    assert not m.is_open((0, 0), Direction.EAST)
    assert gen._dead_ends(m) == [(0, 0)]


def test_braid_same_seed_same_maze() -> None:
    gen = MazeGenerator(20, 15, perfect=True, seed=0)
    m1 = gen.generate()
    m2 = gen.generate()
    gen._braid(m1, Random(1))
    gen._braid(m2, Random(1))
    assert tuple(m1.rows()) == tuple(m2.rows())


def test_braid_leaves_reserved_cells_closed() -> None:
    m = Maze(3, 3, reserved=frozenset({(1, 0)}))
    gen = MazeGenerator(m.width, m.height, perfect=True)
    tree = [
        ((0, 0), (0, 1)),
        ((0, 1), (1, 1)),
        ((1, 1), (2, 1)),
        ((2, 1), (2, 0)),
        ((1, 1), (1, 2)),
        ((1, 2), (0, 2)),
        ((1, 2), (2, 2))
    ]
    for a, b in tree:
        m.open_passage(a, b)
    gen._braid(m, Random(0))
    assert m.walls_at((1, 0)) == _ALL_WALLS


def test_braid_leaves_no_3x3_open_area() -> None:
    gen = MazeGenerator(20, 15, perfect=True, seed=0)
    m = gen.generate()
    gen._braid(m, Random(gen.seed))
    for y in range(m.height - 2):
        for x in range(m.width - 2):
            assert gen._closed_walls_in(m, x, y) >= 1


def test_add_loops_tops_up_the_3x2_path() -> None:
    m = Maze(3, 2)
    gen = MazeGenerator(m.width, m.height, perfect=True)
    tree = [
        ((0, 0), (1, 0)),
        ((1, 0), (2, 0)),
        ((2, 0), (2, 1)),
        ((2, 1), (1, 1)),
        ((1, 1), (0, 1))
    ]
    for a, b in tree:
        m.open_passage(a, b)
    gen._braid(m, Random(0))
    gen._add_loops(m, Random(0), 1)
    assert _count_passages(m) == m.width * m.height + 1


def test_add_loops_reaches_the_last_row_and_column() -> None:
    m1 = _open_all_but(
        3, 2,
        closed=frozenset({((0, 1), (1, 1)), ((1, 1), (2, 1))})
    )
    gen1 = MazeGenerator(m1.width, m1.height, perfect=True)
    passages_before = _count_passages(m1)
    gen1._add_loops(m1, Random(0), 1)
    assert _count_passages(m1) == passages_before + 1
    m2 = _open_all_but(
        2, 3,
        closed=frozenset({((1, 0), (1, 1)), ((1, 1), (1, 2))})
    )
    gen2 = MazeGenerator(m2.width, m2.height, perfect=True)
    passages_before = _count_passages(m2)
    gen2._add_loops(m2, Random(0), 1)
    assert _count_passages(m2) == passages_before + 1


def test_add_loops_raises_when_no_wall_can_open() -> None:
    m1 = _open_all_but(
        3, 2,
        closed=frozenset({((1, 0), (1, 1))})
    )
    gen1 = MazeGenerator(m1.width, m1.height, perfect=True)
    with pytest.raises(GenerationError):
        gen1._add_loops(m1, Random(0), 2)
    m2 = _open_all_but(3, 2, reserved=frozenset({(1, 1)}))
    gen2 = MazeGenerator(m2.width, m2.height, perfect=True)
    with pytest.raises(GenerationError):
        gen2._add_loops(m2, Random(0), 1)


def test_add_loops_never_completes_a_3x3() -> None:
    south_walls = _open_all_but(
        4, 3,
        closed=frozenset({((1, 1), (1, 2)), ((3, 0), (3, 1))})
    )
    east_walls = _open_all_but(
        3, 4,
        closed=frozenset({((1, 1), (2, 1)), ((0, 3), (1, 3))})
    )
    for m in (south_walls, east_walls):
        gen = MazeGenerator(m.width, m.height, perfect=True)
        with pytest.raises(GenerationError):
            gen._add_loops(m, Random(0), 2)
