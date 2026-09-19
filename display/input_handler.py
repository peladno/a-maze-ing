from __future__ import annotations

from collections.abc import Callable, Collection
from enum import Enum
from typing import TYPE_CHECKING

from display.colors import WALL_COLORS
from display.renderer import MazeLike

from .terminal_renderer import TerminalRenderer

if TYPE_CHECKING:
    from maze.maze import Coord


class UserAction(Enum):
    TOGGLE_PATH = "t"
    CHANGE_COLOR = "c"
    REGENERATE = "r"
    QUIT = "q"


def display_menu() -> None:
    """Prints a beautiful and clean interactive menu to the terminal."""
    print("=" * 40)
    print(f"{'MAZE INTERACTIVE MENU':^40}")
    print("=" * 40)
    print(f"  [{UserAction.TOGGLE_PATH.value}] Toggle Path     - "
          "Show/hide optimal path")
    print(f"  [{UserAction.CHANGE_COLOR.value}] Change Color    - "
          "Switch wall color mode")
    print(f"  [{UserAction.REGENERATE.value}] Regenerate      - "
          "Generate a new maze")
    print(f"  [{UserAction.QUIT.value}] Quit            - "
          "Exit the application")
    print("=" * 40)


def get_user_action() -> UserAction:
    """Prompt the user and return the selected action.

    Returns
    -------
    UserAction
        The valid action selected by the user ('t', 'c', 'r', or 'q').
    """
    while True:
        user_selection = input("Choose an option (t/c/r/q): ").strip().lower()

        valid_values = [action.value for action in UserAction]

        if user_selection in valid_values:
            return UserAction(user_selection)
        else:
            print("❌ Incorrect option, "
                  "please choose between: 't', 'c', 'r' or 'q'.")


def apply_action(
    action: UserAction,
    renderer: TerminalRenderer,
    on_regenerate: Callable[[], object] | None = None,
) -> bool:
    """Apply the chosen user action to the renderer or application state.

    Parameters
    ----------
    action:
        The action chosen by the user.
    renderer:
        The renderer whose options (show_path, color_mode) are updated.
    on_regenerate:
        Optional callback invoked when ``UserAction.REGENERATE`` is chosen.

    Returns
    -------
    bool
        True if the interactive loop should continue; False if quitting.
    """
    if action == UserAction.TOGGLE_PATH:
        renderer.show_path = not renderer.show_path
        return True

    if action == UserAction.CHANGE_COLOR:
        renderer.color_mode = (renderer.color_mode + 1) % len(WALL_COLORS)
        return True

    if action == UserAction.REGENERATE:
        if on_regenerate is not None:
            on_regenerate()
        return True

    if action == UserAction.QUIT:
        print("Exiting application. Goodbye!")
        return False

    return True


def run_interactive_session(
    renderer: TerminalRenderer,
    maze: MazeLike,
    on_regenerate: (
        Callable[[], tuple[MazeLike, Collection[Coord]] | MazeLike] | None
    ) = None,
) -> None:
    """Run the interactive terminal session loop.

    Parameters
    ----------
    renderer:
        The terminal renderer used to draw the maze.
    maze:
        The initial maze object to display.
    on_regenerate:
        Optional callable invoked when the user selects 'r' (Regenerate).
        It may return a new ``MazeLike`` object, or a tuple of
        ``(new_maze, new_path)``.

    Returns
    -------
    None
        The loop runs until the user chooses to quit.
    """
    current_maze = maze
    running = True
    while running:
        renderer.render(current_maze)
        display_menu()
        action = get_user_action()
        if action == UserAction.REGENERATE and on_regenerate is not None:
            result = on_regenerate()
            if isinstance(result, tuple):
                current_maze, new_path = result
                renderer.shortest_path = set(new_path)
                setattr(current_maze, "shortest_path", set(new_path))
                if renderer.entry is not None:
                    setattr(current_maze, "entry", renderer.entry)
                if renderer.exit is not None:
                    setattr(current_maze, "exit", renderer.exit)
            else:
                current_maze = result
        else:
            running = apply_action(action, renderer)
