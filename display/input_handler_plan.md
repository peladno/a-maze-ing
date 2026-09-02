# Input Handler Implementation Plan

## 1. Overview & Purpose

The `input_handler.py` module is responsible for handling interactive user commands in the terminal interface. It decouples user input processing from the maze rendering logic (`TerminalRenderer`) and maze data structures (`Maze`).

## 2. Requirements & Features

According to the project subject (§V) and architecture proposal (W16), the input handler must support the following interactive operations:

1. **Toggle Shortest Path**:
   - Allow the user to show or hide the optimal path markers (`.`) on the rendered terminal output.
2. **Change Wall Colors**:
   - Cycle through or select configured ANSI wall color modes (`color_mode=0..3`).
3. **Maze Regeneration / Refresh**:
   - Provide a command to signal maze regeneration or screen refresh.
4. **Exit Interactive Session**:
   - Allow the user to gracefully terminate the interactive loop and exit the application.

## 3. Component Architecture & Interface Design

### Responsibilities

- **Input Parsing**: Read user keystrokes or menu selections from standard input (`sys.stdin` / `input()`).
- **State Management**: Update renderer display flags (`show_path`, `color_mode`) or trigger callback actions.
- **Display Loop Integration**: Coordinate with `TerminalRenderer.render()` to redraw the maze upon state changes.

### Key Classes & Methods (Conceptual)

```text
+---------------------+       updates flags       +--------------------+
|    InputHandler     | ------------------------> |  TerminalRenderer  |
+---------------------+                           +--------------------+
| - prompt_user()     |                                     |
| - process_command() |                                     v
| - run_loop()        |                            Redraws Terminal
+---------------------+
```

## 4. Proposed Development Steps

1. **Define Command Action Enumeration**:
   - Create an Enum or clear mapping representing supported user actions (`TOGGLE_PATH`, `CHANGE_COLOR`, `REGENERATE`, `QUIT`).
2. **Implement Input Processing Logic**:
   - Build a parser that prompts the user for menu input or key commands and maps valid inputs to corresponding actions.
3. **Connect State Mutations**:
   - Write helper methods to safely mutate renderer display properties (e.g., cycling `color_mode` within valid bounds `0..3`).
4. **Build Interactive Loop**:
   - Implement an interactive loop that redraws the maze, displays command options, processes user choices, and exits cleanly.
5. **Add Comprehensive Docstrings & Types**:
   - Add NumPy-style docstrings following `Docs/python-docstrings_guide.md` and complete static type annotations.

## 5. Verification & Testing Plan

### Automated Tests (`tests/test_display.py`)

- Unit test input parsing with mocked user inputs (using `monkeypatch` or `unittest.mock`).
- Verify that toggling `show_path` correctly updates renderer options.
- Verify that cycling `color_mode` wraps around or validates boundaries `0..3`.

### Manual Verification

- Execute `python -m display.input_handler` to manually test interactive menu commands in the terminal.
