# A-Maze-ing — Project Structure & Team Division

## 1. Project Overview

**A-Maze-ing** is a Python 3.10+ project in which we must generate a maze from a configuration file, save it using the required hexadecimal wall representation, and provide a visual representation with the entrance, exit, and solution path.

The project must support:

- Random maze generation.
- Reproducible generation through a seed.
- `PERFECT=True`: a perfect maze with exactly one path between any two cells.
- `PERFECT=False`: a playable maze with full connectivity and multiple independent routes.
- Validation of maze consistency and configuration errors.
- A visible `42` pattern when the maze is large enough.
- Output in the required hexadecimal format.
- Visual display with regeneration, path visibility, and wall-colour changes.
- A reusable `MazeGenerator` class packaged as `mazegen-*`.
- Type hints, docstrings, `flake8`, `mypy`, tests, a `Makefile`, `.gitignore`, and documentation.

---

# 2. Proposed Project Structure

```text
a-maze-ing/
│
├── a_maze_ing.py                 # Main entry point
├── config.txt                    # Default configuration
├── Makefile
├── README.md
├── LICENSE.md
├── .gitignore
│
├── maze/
│   ├── __init__.py
│   ├── cell.py                   # Cell representation
│   ├── maze.py                   # Maze data structure
│   ├── generator.py              # Maze generation algorithms
│   ├── solver.py                 # Shortest-path calculation
│   ├── validator.py              # Maze/config validation
│   ├── config.py                 # Configuration parser
│   ├── output.py                 # Hexadecimal output format
│   └── pattern_42.py             # 42 pattern generation/validation
│
├── display/
│   ├── __init__.py
│   ├── renderer.py               # Rendering abstraction
│   └── terminal.py               # ASCII terminal renderer
│
├── mazegen/
│   ├── __init__.py
│   └── generator.py              # Reusable MazeGenerator package
│
├── tests/
│   ├── test_config.py
│   ├── test_maze.py
│   ├── test_generator.py
│   ├── test_solver.py
│   ├── test_validator.py
│   └── test_output.py
│
└── dist/
    ├── mazegen-*.whl
    └── mazegen-*.tar.gz
```

> The exact internal structure can be simplified. The important requirement is that the maze generation itself is implemented as a unique reusable class in a standalone module/package, and that the project contains everything required to build the `mazegen-*` package.

---

# 3. Responsibilities

## Member A — Maze Core & Generation

### Main responsibility

Build the **maze engine**: configuration handling, data structures, generation algorithms, validation, and reusable generator package.

### Tasks

- [ ] Design the `Cell` structure.
- [ ] Design the `Maze` structure.
- [ ] Implement the maze grid.
- [ ] Implement wall representation:
  - North
  - East
  - South
  - West
- [ ] Implement the selected maze-generation algorithm.
- [ ] Support deterministic generation using a seed.
- [ ] Implement `PERFECT=True`.
- [ ] Implement `PERFECT=False`.
- [ ] Ensure neighbouring cells have coherent shared walls.
- [ ] Ensure all cells are reachable.
- [ ] Implement the `42` pattern.
- [ ] Validate maze dimensions and coordinates.
- [ ] Validate entry and exit.
- [ ] Implement configuration parsing.
- [ ] Handle invalid configuration gracefully.
- [ ] Implement shortest-path calculation if this is considered part of the maze core.
- [ ] Create the reusable `MazeGenerator` class.
- [ ] Prepare the `mazegen-*` package.
- [ ] Write unit tests for the core logic.

### Main files

```text
maze/cell.py
maze/maze.py
maze/generator.py
maze/config.py
maze/validator.py
maze/pattern_42.py
mazegen/
tests/test_maze.py
tests/test_generator.py
tests/test_config.py
tests/test_validator.py
```

---

# 4. Member B — Output, Visualisation & Project Infrastructure

### Main responsibility

Build everything needed to **use, display, export, test, and document** the generated maze.

