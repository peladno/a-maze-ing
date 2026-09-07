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


def _where(source: str, key: str, lineno: int) -> str:
    """Build the prefix every error message in this module starts with.

    Parameters
    ----------
    source:
        The name of the configuration, normally the file it was read
        from.
    key:
        The key the message is about.
    lineno:
        The line that key was read from, counting from 1 as an editor
        does.

    Returns
    -------
    str
        ``source:line: KEY``, so that whatever follows reads as a
        sentence about that key. Holding the format in one place is what
        keeps the call sites from drifting apart.
    """
    where = f"{source}:{lineno}: {key}"
    return where


def _as_filename(filename: str, where: str) -> str:
    """Return the output file name, refusing an empty one.

    Parameters
    ----------
    filename:
        The value as it was written, already stripped.
    where:
        Prefix from ``_where``, naming the source, line and key.

    Returns
    -------
    str
        The name unchanged. Nothing about the path is checked here:
        whether it can be created, and whether its directory exists, are
        only knowable at the moment it is opened, and that belongs to
        the code that writes the output file.

    Raises
    ------
    ConfigValueError
        If the value is empty.
    """
    if not filename:
        raise ConfigValueError(f"{where} must not be empty")
    return filename


_BOOL: dict[str, bool] = {
    "True": True,
    "False": False
}


def _as_bool(value: str, where: str) -> bool:
    """Return the PERFECT flag as a boolean.

    Parameters
    ----------
    value:
        The value as it was written, already stripped.
    where:
        Prefix from ``_where``, naming the source, line and key.

    Returns
    -------
    bool
        True or False, read from the two spellings §IV.3 uses.

    Raises
    ------
    ConfigValueError
        For any other spelling, naming the ones that are accepted.

    Notes
    -----
    Only ``True`` and ``False`` are accepted, matching the subject
    exactly rather than guessing at ``true``, ``1`` or ``yes``. The
    table is the single statement of what is allowed, and the rejection
    message is built from it, so the two cannot disagree.

    ``bool()`` is deliberately not used: ``bool("False")`` is True,
    because a non-empty string is truthy whatever it happens to say.
    """
    if value in _BOOL:
        return _BOOL[value]
    accepted = " or ".join(_BOOL)
    raise ConfigValueError(f"{where} must be {accepted}, got '{value}'")


def _as_int(value: str, where: str, minimum: int | None) -> int:
    """Return the value as an integer, within an optional lower bound.

    Parameters
    ----------
    value:
        The value as it was written, already stripped.
    where:
        Prefix from ``_where``, naming the source, line and key.
    minimum:
        The smallest value allowed, or None when any integer will do.
        There is deliberately no default: every caller states its own
        range, so a bound cannot be forgotten. Sizes pass 1, the parts
        of a coordinate pass 0, and a seed passes None.

    Returns
    -------
    int
        The converted value, known to be within the bound.

    Raises
    ------
    ConfigValueError
        If the text is not a whole number, or is below the bound.

    Notes
    -----
    ``int()`` does the whole job: it accepts a sign and surrounding
    spaces, and refuses ``3.5``, ``1e3``, ``20abc`` and the empty string
    alike, because it converts the whole text or none of it. Its
    ValueError is translated rather than let out, since §IV.2 asks for a
    message naming the line the value came from.

    The bound is tested with ``is not None`` and not for truth: 0 is a
    legitimate bound, and ``if minimum:`` would silently skip it, so a
    negative coordinate would pass.
    """
    try:
        number = int(value)
    except ValueError as err:
        message = f"{where} must be a whole number, got '{value}'"
        raise ConfigValueError(message) from err
    if minimum is not None and number < minimum:
        message = f"{where} must be at least {minimum}, got '{value}'"
        raise ConfigValueError(message)
    return number


def _as_coord(value: str, where: str) -> Coord:
    """Return the value as an ``(x, y)`` coordinate.

    Parameters
    ----------
    value:
        The value as it was written, already stripped.
    where:
        Prefix from ``_where``, naming the source, line and key. Each
        part is converted under a prefix of its own, so a message can
        say which of the two is at fault.

    Returns
    -------
    Coord
        ``(x, y)``: x the column, y the row, both at least 0. Whether
        the pair is *inside the grid* is not knowable here, since that
        needs WIDTH and HEIGHT; it is checked once every key has been
        read.

    Raises
    ------
    ConfigValueError
        If the value is not exactly two comma-separated parts, or if
        either part is not a whole number, or is negative.

    Notes
    -----
    The count is checked **before** unpacking. Unpacking the wrong
    number of parts raises a bare ValueError, which is the kind of
    crash §IV.2 forbids, and ``ENTRY=0`` is an easy line to write.

    Each part is converted by ``_as_int``, so what counts as a number,
    the lower bound, and the message that rejects one are all written
    in a single place. Nothing here repeats them.
    """
    parts = value.split(",")
    if len(parts) != 2:
        message = f"{where} must be 'x,y', got '{value}'"
        raise ConfigValueError(message)
    x, y = parts
    where_x = f"{where} x"
    x_int = _as_int(x, where_x, minimum=0)
    where_y = f"{where} y"
    y_int = _as_int(y, where_y, minimum=0)
    return (x_int, y_int)


def parse_config(text: str, source: str = "<config>") -> Config:
    raise NotImplementedError
