from enum import Enum

from display.colors import WALL_COLORS
from display.renderer import MazeLike

from .terminal_renderer import TerminalRenderer


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
    while True:
        user_selection = input("Choose an option (t/c/r/q): ").strip().lower()

        valid_values = [action.value for action in UserAction]

        if user_selection in valid_values:
            return UserAction(user_selection)
        else:
            print("❌ Incorrect option, "
                  "please choose between: 't', 'c', 'r' or 'q'.")


def apply_action(action: UserAction, renderer: TerminalRenderer) -> bool:
    """Apply the chosen user action to the renderer or application state.

    Parameters
    ----------
    action:
        The action chosen by the user.
    renderer:
        The renderer whose options (show_path, color_mode) are updated.

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
        return True

    if action == UserAction.QUIT:
        print("Exiting application. Goodbye!")
        return False

    return True


def run_interactive_session(
    renderer: TerminalRenderer, maze: MazeLike
) -> None:
    """Run the interactive terminal session loop.

    Parameters
    ----------
    renderer:
        The terminal renderer used to draw the maze.
    maze:
        The maze object to display.

    Returns
    -------
    None
        The loop runs until the user chooses to quit.
    """
    running = True
    while running:
        renderer.render(maze)
        display_menu()
        action = get_user_action()
        running = apply_action(action, renderer)


# if __name__ == "__main__":
#     from display.example_maze import DummyMaze

#     test_maze = DummyMaze(width=5, height=4, seed=42)
#     sample_path = (
#         (0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3)
#     )
#     setattr(test_maze, "shortest_path", sample_path)
#     test_renderer = TerminalRenderer(show_path=False, color_mode=0)

#     run_interactive_session(test_renderer, test_maze)
