import pytest
from maze.config import _read_pairs
from maze.config import _as_filename
from maze.config import _as_bool
from maze.config import _as_int
from maze.config import _as_coord
from maze.config import ConfigSyntaxError
from maze.config import ConfigValueError


def test_line_without_equals_raises() -> None:
    text = "WIDTH"
    with pytest.raises(ConfigSyntaxError):
        _read_pairs(text, "config.txt")


def test_reads_a_simple_config() -> None:
    text = "WIDTH=20\nHEIGHT=15\n"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"WIDTH": ("20", 1), "HEIGHT": ("15", 2)}


def test_blank_lines_are_ignored() -> None:
    text = "WIDTH=20\n\nHEIGHT=15\n"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"WIDTH": ("20", 1), "HEIGHT": ("15", 3)}


def test_comments_are_ignored() -> None:
    text = "# WIDTH=99\nWIDTH=20\nHEIGHT=15\n # HEIGHT=99\n"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"WIDTH": ("20", 2), "HEIGHT": ("15", 3)}


def test_whitespace_is_stripped() -> None:
    text = "WIDTH = 20\n HEIGHT=15 \n"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"WIDTH": ("20", 1), "HEIGHT": ("15", 2)}


def test_value_may_contain_equals() -> None:
    text = "OUTPUT_FILE=a=b.txt"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"OUTPUT_FILE": ("a=b.txt", 1)}


def test_hash_inside_a_value_is_kept() -> None:
    text = "OUTPUT_FILE=my#maze.txt"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"OUTPUT_FILE": ("my#maze.txt", 1)}


def test_unknown_keys_are_kept() -> None:
    text = "COLOUR=blue"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"COLOUR": ("blue", 1)}


def test_keys_are_case_sensitive() -> None:
    text = "width=20"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {"width": ("20", 1)}


def test_crlf_line_endings() -> None:
    text = "WIDTH=20\nHEIGHT=15\r\nOUTPUT_FILE=maze.txt"
    pairs = _read_pairs(text, "config.txt")
    assert pairs == {
        "WIDTH": ("20", 1),
        "HEIGHT": ("15", 2),
        "OUTPUT_FILE": ("maze.txt", 3),
    }


def test_empty_key_raises() -> None:
    text = "=20"
    with pytest.raises(ConfigSyntaxError):
        _read_pairs(text, "config.txt")


def test_duplicate_key_raises() -> None:
    text = "WIDTH=20\nWIDTH=10"
    with pytest.raises(ConfigValueError):
        _read_pairs(text, "config.txt")


def test_message_names_source_and_line() -> None:
    text = "WIDTH=20\nHEIGHT=15\n=20"
    with pytest.raises(ConfigSyntaxError) as excinfo:
        _read_pairs(text, "config.txt")
    assert "config.txt:3" in str(excinfo.value)


def test_duplicate_message_names_both_lines() -> None:
    text = "WIDTH=20\nWIDTH=10"
    with pytest.raises(ConfigValueError) as excinfo:
        _read_pairs(text, "config.txt")
    assert "config.txt:2" in str(excinfo.value)
    assert "'WIDTH'" in str(excinfo.value)
    assert "line 1" in str(excinfo.value)


def test_as_filename_accepts_a_name() -> None:
    filename = "maze.txt"
    where = "config.txt:5: OUTPUT_FILE"
    result = _as_filename(filename, where)
    assert result == "maze.txt"


def test_as_filename_rejects_empty() -> None:
    filename = ""
    where = "config.txt:5: OUTPUT_FILE"
    with pytest.raises(ConfigValueError) as excinfo:
        _as_filename(filename, where)
    assert where in str(excinfo.value)


def test_as_bool_accepts_true() -> None:
    where = "config.txt:6: PERFECT"
    result = _as_bool("True", where)
    assert result is True


def test_as_bool_accepts_false() -> None:
    where = "config.txt:6: PERFECT"
    result = _as_bool("False", where)
    assert result is False


def test_as_bool_rejects_other_spellings() -> None:
    where = "config.txt:6: PERFECT"
    for value in ["true", "1", "yes", ""]:
        with pytest.raises(ConfigValueError) as excinfo:
            _as_bool(value, where)
        assert where in str(excinfo.value)


def test_as_int_accepts_a_number() -> None:
    where = "config.txt:1: WIDTH"
    result = _as_int("20", where, 1)
    assert result == 20


def test_as_int_rejects_non_numbers() -> None:
    where = "config.txt:1: WIDTH"
    for value in ["twenty", "3.5", "1e3", "", "20abc"]:
        with pytest.raises(ConfigValueError) as excinfo:
            _as_int(value, where, None)
        assert where in str(excinfo.value)


def test_as_int_rejects_below_minimum() -> None:
    where = "config.txt:2: HEIGHT"
    with pytest.raises(ConfigValueError) as excinfo:
        _as_int("0", where, minimum=1)
    assert where in str(excinfo.value)


def test_as_int_accepts_zero_when_minimum_is_zero() -> None:
    where = "config.txt:2: HEIGHT"
    result = _as_int("0", where, 0)
    assert result == 0


def test_as_int_without_minimum_accepts_negative() -> None:
    where = "config.txt:2: HEIGHT"
    result = _as_int("-5", where, None)
    assert result == -5


def test_as_coord_accepts_a_pair() -> None:
    where = "config.txt:3: ENTRY"
    result = _as_coord("5,3", where)
    assert result == (5, 3)


def test_as_coord_rejects_one_number() -> None:
    where = "config.txt:3: ENTRY"
    with pytest.raises(ConfigValueError) as excinfo:
        _as_coord("0", where)
    assert where in str(excinfo.value)


def test_as_coord_rejects_three_numbers() -> None:
    where = "config.txt:3: ENTRY"
    with pytest.raises(ConfigValueError) as excinfo:
        _as_coord("1,2,3", where)
    assert where in str(excinfo.value)


def test_as_coord_rejects_non_numbers() -> None:
    where = "config.txt:3: ENTRY"
    with pytest.raises(ConfigValueError) as excinfo:
        _as_coord("a,b", where)
    assert where in str(excinfo.value)


def test_as_coord_rejects_negative() -> None:
    where = "config.txt:3: ENTRY"
    for value in ["-1,0", "0,-1"]:
        with pytest.raises(ConfigValueError) as excinfo:
            _as_coord(value, where)
    assert where in str(excinfo.value)


def test_as_coord_allows_spaces_around_numbers() -> None:
    where = "config.txt:3: ENTRY"
    result = _as_coord("5 , 3", where)
    assert result == (5, 3)