### Tasks

- [ ] Implement the terminal/graphical renderer.
- [ ] Display maze walls clearly.
- [ ] Display entry.
- [ ] Display exit.
- [ ] Display the solution path.
- [ ] Implement show/hide solution.
- [ ] Implement maze regeneration.
- [ ] Implement wall-colour changes.
- [ ] Add optional colours for the `42` pattern.
- [ ] Implement hexadecimal output format.
- [ ] Write entry coordinates to the output file.
- [ ] Write exit coordinates to the output file.
- [ ] Write the shortest path to the output file.
- [ ] Ensure every output line ends with `\n`.
- [ ] Create `a_maze_ing.py` integration.
- [ ] Create the `Makefile`.
- [ ] Create `.gitignore`.
- [ ] Set up linting and mypy commands.
- [ ] Create integration tests.
- [ ] Write the main `README.md`.
- [ ] Document the selected algorithm.
- [ ] Document the configuration file.
- [ ] Document how the reusable package works.
- [ ] Document team roles and project planning.
- [ ] Add `LICENSE.md`.

### Main files

```text
display/renderer.py
display/terminal.py
maze/output.py
a_maze_ing.py
Makefile
README.md
LICENSE.md
.gitignore
tests/test_output.py
```

---

# 5. Shared Responsibilities

Some parts should **not** belong exclusively to one person.

Both members should understand and review:

- [ ] The maze data structure.
- [ ] The generation algorithm.
- [ ] The `PERFECT` and non-perfect modes.
- [ ] The wall encoding.
- [ ] The shortest-path algorithm.
- [ ] Configuration parsing.
- [ ] Error handling.
- [ ] The reusable `MazeGenerator` API.
- [ ] The final integration.
- [ ] The README.
- [ ] The test suite.

This is especially important because the assignment explicitly expects students to understand and be able to explain their code during evaluation.

---

# 6. Recommended Git Workflow

Use one branch per major responsibility.

```text
main
│
├── feature/maze-generation
├── feature/config-validation
├── feature/solver
├── feature/output-format
├── feature/renderer
├── feature/tests
└── feature/documentation
```

### Suggested workflow

1. Both members work from `main`.
2. Each member creates feature branches.
3. Small commits with clear messages.
4. Open Pull Requests for important changes.
5. The other member reviews the code.
6. Merge only after both members understand the implementation.
7. Regularly rebase/pull from `main` to avoid large conflicts.
8. Integrate the complete project early rather than waiting until the end.

---

# 7. Integration Order

A good order is:

```text
1. Configuration parser
        ↓
2. Cell / Maze data structures
        ↓
3. Maze generation
        ↓
4. Maze validation
        ↓
5. Shortest-path solver
        ↓
6. Hexadecimal output
        ↓
7. Visual renderer
        ↓
8. User interactions
        ↓
9. Reusable mazegen package
        ↓
10. Tests + lint + mypy
        ↓
11. README + LICENSE
        ↓
12. Final integration and evaluation
```

---

# 8. Alternative Division: Algorithm vs. Interface

If both members prefer a more balanced separation, another possibility is:

## Member A — Algorithm / Backend

Responsible for:

- Configuration parsing
- Maze data structures
- Maze generation
- Perfect maze mode
- Playable maze mode
- Seed support
- Maze validation
- `42` pattern
- Shortest-path algorithm
- Reusable `MazeGenerator`
- Core unit tests

## Member B — Frontend / Application

Responsible for:

- Main program
- Output file generation
- Hexadecimal encoding
- Terminal/MLX rendering
- User interaction
- Path visualisation
- Regeneration
- Colours
- Integration tests
- Makefile
- README
- Package build
- License

### Advantage

This creates a clean architecture:

