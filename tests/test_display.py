"""Integration and unit tests for display/terminal_renderer.py.

Verifies terminal rendering functionality, option validation, horizontal and
vertical wall formatting, cell marker placement, and standard output.
"""

from __future__ import annotations
import pytest

from typing import TYPE_CHECKING
from maze.maze import Maze
from display import (
    TerminalRenderer,
    UserAction,
    WALL_COLORS,
    apply_action,
    display_menu,
    get_user_action,
    run_interactive_session,
)

if TYPE_CHECKING:
    from maze.maze import Coord


def test_terminal_renderer_init_valid() -> None:
    """Verify initializing TerminalRenderer with valid display options.

    Returns
    -------
    None
        Asserts that show_path and color_mode properties are set correctly.
    """
    renderer = TerminalRenderer(show_path=True, color_mode=1)
    assert renderer.show_path is True
    assert renderer.color_mode == 1


def test_terminal_renderer_init_invalid_color_mode() -> None:
    """Verify that invalid color_mode values raise a ValueError.

    Returns
    -------
    None
        Asserts that out-of-range color_mode values raise ValueError.
    """
    with pytest.raises(ValueError):
        TerminalRenderer(color_mode=-1)

    with pytest.raises(ValueError):
        TerminalRenderer(color_mode=len(WALL_COLORS))


def test_terminal_renderer_horizontal_wall() -> None:
    """Verify horizontal wall string construction for a grid row.

    Returns
    -------
    None
        Asserts the generated ASCII segment matching cell wall masks.
    """
    renderer = TerminalRenderer(color_mode=0)
    maze = Maze(width=2, height=2)

    # N wall (1) in row 0: cell 0 mask 9 (N bit set), cell 1 mask 3 (N bit set)
    wall_str = renderer._horizontal_wall(maze, y=0, wall=1)
    assert wall_str == "+---+---+"


def test_terminal_renderer_cell_content() -> None:
    """Verify cell marker formatting for entry, exit, path, and empty cells.

    Returns
    -------
    None
        Asserts presence of 'E', 'X', and '.' markers under display options.
    """
    maze = Maze(width=2, height=2)
    setattr(maze, "entry", (0, 0))
    setattr(maze, "exit", (1, 1))
    shortest_path: tuple[Coord, ...] = ((0, 0), (0, 1), (1, 1))
    setattr(maze, "shortest_path", shortest_path)

    renderer_with_path = TerminalRenderer(show_path=True, color_mode=0)
    renderer_no_path = TerminalRenderer(show_path=False, color_mode=0)

    # Entry cell
    assert "E" in renderer_with_path._cell_content(0, 0, maze)
    # Exit cell
    assert "X" in renderer_with_path._cell_content(1, 1, maze)
    # Path cell (0, 1) when show_path=True
    assert "." in renderer_with_path._cell_content(0, 1, maze)
    # Path cell (0, 1) when show_path=False
    assert "." not in renderer_no_path._cell_content(0, 1, maze)


