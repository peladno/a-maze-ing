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


_REQUIRED = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")


def _take(
    pairs: dict[str, tuple[str, int]],
    key: str,
    source: str
) -> tuple[str, str]:
    """Return one key's value together with the prefix for its messages.

    Parameters
    ----------
    pairs:
        The result of ``_read_pairs``. The key must be present; callers
        check that first, either against the required list or with
        ``in``.
    key:
        The key to read.
    source:
        The name of the configuration, for the prefix.

    Returns
    -------
    tuple[str, str]
        ``(value, where)`` in that order. Both are strings, so nothing
        would complain if they were swapped -- unpack them under these
        two names.

    Notes
    -----
    It exists so the key is named **once** per setting. Reading the
    value and building the prefix both need it, and writing it twice is
    how a message ends up naming the key next to the one it read.
    """
    value, lineno = pairs[key]
    where = _where(source, key, lineno)
    return (value, where)


def _require_inside(coord: Coord, where: str, width: int, height: int) -> None:
    """Raise unless the coordinate falls inside a width by height grid.

    Parameters
    ----------
    coord:
        The position to check, as ``(x, y)``.
    where:
        Prefix from ``_where``. The failing part is named after it, so a
        message can say which of x and y is out.
    width, height:
        The grid the configuration asked for.

    Raises
    ------
    ConfigValueError
        If x is not below width, or y is not below height.

    Notes
    -----
    Only the upper bound is tested here: ``_as_coord`` already refused a
    negative part. And only this much is testable at all before a maze
    exists -- whether the cell is on the outer wall, and whether it is
    reachable, are questions for the code that validates the maze.

    The bound is ``width``, not ``width - 1``: with WIDTH=20 the columns
    are 0 to 19, which is the off-by-one the subject's own example is
    written to show.
    """
    x, y = coord
    if x >= width:
        where_x = f"{where} x"
        message = f"{where_x} must be less than {width}, got {x}"
        raise ConfigValueError(message)
    if y >= height:
        where_y = f"{where} y"
        message = f"{where_y} must be less than {height}, got {y}"
        raise ConfigValueError(message)


def parse_config(text: str, source: str = "<config>") -> Config:
    """Turn the text of a configuration file into a validated Config.

    The three stages run in order and the order matters: the pairs are
    read, the required keys are confirmed, and only then is any value
    interpreted. Confirming the keys first is what makes the lookups
    below safe -- past that point a key is known to be there.

    Parameters
    ----------
    text:
        The whole configuration file.
    source:
        The name to show in error messages, normally the file the text
        came from. ``load_config`` passes the path; a test passing a
        string of its own can leave the default.

    Returns
    -------
    Config
        Frozen, with every value converted and in range. Nothing
        downstream needs to check any of it again.

    Raises
    ------
    ConfigSyntaxError
        From ``_read_pairs``, if a line is not a ``KEY=VALUE`` pair.
    ConfigMissingKeyError
        If any of the six keys §IV.3 requires never appeared. All the
        missing ones are named at once: they are equally wrong, and
        reporting the first alone would send the user round again.
    ConfigValueError
        If a value cannot be used, or if entry or exit falls outside the
        grid, or if they are the same cell (§IV.4).

    Notes
    -----
    The checks at the end are the ones that need more than one key, so
    they cannot be made while the keys are being read. What they do
    *not* include is anything needing the maze itself: that a cell sits
    on the outer wall, or can be reached, is checked once a maze exists.
    The line between the two is simply whether the question can be
    answered from the file alone.

    A missing key carries no line number, unlike every other message
    here. There is no line to point at -- the failure is that nothing
    was written.
    """
    pairs = _read_pairs(text, source)
    missing = []
    for key in _REQUIRED:
        if key not in pairs:
            missing.append(key)
    if missing:
        mkeys = ", ".join(missing)
        message = f"{source}: missing required keys: {mkeys}"
        raise ConfigMissingKeyError(message)
    value, where = _take(pairs, "WIDTH", source)
    width = _as_int(value, where, 1)
    value, where = _take(pairs, "HEIGHT", source)
    height = _as_int(value, where, 1)
    value, where_entry = _take(pairs, "ENTRY", source)
    entry = _as_coord(value, where_entry)
    value, where_exit = _take(pairs, "EXIT", source)
    exit = _as_coord(value, where_exit)
    value, where = _take(pairs, "OUTPUT_FILE", source)
    output_file = _as_filename(value, where)
    value, where = _take(pairs, "PERFECT", source)
    perfect = _as_bool(value, where)
    if "SEED" in pairs:
        value, where = _take(pairs, "SEED", source)
        seed = _as_int(value, where, minimum=None)
    else:
        seed = None
    _require_inside(entry, where_entry, width, height)
    _require_inside(exit, where_exit, width, height)
    if entry == exit:
        message = (
            f"{where_exit} must not be the same value of entry {entry}"
        )
        raise ConfigValueError(message)
    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=output_file,
        perfect=perfect,
        seed=seed
    )


def load_config(path: str | Path) -> Config:
    """Read a configuration file and return it as a validated Config.

    This is the only function here that touches the filesystem, which is
    why it is so thin: everything else takes text, and so every test of
    the parsing needs nothing but a string literal.

    Parameters
    ----------
    path:
        The file to read. ``str`` or ``Path`` -- ``Path()`` accepts
        either, so nothing branches on which one arrived.

    Returns
    -------
    Config
        The parsed configuration. See ``parse_config``.

    Raises
    ------
    ConfigFileError
        If the file cannot be read at all: missing, a directory, no
        permission, or not valid UTF-8.
    ConfigError
        Any of the parsing errors, unchanged, from ``parse_config``.

    Notes
    -----
    Nothing is checked before reading. Asking ``exists()`` first would
    cover one of the four failures and leave the other three to the read
    anyway, so the check would not remove the ``try`` -- and between the
    question and the answer the file can still go away.

    ``OSError`` is caught as a whole rather than by subclass, because
    every one of them means the same thing to us and the subclasses are
    not the same everywhere: opening a directory raises
    ``IsADirectoryError`` on Linux and ``PermissionError`` on Windows.
    ``UnicodeDecodeError`` is named separately since it is not an
    ``OSError``.

    The message keeps what the system said. A failure we never thought
    of still arrives described correctly, rather than being labelled
    with the nearest guess we had prepared.

    ``encoding`` is stated rather than left to the platform default: the
    two of us read the same file on different machines.
    """
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        raise ConfigFileError(f"{path}: {err}") from err
    return parse_config(text, str(path))