```text
                 ┌──────────────────┐
                 │   a_maze_ing.py  │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
      ┌──────▼──────┐           ┌──────▼──────┐
      │ Maze Engine │           │  Interface   │
      │   Member A  │           │  Member B    │
      └──────┬──────┘           └──────┬──────┘
             │                         │
             └────────────┬────────────┘
                          │
                   ┌──────▼──────┐
                   │ Final Maze  │
                   └─────────────┘
```

---

# 9. Recommended Division

For two people, the **Algorithm/Backend vs. Interface/Infrastructure** split is recommended.

The maze generator is the most algorithmically important part of the assignment, while rendering, output, packaging, testing, and documentation form a second coherent group.

However, avoid a situation where one person only writes documentation or only writes rendering code. Both members should contribute meaningful programming work.

---

# 10. Minimum Milestones

## Milestone 1 — Skeleton

- [ ] Repository created.
- [ ] Basic folder structure.
- [ ] `a_maze_ing.py`.
- [ ] `Makefile`.
- [ ] Configuration example.
- [ ] Basic tests.

## Milestone 2 — Core Maze

- [ ] Maze representation.
- [ ] Cell representation.
- [ ] Generation algorithm.
- [ ] Seed support.
- [ ] Perfect mode.
- [ ] Non-perfect mode.

## Milestone 3 — Validation & Solver

- [ ] Configuration validation.
- [ ] Maze validation.
- [ ] Wall consistency.
- [ ] Connectivity.
- [ ] Entry/exit validation.
- [ ] Shortest path.
- [ ] `42` pattern.

## Milestone 4 — Output & Display

- [ ] Hexadecimal output.
- [ ] Entry/exit/path output.
- [ ] Visual rendering.
- [ ] Regeneration.
- [ ] Show/hide path.
- [ ] Wall colours.

## Milestone 5 — Reusable Package

- [ ] `MazeGenerator` reusable class.
- [ ] Public API.
- [ ] Package metadata.
- [ ] Build `.whl`.
- [ ] Build `.tar.gz`.
- [ ] Verify installation in a clean virtual environment.

## Milestone 6 — Finalisation

- [ ] Full test suite.
- [ ] `flake8`.
- [ ] `mypy`.
- [ ] Error handling.
- [ ] README.
- [ ] LICENSE.
- [ ] Final peer review.
- [ ] Test with the provided maze analyzer.
- [ ] Final evaluation preparation.

---

# 11. Important Project Requirements

According to the subject, the project must use **Python 3.10 or later**, follow `flake8`, use type hints and `mypy`, handle errors gracefully, and include docstrings. fileciteturn0file0

The program must be executable as:

```bash
python3 a_maze_ing.py config.txt
```

The configuration includes at least:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

A seed may be added for reproducibility. fileciteturn0file0

The generated maze must maintain coherent shared walls, full connectivity, valid entry/exit coordinates, and the required behaviour for perfect and playable modes. fileciteturn0file0

The output format uses one hexadecimal digit per cell. The four bits represent North, East, South, and West walls. After the maze grid, the output contains the entry, exit, and shortest path. fileciteturn0file0

The visual representation must show the maze, entry, exit, and solution path, and provide at least regeneration, path visibility, and wall-colour interaction. fileciteturn0file0

The maze generation must be implemented as a reusable `MazeGenerator` class in a standalone module/package, and the repository must contain the required files to build a `mazegen-*` package. fileciteturn0file0

The README must document the project, execution, configuration, chosen algorithm and its justification, reusable code, team roles, planning, and AI usage. fileciteturn0file0

---

# 12. Final Rule for Collaboration

Do not divide the project into:

> "You write your code and I write my code."

Instead, divide it into **responsibilities**, but continuously review and integrate each other's work.

Both members should be able to explain:

```text
Configuration
      ↓
Maze generation
      ↓
Maze validation
      ↓
Solution
      ↓
Output
      ↓
Visualisation
      ↓
Reusable package
```

This is important because the project may require a small modification during evaluation, and both students should be prepared to understand and modify the implementation.