def test_terminal_renderer_render_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify that render() prints the complete ASCII maze to stdout.

    Parameters
    ----------
    capsys:
        Pytest standard output and standard error capture fixture.

    Returns
    -------
    None
        Asserts line count and start pattern written to standard output.
    """
    renderer = TerminalRenderer(show_path=True, color_mode=0)
    maze = Maze(width=2, height=2)
    maze.open_passage((0, 0), (1, 0))

    renderer.render(maze)

    captured = capsys.readouterr()
    lines = captured.out.splitlines()

    # 2 rows -> 1 top border + 2 * (1 vertical row + 1 bottom border) = 5 lines
    assert len(lines) == 5
    assert lines[0].startswith("+")


def test_apply_action_toggle_path() -> None:
    """Verify that TOGGLE_PATH inverts show_path and returns True.

    Returns
    -------
    None
        Asserts that renderer.show_path is toggled.
    """
    render = TerminalRenderer(show_path=False, color_mode=0)
    loop = apply_action(UserAction.TOGGLE_PATH, render)

    assert render.show_path is True
    assert loop is True

    loop = apply_action(UserAction.TOGGLE_PATH, render)

    assert render.show_path is False
    assert loop is True


def test_apply_action_change_color() -> None:
    """Verify that CHANGE_COLOR cycles color_mode and returns True.

    Returns
    -------
    None
        Asserts that renderer.color_mode increments and wraps around.
    """
    render = TerminalRenderer(show_path=False, color_mode=0)
    loop = apply_action(UserAction.CHANGE_COLOR, render)

    assert loop is True
    assert render.color_mode == 1

    render.color_mode = len(WALL_COLORS) - 1
    loop = apply_action(UserAction.CHANGE_COLOR, render)

    assert render.color_mode == 0


def test_apply_action_quit() -> None:
    """Verify that QUIT returns False to signal loop termination.

    Returns
    -------
    None
        Asserts that apply_action returns False.
    """
    render = TerminalRenderer(show_path=False, color_mode=0)
    loop = apply_action(UserAction.QUIT, render)

    assert loop is False


def test_get_user_action_valid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that get_user_action returns the matching UserAction.

    Parameters
    ----------
    monkeypatch:
        Pytest monkeypatch fixture to simulate user input.

    Returns
    -------
    None
        Asserts that valid input string maps to UserAction.
    """
    test_cases = [
        ("t", UserAction.TOGGLE_PATH),
        ("c", UserAction.CHANGE_COLOR),
        ("r", UserAction.REGENERATE),
        ("q", UserAction.QUIT),
        (" T ", UserAction.TOGGLE_PATH),
    ]

    for user_input, expected_action in test_cases:
        monkeypatch.setattr("builtins.input", lambda _: user_input)
        assert get_user_action() == expected_action

    answer = iter([" ", "a", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(answer))

    action = get_user_action()
    assert action == UserAction.QUIT


def test_display_menu_content(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify that display_menu prints the menu with all options.

    Parameters
    ----------
    capsys:
        Pytest standard output capture fixture.

    Returns
    -------
    None
        Asserts that option keys appear in stdout.
    """
    display_menu()

    captured = capsys.readouterr()
    printed = captured.out

    assert "MAZE INTERACTIVE MENU" in printed
    assert "=" * 40 in printed
    assert f"[{UserAction.TOGGLE_PATH.value}] Toggle Path" in printed
    assert f"[{UserAction.CHANGE_COLOR.value}] Change Color" in printed
    assert f"[{UserAction.REGENERATE.value}] Regenerate" in printed
    assert f"[{UserAction.QUIT.value}] Quit" in printed


def test_terminal_renderer_init_with_explicit_params() -> None:
    """Verify initializing TerminalRenderer with explicit coordinates and path.

    Returns
    -------
    None
        Asserts that entry, exit, and shortest_path attributes are stored
        correctly on the renderer.
    """
    entry: Coord = (0, 0)
    exit_coord: Coord = (3, 3)
    path: list[Coord] = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 3)]

    renderer = TerminalRenderer(
        show_path=True,
        color_mode=2,
        entry=entry,
        exit=exit_coord,
        shortest_path=path,
    )

    assert renderer.entry == (0, 0)
    assert renderer.exit == (3, 3)
    assert renderer.shortest_path == set(path)
    assert renderer.show_path is True
    assert renderer.color_mode == 2

    maze = Maze(width=4, height=4)
    assert "E" in renderer._cell_content(0, 0, maze)
    assert "X" in renderer._cell_content(3, 3, maze)
    assert "." in renderer._cell_content(1, 0, maze)
    assert " " in renderer._cell_content(0, 1, maze)


def test_terminal_renderer_render_shortest_path_override(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify that render() accepts a shortest_path override and updates state.

    Parameters
    ----------
    capsys:
        Pytest standard output capture fixture.

    Returns
    -------
    None
        Asserts that shortest_path on the renderer is updated and rendered.
    """
    renderer = TerminalRenderer(show_path=True, color_mode=0)
    maze = Maze(width=2, height=2)

    assert renderer.shortest_path is None
    new_path: list[Coord] = [(0, 0), (1, 0)]
    renderer.render(maze, shortest_path=new_path)

    assert renderer.shortest_path == {(0, 0), (1, 0)}
    captured = capsys.readouterr()
    assert "." in captured.out


def test_apply_action_regenerate() -> None:
    """Verify that REGENERATE triggers on_regenerate callback and returns True.

    Returns
    -------
    None
        Asserts that callback is called and loop continues.
    """
    called = False

    def callback() -> None:
        nonlocal called
        called = True

    renderer = TerminalRenderer(color_mode=0)

    assert apply_action(UserAction.REGENERATE, renderer) is True

    assert apply_action(
        UserAction.REGENERATE, renderer, on_regenerate=callback
    ) is True
    assert called is True


def test_run_interactive_session_regenerate_and_quit(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify interactive session handles regeneration and quit actions.

    Parameters
    ----------
    monkeypatch:
        Pytest monkeypatch fixture to simulate user input sequence.
    capsys:
        Pytest standard output capture fixture.

    Returns
    -------
    None
        Asserts that maze and shortest_path are updated on regeneration and
        session terminates on quit.
    """
    initial_maze = Maze(width=2, height=2)
    new_maze = Maze(width=2, height=2)
    new_path: list[Coord] = [(0, 0), (0, 1)]
    callback_called = False

    def on_regen() -> tuple[Maze, list[Coord]]:
        nonlocal callback_called
        callback_called = True
        return new_maze, new_path

    renderer = TerminalRenderer(
        show_path=True,
        color_mode=0,
        entry=(0, 0),
        exit=(1, 1),
    )

    inputs = iter(["r", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_interactive_session(renderer, initial_maze, on_regenerate=on_regen)

    assert callback_called is True
    assert renderer.shortest_path == set(new_path)
    captured = capsys.readouterr()
    assert "MAZE INTERACTIVE MENU" in captured.out
