import pytest
from maze.generator import MazeGenerator
from maze.generator import GenerationError


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
