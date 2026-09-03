"""Reading the configuration file the program is given.

The configuration is the program's only input (§IV.2), so this module is
where text written by hand becomes values the rest of the code can rely
on. Nothing downstream checks them a second time.
"""

from dataclasses import dataclass
from pathlib import Path


Coord = tuple[int, int]


class ConfigError(Exception):
    """Base class for every error this module raises."""


class ConfigFileError(ConfigError):
    """The file could not be read: missing, a directory, no permission."""


class ConfigSyntaxError(ConfigError):
    """A line exists but is not a KEY=VALUE pair."""


class ConfigValueError(ConfigError):
    """A key is present but its value cannot be used."""


class ConfigMissingKeyError(ConfigError):
    """A mandatory key never appeared."""


@dataclass(frozen=True)
class Config:
    """The whole configuration, validated, as one immutable object."""

    width: int
    height: int
    entry: Coord
    exit: Coord
    output_file: str
    perfect: bool
    seed: int | None = None


def _read_pairs(text: str, source: str) -> dict[str, tuple[str, int]]:
    """Split the configuration text into its ``KEY=VALUE`` pairs.

    Blank lines and lines starting with ``#`` are ignored (§IV.3). Every
    other line must hold an ``=``: the key is what comes before the first
    one, the value is all of the rest, so a value may contain ``=``
    itself.

    Parameters
    ----------
    text:
        The whole configuration file, newlines included.
    source:
        The name to show in error messages, normally the file the text
        was read from. Every message reads ``source:line: problem``.

    Returns
    -------
    dict[str, tuple[str, int]]
        One entry per key, holding its value and the line it came from.
        The line number travels with the value because the stages that
        interpret it report their own errors long after the text itself
        is gone.

    Raises
    ------
    ConfigSyntaxError
        If a line holds no ``=``, or holds nothing before it.
    ConfigValueError
        If a key appears twice. Both line numbers are named: the one to
        delete is the one the reader has to find.

    Notes
    -----
    **Values are not interpreted here.** ``WIDTH=abc`` passes — it is a
    well-formed pair whose value happens to be unusable, and saying so
    belongs to a later stage. Keys are case-sensitive, and unknown keys
    are kept rather than rejected, since §IV.3 allows a configuration to
    carry extra ones.
    """
    pairs: dict[str, tuple[str, int]] = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue
        if "=" not in line:
            message = (
                f"{source}:{lineno}: "
                f"expected KEY=VALUE, got '{line}'"
            )
            raise ConfigSyntaxError(message)
        key, value = line.split("=", 1)
        key = key.strip()
        if key == "":
            message = (
                f"{source}:{lineno}: "
                f"missing key before '=', got '{line}'"
            )
            raise ConfigSyntaxError(message)
        if key in pairs:
            _, first_lineno = pairs[key]
            message = (
                f"{source}:{lineno}: "
                f"duplicate key '{key}', "
                f"first defined on line {first_lineno}"
            )
            raise ConfigValueError(message)
        value = value.strip()
        pairs[key] = (value, lineno)
    return pairs


def parse_config(text: str, source: str = "<config>") -> Config:
    raise NotImplementedError("Not implemented")
