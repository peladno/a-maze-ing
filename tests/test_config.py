import pytest
from maze.config import _read_pairs
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
