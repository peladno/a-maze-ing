from enum import Enum

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
    raise NotImplementedError("Not implemented yet")


if __name__ == "__main__":
    display_menu()
    action = get_user_action()
    print(f"¡You choose the correct action: {action.name}!")
