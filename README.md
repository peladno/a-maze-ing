_This project has been created as part of the 42 curriculum by skusakab, jperez-u._

# A-Maze-ing

## Description

**A-Maze-ing** is a Python 3.10+ maze generation, solving, and visualization application built as part of the 42 curriculum. The program reads a configuration file, generates a valid 2D maze (either a **perfect maze** with a unique path between any two cells or a **braided playable board** suitable for Pac-Man-style games), calculates the optimal shortest path from entry to exit using Breadth-First Search (BFS), serializes the maze to a file using a 4-bit hexadecimal wall bitmask format, and presents an interactive terminal-based ASCII interface.

### Key Features

- **Dual Generation Modes (§IV.4):**
  - `PERFECT=True`: Generates a perfect maze (spanning tree) with exactly one path between any two reachable cells and zero loops.
  - `PERFECT=False` (the subject's default mode): Generates a braided, playable board with full connectivity, at least two independent loops, and rare or zero dead ends.
- **Embedded "42" Logo:** When the maze dimensions are sufficiently large, cells representing a stylized "42" are reserved and kept fully closed (`0xf`), while guaranteeing corridor connectivity around the pattern. If the maze is too small to fit the logo, generation continues and a warning is printed on standard error.
- **4-Bit Hexadecimal Wall Encoding (§IV.5):** Each cell is encoded as a single hexadecimal character representing its four wall states (North=1, East=2, South=4, West=8; 1 = closed, 0 = open). Adjacent cells always maintain coherent shared wall states.
- **Interactive Terminal Visualizer (§V):** Provides clean ASCII rendering with dynamic color rotation (ANSI palettes), shortest path toggle, dynamic maze regeneration, and graceful exit.
- **Reusable Standalone Package (`mazegen`) (§VI):** The `MazeGenerator` class lives in `maze/generator.py`; the `mazegen` package re-exports it together with the solver, and the wheel and source archive built via Poetry ship both `mazegen` and `maze`.
- **Strict Code Quality & Standards (§III.1):** Enforces 100% type annotations verified with `mypy`, compliance with `flake8` (PEP 8), NumPy-style docstrings (PEP 257), and clear error messages instead of tracebacks for invalid configurations (see the Error Policy).

---

## Instructions

### Setup

Poetry is used for virtual environment management, strict lockfile dependency pinning, and package building.

Install Poetry using the [official Poetry installer](https://python-poetry.org/docs/#installation), then install the project dependencies:

```bash
poetry install
```

With Python 3.10+ installed, this creates Poetry's virtual environment and installs development dependencies (`pytest`, `flake8`, `mypy`). On systems with `make`, run:

```bash
make install
```

### Run

Execute the main application with a configuration file:

```bash
python3 a_maze_ing.py config.txt
```

Alternatively, run through Poetry or Make:

```bash
make run
```

To run through Python's built-in interactive debugger (`pdb`):

```bash
make debug
```

### Controls

After the maze is drawn, a menu waits for one key followed by Enter:

| Key | Action |
| --- | --- |
| `t` | Show or hide the shortest path (green `.` marks) |
| `c` | Cycle the wall colour: none → cyan → yellow → blue |
| `r` | Generate a new maze with a fresh random seed, even when the configuration sets `SEED`. The new seed is printed as `New seed: N`, and `OUTPUT_FILE` is rewritten so that it matches the screen |
| `q` | Quit |

The entry is shown as `E` on a blue background, the exit as `X` on a red background, and the cells of the "42" as magenta `███`.

### Test

Run the automated test suite, static type analysis, and style linters:

```bash
make test         # Run pytest test suite
make lint         # Run flake8 and mypy with subject §III.2 flags
make lint-strict  # Run flake8 and mypy in --strict mode
```

Clean temporary files (`.mypy_cache`, `.pytest_cache`, `dist/`, every `__pycache__` and `*.py[cod]`):

```bash
make clean
```

Build the distributable `mazegen-*` wheel and source archive directly to the repository root as required by §VI:

```bash
make build
```

---

## Configuration file

The program accepts a single configuration file argument (`KEY=VALUE` format, one directive per line). Lines starting with `#` and empty lines are ignored (§IV.3).

### Format & Supported Keys

| Key           | Type                     | Required? | Description                                              | Example                |
| ------------- | ------------------------ | :-------: | -------------------------------------------------------- | ---------------------- |
| `WIDTH`       | Integer ($\ge 1$)        |  **Yes**  | Width of the maze in cells                               | `WIDTH=20`             |
| `HEIGHT`      | Integer ($\ge 1$)        |  **Yes**  | Height of the maze in cells                              | `HEIGHT=15`            |
| `ENTRY`       | `x,y` coordinates        |  **Yes**  | Entry coordinate (origin `0,0` at top-left)              | `ENTRY=0,0`            |
| `EXIT`        | `x,y` coordinates        |  **Yes**  | Exit coordinate (`ENTRY != EXIT`, within bounds)         | `EXIT=19,14`           |
| `OUTPUT_FILE` | String (filename)        |  **Yes**  | Path to the output maze file                             | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | Boolean (`True`/`False`) |  **Yes**  | `True` for perfect maze; `False` for playable loop board | `PERFECT=False`        |
| `SEED`        | Integer                  |    No     | Random seed for deterministic reproducibility            | `SEED=42`              |

With `PERFECT=False` the board must have room for two loops, so it has to be at least 3x2 or 2x3; a smaller one is refused with a `GenerationError`. The "42" is drawn from 9x7 up.

### Coordinate Convention

- The origin `(0, 0)` is at the **top-left corner**.
- `x` represents the horizontal column (`0` to `WIDTH - 1`).
- `y` represents the vertical row (`0` to `HEIGHT - 1`).
- The entire project consistently speaks `(x, y)` across configuration parsing, generator methods, and display renderers; internal transposition to `grid[y][x]` is encapsulated within `Maze`.

### Error Policy (§IV.2)

The configuration, generation and solving steps never end in a raw stack trace: every problem they detect is reported as one line on standard error, and the program exits with code `1`.

- Invalid configuration syntax, missing keys, bad values or out-of-bounds coordinates, and a configuration file that cannot be read raise subclasses of `ConfigError`: `ConfigSyntaxError` (a line that is not `KEY=VALUE`), `ConfigMissingKeyError`, `ConfigValueError` (including duplicate keys) and `ConfigFileError`.
- An error tied to a line reads `source:line: KEY problem`, for example `config.txt:4: WIDTH must be at least 1, got '0'`; missing keys are listed with the file name only.
- The top-level entry point in `a_maze_ing.py` intercepts these errors, prints them to `sys.stderr` prefixed with `Error: `, and terminates with exit code `1`. A missing configuration file is reported the same way.
- Generation and solving report problems with subclasses of `MazeError` instead: `GenerationError` (a size that cannot hold a valid maze) and `SolveError` (an entry or exit placed on the "42", or an exit that cannot be reached). `ConfigError` and `MazeError` are separate families, so the entry point catches both. `SolveError` messages give cells in the `x,y` form of the configuration file.

---

## Maze generation algorithm

We implemented the **Iterative Recursive Backtracker (Depth-First Search)** algorithm, coupled with a targeted **dead-end braiding stage** for the default `PERFECT=False` mode.

### Execution Pipeline

1. **Seed Initialization:** A dedicated `random.Random(seed)` instance is created. If `SEED` is omitted in the config, a random seed is generated and preserved in the `MazeGenerator.seed` property so `a_maze_ing.py` can output it for full reproducibility.
2. **"42" Pattern Reservation:** The pattern is a 7x5 block — a "4" and a "2", each 3 cells wide, with an open column between them, 18 cells in all. From 9x7 up, its top-left is placed at `(WIDTH // 2 - 3, HEIGHT // 2 - 2)`, which puts the open column on the middle column: a centre cell always stays free, a margin of at least one cell keeps the corners free, and every walkable cell stays connected (checked on every size from 9x7 to 60x60). The pattern cells are marked as `reserved`, remain untouched throughout generation, and naturally stay fully closed (`0xf`). On a smaller board the pattern is left out: `maze.reserved` is empty, and the entry point reports it while generation proceeds.
3. **Maze Initialization:** A `Maze` object is initialized where every cell starts with all four walls closed (`15` / `0xf`).
4. **Spanning Tree Carving (DFS):** Starting from `(0, 0)`, which the "42" never covers, the backtracker iteratively visits neighbouring unvisited cells using an explicit, heap-allocated stack. As passages are carved, `Maze.open_passage(a, b)` removes shared walls simultaneously on both adjacent cells. This stage guarantees complete connectivity and reaches every non-reserved cell in $O(V)$ time.
5. **Mode Branching:**
   - If `PERFECT=True`: Generation completes. The resulting maze is a spanning tree with exactly $V - 1$ open passages, zero loops, and exactly one path between entry and exit.
   - If `PERFECT=False` (the subject's default mode): Proceed to Stage 6 (Braiding).
6. **Braid Dead Ends & Enforce Open Space Limits:**
   - Walkable cells with only 1 open passage facing a standard interior cell are identified as "real dead ends" (as defined by `maze_analyzer.py`).
   - Walls at real dead ends are selectively opened to create alternative loops.
   - **Corridor Width Constraint:** Before any wall between cell $a$ and cell $b$ is opened, `_completes_open_3x3(maze, a, b)` verifies that opening the wall will not complete a $3 \times 3$ open area (defined as 9 cells with all 12 internal walls open). Because only the $\le 6$ overlapping $3 \times 3$ windows containing both cells can be affected, this check is executed in constant $O(1)$ time.
   - The list of real dead ends is made once and walked once: opening a wall never creates a dead end, but it can fix two neighbouring dead ends at once, so each cell's open passages are counted again on its turn. Starting from a spanning tree, every wall opened adds exactly one independent loop ($E - V + 1$), so the number of walls opened is the number of loops.
   - On every generated board tested (20x15, 40x30 and 9x7, with and without the "42"), no real dead end is left, which meets the bonus criterion.
7. **Loop Top-Up:** On the smallest boards (3x2, 2x3) one wall can fix both dead ends and leave a single loop. If braiding opened fewer than two walls, further closed walls between walkable cells are opened, one at a time and each checked for $3 \times 3$ areas, until there are two loops.

---

### Why this algorithm

We evaluated three classic spanning-tree algorithms (Recursive Backtracker, Randomized Prim's, and Randomized Kruskal's) and selected the Recursive Backtracker for concrete technical reasons:

1. **Fewer Initial Dead Ends for Braiding:**
   The default and primary mode required by §IV.4 is `PERFECT=False`, which mandates a playable board with rare dead ends.
   - The Recursive Backtracker naturally carves long, winding corridors with high directional persistence, yielding an initial dead-end ratio of only ~10%.
   - In contrast, Randomized Prim's and Kruskal's algorithms grow outward uniformly from frontiers, producing highly branched mazes with ~30% dead ends (roughly $3\times$ more dead ends to eliminate during braiding). Starting with fewer dead ends minimizes the post-processing wall removals required to braid the maze.
2. **Eliminating Recursion Overhead via Explicit Stack:**
   Standard recursive DFS hits Python's default recursion limit (`sys.getrecursionlimit()`, about 1000) on moderate mazes (e.g., $40 \times 40 = 1600$ cells). By implementing the backtracker iteratively using an explicit Python `list` as a stack, execution occurs on the heap with $O(V)$ time and space complexity, completely eliminating recursion limit bottlenecks.
3. **Clean Handling of Non-Rectangular Reserved Zones:**
   Reserving the "42" pattern cells _before_ generation means the backtracker simply treats those coordinates as out-of-bounds. The spanning tree naturally navigates around the obstacle. Carving around reserved cells guarantees perimeter connectivity by construction, avoiding the need to forcefully close cells and repair broken graphs afterwards.
4. **Structural Coherence via Single Mutator:**
   All wall modifications route through `Maze.open_passage(a, b)`. This guarantees that cell $a$'s wall and cell $b$'s opposite wall are updated in a single atomic step, making mismatched neighbour wall encodings mathematically unrepresentable.

---

## Shortest path

The path written at the end of the output file (§IV.5) and shown on screen (§V) comes from a **Breadth-First Search** over open walls, in `maze/solver.py`.

- **Why BFS:** every step costs the same, so this is an unweighted shortest-path problem. Cells wait in a queue (`collections.deque`) and are taken from its front, so they come out in order of their distance from the entry. The first time the exit comes out, no shorter route to it can still be waiting. A depth-first search, like the one that carves the maze, finds _a_ path but not always the shortest. Dijkstra's algorithm and A\* would give the same answer with more machinery.
- **Recovering the path:** each cell records the cell it was reached from when it joins the queue, which also marks it as reached. The path is read back from the exit and reversed. Time and memory are $O(V)$.
- **Two shapes:** `shortest_path` returns the cells (for the display), and `to_directions` turns them into `N`/`E`/`S`/`W` letters (for the file).
- **Ties:** when several shortest paths exist, the fixed neighbour order (N, E, S, W) decides which one is returned, so the same maze always gives the same path.
- **No path:** `SolveError` is raised if the entry or exit lies on the "42", or if the exit cannot be reached.

---

## Reusable module — `mazegen`

The maze generation engine is packaged as a reusable standalone Python module named `mazegen`, as required by Subject §VI. It can be installed into any Python 3.10+ project via `pip`.

### Packaging & Distribution

The package metadata is configured in [`pyproject.toml`](pyproject.toml). Build the distributable `.whl` and `.tar.gz` artifacts at the repository root using:

```bash
make build
# or: poetry build --output .
```

This generates `mazegen-0.1.0-py3-none-any.whl` and `mazegen-0.1.0.tar.gz` at the repository root, ready for distribution and installation:

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

### Licensing

`mazegen` is distributed under the **MIT License** (see [`LICENSE.md`](LICENSE.md)), explicitly permitting unrestricted reuse, modification, and redistribution in downstream projects.

### Basic Usage Example

```python
from mazegen import MazeGenerator, shortest_path, to_directions

# 1. Instantiate the generator with dimensions and options
generator = MazeGenerator(
    width=20,
    height=15,
    perfect=False,  # False for playable braided maze, True for perfect maze
    seed=12345      # Optional: pass an integer for deterministic output
)

# 2. Access the effective seed (auto-generated if not passed)
used_seed = generator.seed
print(f"Generated maze using seed: {used_seed}")

# 3. Generate the maze structure
maze = generator.generate()

# 4. Access the generated grid structure
width = maze.width
height = maze.height
cell_mask = maze.walls_at((0, 0))  # 4-bit integer mask (N=1, E=2, S=4, W=8)
print(f"Top-left cell wall mask: {cell_mask:#x}")

# Iterate over all rows of masks
for row in maze.rows():
    hex_row = "".join(f"{mask:x}" for mask in row)
    print(hex_row)

# 5. Access a solution: the shortest path from entry to exit
entry_point = (0, 0)
exit_point = (19, 14)
cells = shortest_path(maze, entry_point, exit_point)  # [(0, 0), ..., (19, 14)]
letters = to_directions(cells)                         # one N/E/S/W per step
print(f"Shortest path ({len(letters)} steps): {letters}")

# "42" cells are reserved; empty when the board is too small for the pattern
print(f"Pattern cells: {len(maze.reserved)}")
```

Errors are subclasses of `maze.maze.MazeError`: `GenerationError` from `MazeGenerator` and `SolveError` from `shortest_path`. Neither module prints anything; showing the seed or an error is the caller's decision.

---

## Work assignments

### Team Member Roles

The project responsibilities were divided between `skusakab` (So) and `jperez-u` (Javier) according to design seams and module contracts:

- **`skusakab` (So) — Maze Core & Generation Engine (W01–W09, W11–W12, W18, W21; W10, a separate validator, was dropped because the tests and `maze_analyzer.py` cover it):**
  - **Configuration:** Lexical and semantic parsing of `config.txt` (`maze/config.py`), syntax verification, type conversion, and boundary checks.
  - **Data Structure:** `Maze` grid implementation (`maze/maze.py`), `Direction` enum, bitmask manipulation, and the atomic `open_passage` mutator.
  - **Generation:** Iterative DFS backtracker, seed management, "42" pattern placement, braiding with $O(1)$ $3 \times 3$ open area detection, and the loop top-up (`maze/generator.py`).
  - **Solving:** Shortest-path BFS solver producing the path cells and the `NESW` string (`maze/solver.py`).
  - **Testing:** Core unit test suite (`tests/test_config.py`, `tests/test_maze.py`, `tests/test_generator.py`, `tests/test_solver.py`).
- **`jperez-u` (Javier) — Output, Visualisation, CLI & Packaging (W13–W17, W19–W20, W22–W24):**
  - **Output Serialization:** Hexadecimal formatting, file export, and trailing newline enforcement (`output/maze_writer.py`).
  - **Terminal Rendering:** Modular ASCII visualizer (`display/terminal_renderer.py`), ANSI wall coloring palettes, and path overlay.
  - **User Interaction:** Keyboard action handler (`display/input_handler.py`) supporting regeneration, path toggling, and color switching.
  - **Integration & Entry Point:** Command-line argument parsing and error orchestration (`a_maze_ing.py`).
  - **Tooling & Infrastructure:** `Makefile`, `pyproject.toml`, Poetry environment setup, `.gitattributes`, integration tests (`tests/test_output.py`, `tests/test_display.py`), `LICENSE.md`, and project documentation (`README.md`).

---

### Planning and Evolution

1. **Initial Kickoff (2026-08-13):**
   - Targeted a 1-month development cycle (deadline: 2026-09-17).
   - Originally agreed on Python's built-in `venv` + `pip` with `requirements.txt`.
   - Outlined modular separation between backend generation and frontend visualization.
2. **Transition to Poetry (2026-08-20 / Decision 2.1):**
   - Javier proposed and implemented Poetry via `pyproject.toml` and `poetry.lock`.
   - _Rationale:_ Deterministic dependency resolution across different development operating systems (Windows and Linux), clean separation of developer tooling (`flake8`, `mypy`, `pytest`) from runtime dependencies, and standardized wheel builds satisfying §VI. Documented in [`Docs/pair_communication/03_poetry_switch.md`](Docs/pair_communication/03_poetry_switch.md).
3. **Data Structure & Unified Coordinate System (2026-08-21 to 2026-09-02):**
   - The team initially considered converting coordinates at boundaries between `(x, y)` and `[row][col]`.
   - _Evolution:_ Unified the entire project around `(x, y)` tuples (`Coord = tuple[int, int]`). The internal transposition to `_grid[y][x]` is completely encapsulated inside `Maze`, eliminating transpose bugs on non-square mazes.
4. **Invariant Enforcement via Single Mutator (2026-08-24):**
   - To guarantee that shared walls between adjacent cells never disagree (§IV.4), `Maze` makes cell wall masks read-only to external callers. The only way to open a wall is `Maze.open_passage(a, b)`, which updates both neighbouring cells atomically.
5. **Refinement of Stage 6 Braiding & Open Area Constraints (2026-09-01 to 2026-09-13):**
   - Analysis of `maze_analyzer.py` revealed that loop count is strictly $E - V + 1$, and that dead ends facing border walls or the "42" pattern are classified as enclosed rather than real.
   - Rigorously defined a $3 \times 3$ open area as 9 cells with all 12 internal walls open.
   - Transitioned from a generate-and-retry strategy to a constant-time pre-check (`_completes_open_3x3`) evaluating at most 6 windows before opening any wall during braiding.
6. **Encapsulation of Reusable Module Seed Printing (2026-09-13):**
   - Established that `MazeGenerator` must remain quiet and free of side effects. The seed is exposed via a property, and only `a_maze_ing.py` prints it to `stdout`.
7. **Loop Top-Up for the Smallest Boards (2026-09-15):**
   - Braiding one 3x2 path showed that a single wall can fix both dead ends and leave one loop, on a size the generator accepts. Rather than raising the minimum size, a final stage opens the missing walls. Because a tree has exactly $V - 1$ passages, the number of walls braiding opened already gives the loop count, so nothing is counted twice.
8. **The "42" Shape and Placement (2026-09-15):**
   - The shape was read from the subject's image. The first placement rule was explained with a wrong argument about 8-wide boards; checking every size by script corrected it, and the 9x7 bound was kept as a simple margin rule even though 9x6 would also work.
9. **Solver Design (2026-09-17, kickoff item 3.8):**
   - BFS in the engine, exposed as functions in `maze/solver.py` rather than as a `MazeGenerator` method, since §VI asks the module for access to a solution. Cells and letters come from separate functions, and a missing path raises `SolveError` rather than returning `None`.
10. **Schedule (2026-09-17):**
    - The original one-month deadline did not leave time to review the integration of both halves, so it was extended; the new date is still to be fixed.

---

### What Worked Well & What Could Be Improved

#### What Worked Well

- **Contract-First Implementation:** Drafting architecture specifications in `Docs/implementation_plans/` before writing code allowed both members to work in parallel on opposite sides of interfaces without integration friction.
- **Bilingual Documentation & Work Logs:** Maintaining daily logs in `Docs/work_log/` and bilingual guides in `Docs/learning_log/` bridged communication across native languages (Japanese and Spanish) and provided complete audit trails of technical decisions.
- **Correct-by-Construction Design:** Designing `open_passage` to update both sides of a wall and reserving "42" cells prior to DFS eliminated entire categories of wall-incoherence and graph-disconnection bugs.
- **Independent Validation via `maze_analyzer.py`:** Incorporating the evaluation analyzer into the verification loop ensured objective validation against grading standards.

#### What Could Be Improved

- **Cross-Platform Makefile Quirks:** Developing across different environments (Windows PowerShell vs Unix) led to early line ending (`CRLF`) and tab issues in `Makefile`. This was resolved by committing a comprehensive `.gitattributes` file and explicit LF configurations.
- **Git Workflow Formalization:** Choosing direct branch merges over Pull Requests (Decision 1.2 = A) sped up rapid iteration but required conscious manual discipline to review the peer's diffs. Formalizing PR reviews for shared contracts earlier would have provided extra visibility.

### Tools Used

- **Runtime & Language:** Python 3.10+
- **Dependency & Build Management:** Poetry (`poetry-core`)
- **Automation:** GNU Make
- **Testing:** `pytest`
- **Code Quality:** `flake8` (PEP 8 style guide), `mypy` (strict static typing)
- **Version Control & Collaboration:** Git, GitHub
- **IDE & Development:** Visual Studio Code
- **Validation:** `maze_analyzer.py` (official 42 verification tool)
- **Generative AI:** Claude (learning explanations, bilingual drafting, design review)

---

## Resources

### References & Documentation

- **Books & Algorithms:**
  - Jamis Buck, _Mazes for Programmers: Code Your Own Twisty Little Mazes_ (The Pragmatic Bookshelf, 2015) — foundational reference for the Recursive Backtracker, spanning trees, braiding techniques, and loop metrics.
  - Cormen, Leiserson, Rivest, and Stein, _Introduction to Algorithms_ (MIT Press) — Breadth-First Search (BFS) and topological properties of undirected graphs.
- **Python Official Documentation & PEPs:**
  - [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
  - [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/) (NumPy Docstring Standard)
  - [Python `dataclasses` and `enum` modules](https://docs.python.org/3/library/dataclasses.html)
  - [Python `typing` and Type Hints Guide](https://docs.python.org/3/library/typing.html)
- **Packaging:**
  - [Python Packaging User Guide](https://packaging.python.org/) & [Poetry Documentation](https://python-poetry.org/docs/)
- **Queues and BFS:**
  - [Python tutorial — Using Lists as Queues](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues)
  - [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque)

---

### AI Usage (§II & §VII)

In accordance with Subject §II and §VII, AI assistance (specifically Claude) was utilized strategically as a learning and pair-programming productivity tool:

#### Specific Tasks & Modules Supported by AI

1. **Bilingual Learning Logs (`Docs/learning_log/`):**
   - AI drafted comprehensive technical explainers and comparative analyses covering Python language mechanics, bitmask operations, generator execution timing, and algorithm trade-offs (e.g., `bitmask-wall-encoding.md`, `maze-generation-algorithms.md`, `python-enum-and-property.md`, `python-exceptions.md`, `python-generators.md`).
2. **Design Specification & Edge-Case Brainstorming:**
   - Assisted in formulating contract specifications in `Docs/implementation_plans/`, particularly mapping out the 31 edge cases in `config-parser.md` and calculating the 6 checking windows for $3 \times 3$ open area constraints in `generation-algorithm.md`.
3. **Docstring Formatting & Typing Assistance:**
   - Generated standardized NumPy-style docstrings and clarified complex `mypy` typing questions (such as `@property` declarations in `typing.Protocol` interfaces).
4. **Cross-Language Communication:**
   - Assisted in translating technical notes and decision rationales between Japanese and English, ensuring equal shared understanding across both team members.
5. **Generator and Solver (so's side):**
   - The implementation code was written by so; Claude explained concepts (spanning trees, loops, queues, BFS), reviewed each version, and pointed out bugs with hints rather than fixes.
   - Claude wrote part of the test suite (the braiding, loop top-up, "42" and solver tests), and checked every test file by mutation testing: breaking the code on purpose, one change at a time, to confirm that some test fails.
   - Claude drafted the docstrings, the user-facing error messages, the solver plan (`Docs/implementation_plans/shortest-path-solver.md`) and the learning note on queues and BFS, and ran generated mazes through `maze_analyzer.py`.

#### Principles & Verification

- **Full Human Ownership:** No code was committed without complete line-by-line understanding. Both team members reviewed, modified, and verified all algorithm implementations and mathematical proofs.
- **Zero Hallucination Acceptance:** AI-generated suggestions (such as early claims regarding Poetry in `poetry_proposal.md`) were fact-checked against the official subject PDF and corrected whenever inaccuracies were detected.
- **Defense Readiness (§IX):** Both members possess the complete theoretical and practical knowledge required to explain, justify, and modify any component of the codebase during peer evaluation.

---

## 日本語

### 概要

**A-Maze-ing** は、42 カリキュラムの課題として Python 3.10+ で開発された迷路生成・探索・可視化プログラムです。設定ファイルを読み込み、2次元迷路（任意の2点間の経路が1本のみ存在する**完全迷路**、またはパックマンのゲームに適したループを持つ**遊べる盤面**）を生成し、幅優先探索（BFS）による最短経路を計算して、各セルの壁情報を 16 進数ビットマスク形式でファイルに出力します。さらに、ターミナル上でのインタラクティブな ASCII 描画機能を提供します。

#### 主な機能

- **2つの生成モード (§IV.4):**
  - `PERFECT=True`: 全域木として迷路を生成し、入口と出口の間にちょうど 1 本の経路を持つ完全迷路（ループなし）。
  - `PERFECT=False`（subject の既定モード）: 完全な連結性を保ちつつ、2本以上の独立したループを持ち、行き止まりを最小限（2個以下、ボーナスで0個）に抑えた遊べる盤面。
- **「42」パターンの描画:** 盤面のサイズが十分な場合、中央付近に完全に閉じたセル（`0xf`）で「42」の形状を埋め込み、その周囲に通路を形成します。サイズが不足する場合は標準エラー出力に警告を表示し、パターンを省略して生成を継続します。
- **16進数ウォール表現 (§IV.5):** 各セルの方位ごとの壁（北=1, 東=2, 南=4, 西=8; 閉=1, 開=0）を 1 桁の 16 進数で出力します。隣接するセル間で共有壁の状態は常に一致します。
- **ターミナル ASCII 可視化 (§V):** 壁の色変更（ANSI エスケープシーケンス）、最短経路の表示/非表示切り替え、迷路の再生成、終了などのインタラクティブ操作が可能です。
- **再利用可能モジュール `mazegen` (§VI):** クラス `MazeGenerator` は `maze/generator.py` にあり、`mazegen` パッケージがソルバーとともに再公開しています。Poetry でビルドする `.whl` と `.tar.gz` には、`mazegen` と `maze` の両方が入ります。
- **厳格なコーディング規約 (§III.1):** すべての関数に型ヒント（`mypy` 準拠）、`flake8`（PEP 8）準拠、NumPy スタイルの docstring（PEP 257）を適用し、不正な設定に対しては traceback ではなく分かりやすいエラーメッセージを表示します（エラー処理方針を参照）。

---

### 使い方(セットアップ / 実行 / テスト)

#### セットアップ

仮想環境の管理・依存関係の固定・パッケージビルドには Poetry を使用します。[Poetry 公式インストーラ](https://python-poetry.org/docs/#installation)で Poetry を導入後、以下を実行します:

```bash
poetry install
```

`make` が利用可能な環境では以下でも同一の操作が可能です:

```bash
make install
```

#### 実行

設定ファイルを引数に指定してメインスクリプトを実行します:

```bash
python3 a_maze_ing.py config.txt
# または
make run
```

Python 組み込みデバッガ (`pdb`) で実行する場合:

```bash
make debug
```

#### 操作方法

迷路が表示された後、メニューがキー 1 つと Enter を待ちます:

| キー | 操作 |
| --- | --- |
| `t` | 最短経路（緑の `.`）の表示/非表示 |
| `c` | 壁の色を切り替える:なし → シアン → 黄 → 青 |
| `r` | 新しいランダムなシードで迷路を作り直す（設定に `SEED` があっても）。新しいシードを `New seed: N` と表示し、画面と一致するよう `OUTPUT_FILE` も書き直す |
| `q` | 終了 |

入口は青背景の `E`、出口は赤背景の `X`、「42」のセルはマゼンタの `███` で表示されます。

#### テストとビルド

```bash
make test         # pytest によるテスト実行
make lint         # flake8 および mypy による静的検証
make lint-strict  # mypy --strict を含む厳格検証
make clean        # キャッシュ・dist/・__pycache__・*.py[cod] の削除
make build        # リポジトリ直下に mazegen-* 配布パッケージをビルド
```

---

### 設定ファイル

設定ファイルは 1 行につき 1 つの `KEY=VALUE` 形式で記述します。`#` から始まる行および空行は無視されます (§IV.3)。

#### 設定項目一覧

| キー          | 型                      |   必須   | 説明                                    | 指定例                 |
| ------------- | ----------------------- | :------: | --------------------------------------- | ---------------------- |
| `WIDTH`       | 整数 ($\ge 1$)          | **必須** | 迷路の幅（セル数）                      | `WIDTH=20`             |
| `HEIGHT`      | 整数 ($\ge 1$)          | **必須** | 迷路の高さ（セル数）                    | `HEIGHT=15`            |
| `ENTRY`       | `x,y` 座標              | **必須** | 入口座標（左上が原点 `0,0`）            | `ENTRY=0,0`            |
| `EXIT`        | `x,y` 座標              | **必須** | 出口座標（範囲内かつ `ENTRY != EXIT`）  | `EXIT=19,14`           |
| `OUTPUT_FILE` | 文字列（パス）          | **必須** | 出力先ファイル名                        | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | 真偽値 (`True`/`False`) | **必須** | `True` で完全迷路、`False` で遊べる盤面 | `PERFECT=False`        |
| `SEED`        | 整数                    |   任意   | 再現性のための乱数シード値              | `SEED=42`              |

`PERFECT=False` では盤面にループ 2 本分の余地が必要なので、3x2 か 2x3 以上でなければなりません。それより小さいと `GenerationError` で拒否されます。「42」は 9x7 以上で描かれます。

#### 座標系規約

- 原点 `(0, 0)` は**左上隅**です。`x` は列（横方向）、`y` は行（縦方向）を表します。
- プログラム全体（パーサ、生成器、描画器）で `(x, y)` 順を一貫して採用し、内部配列 `_grid[y][x]` への転置は `Maze` クラス内に完全に隠蔽されています。

#### エラー処理方針 (§IV.2)

- 設定・生成・経路探索で検出した問題は、traceback を出さずに 1 行のメッセージとして標準エラー出力へ表示し、終了コード `1` で終了します。
- 構文エラー、必須キーの欠落、不正な値や範囲外の座標、読めない設定ファイルに対しては、自前の `ConfigError` サブクラスを送出します:`ConfigSyntaxError`（`KEY=VALUE` でない行）、`ConfigMissingKeyError`、`ConfigValueError`（重複キーを含む）、`ConfigFileError`。
- 行に結びつくエラーは `source:line: KEY 問題` の形式です（例:`config.txt:4: WIDTH must be at least 1, got '0'`）。必須キーの欠落はファイル名だけを示します。エントリポイントはメッセージの前に `Error: ` を付けて表示します。設定ファイルが見つからない場合も同じように報告します。
- 生成と経路探索の問題は `MazeError` の子クラスで伝えます:`GenerationError`(妥当な迷路を作れない大きさ)と `SolveError`(入口か出口が「42」の上、または出口に届かない)。`ConfigError` と `MazeError` は別の系統なので、エントリポイントは両方を捕まえます。`SolveError` のメッセージは、セルを設定ファイルと同じ `x,y` の形で示します。

---

### 生成アルゴリズムと選定理由

#### 採用アルゴリズム

**再帰的バックトラッカー（深さ優先探索 / DFS）** を明示的スタックによる反復処理で実装し、既定モード（`PERFECT=False`）向けに**行き止まり解消（braiding）処理**を組み合わせています。

1. **シード解決:** 専用の `random.Random(seed)` インスタンスを生成。未指定時は乱数シードを自動生成し、呼び出し元が表示・再利用できるようにプロパティとして保持。
2. **「42」パターンの確保:** パターンは 7x5 のブロック(幅 3 の「4」と「2」の間に空き列 1 列、計 18 セル)。9x7 以上の盤面で、左上を `(WIDTH // 2 - 3, HEIGHT // 2 - 2)` に置く。空き列が真ん中の列に重なるので中央のセルは必ず空き、周囲に 1 セル以上の余白が残るので四隅も空き、歩けるセルはすべてつながる(9x7〜60x60 の全サイズでスクリプトにより確認)。該当セルは予約領域となり、全壁閉の `0xf` のまま残る。これより小さい盤面ではパターンを省き(`maze.reserved` が空になる)、エントリポイントがその旨を表示する。
3. **迷路の初期化:** すべてのセルが 4 方向の壁を閉じた状態（`15` / `0xf`）の `Maze` を作る。
4. **全域木の掘削 (DFS):** 「42」が決して覆わない `(0, 0)` から始め、未訪問のセルを探索しながら `Maze.open_passage(a, b)` で壁を開放。反復処理により、Python の再帰深度上限（約1000）を回避。
5. **分岐:** `PERFECT=True` の場合は全域木（ループ数0、経路1本）の時点で完了。`PERFECT=False` の場合は 6 の braiding へ進む。
6. **Braiding (既定モード):** 本物の行き止まり（外周や42パターン以外に面する壁を持つセル）を選択的に開放し、2本以上の独立ループを形成。開放前に `_completes_open_3x3` により最大6個の $3 \times 3$ 枠を $O(1)$ で検査し、幅2を超える開放領域が絶対に生成されないよう構造的に保証。行き止まりの一覧は 1 回作って 1 周する。壁を開けても行き止まりは増えないが、隣り合う 2 つが 1 枚で同時に直ることがあるので、各セルの通路はその順番が来たときに数え直す。木から始めるので、開けた壁の枚数がそのままループの数になる。テストした盤面(20x15、40x30、9x7、「42」の有無とも)では本物の行き止まりは 0 個で、ボーナスの基準を満たした。
7. **ループの補充:** 最小の盤面(3x2、2x3)では、壁 1 枚で両方の行き止まりが直り、ループが 1 本しか残らないことがある。braiding が開けた壁が 2 枚未満なら、歩けるセルどうしの閉じた壁を 1 枚ずつ、毎回 3x3 を確かめてから開け、ループを 2 本にする。

#### 選定理由

- **初期行き止まりの少なさ:** 既定モード（`PERFECT=False`）では行き止まりを潰す必要があります。再帰的バックトラッカーは通路が長く伸びる特性上、初期状態の行き止まり率が約 10% と極めて低く（Prim 法や Kruskal 法は約 30%）、braiding で取り除くべき壁の枚数を大幅に削減できます。
- **反復版による再帰深度の克服:** 明示的なスタック（ヒープメモリ上のリスト）を使用することで、大きな盤面でもスタックオーバーフローを起こさず線形時間 $O(V)$ で安定動作します。
- **非矩形領域への適応性:** 「42」パターンのセルを初期段階で範囲外扱いとするだけで、バックトラッカーはその周囲を自然に迂回して木を構成でき、後から壁を閉じてグラフを修復する手間やリスクが発生しません。
- **共有壁の整合性保証:** 壁の変更を `Maze.open_passage` の1箇所に集約することで、隣接する両セルの壁ビットが同時に更新され、壁の食い違い（不整合）が原理的に発生しません。

---

### 最短経路

出力ファイルの最後(§IV.5)と画面(§V)に出す経路は、`maze/solver.py` の**幅優先探索 (BFS)** で求めます。

- **BFS を選んだ理由:** どの一歩もコストが同じなので、重みなしの最短経路問題になります。セルはキュー(`collections.deque`)に並び、先頭から取り出されるので、入口からの距離の順に出てきます。出口が初めて出てきたとき、それより短い道はもう待っていません。迷路を掘るのに使った深さ優先探索は「ある道」を見つけますが、最短とは限りません。ダイクストラ法や A\* は、同じ答えをより多くの仕組みで出すことになります。
- **経路の取り出し:** 各セルは、キューに入るときに「どのセルから来たか」を記録し、それが到達済みの印も兼ねます。経路は出口からその記録をたどって反転します。時間・メモリとも $O(V)$ です。
- **2 つの形:** `shortest_path` はセルを返し(表示用)、`to_directions` がそれを `N`/`E`/`S`/`W` の文字にします(ファイル用)。
- **同じ長さの経路が複数あるとき:** 隣を見る順番(N, E, S, W)が固定なので、同じ迷路からは常に同じ経路が返ります。
- **経路が無いとき:** 入口か出口が「42」の上にある場合と、出口に届かない場合は `SolveError` を送出します。

---

### 再利用モジュール `mazegen`

迷路生成ロジックは、独立した Python パッケージ `mazegen` 内の単一クラス `MazeGenerator` として実装されています (§VI)。

#### パッケージビルドとインストール

```bash
make build
# リポジトリ直下に mazegen-0.1.0-py3-none-any.whl および .tar.gz が生成されます
pip install mazegen-0.1.0-py3-none-any.whl
```

#### ライセンス

本モジュールは **MIT License** ([`LICENSE.md`](LICENSE.md)) の下で公開されており、後続プロジェクトでの自由な再利用および再配布が明示的に許諾されています。

#### コード例

```python
from mazegen import MazeGenerator, shortest_path, to_directions

# インスタンス化 (カスタムパラメータ: サイズ、モード、シード)
gen = MazeGenerator(width=20, height=15, perfect=False, seed=42)

# 迷路の生成
maze = gen.generate()
print(f"使用シード値: {gen.seed}")

# 構造へのアクセス
for row in maze.rows():
    print("".join(f"{mask:x}" for mask in row))

# 解へのアクセス: 入口から出口への最短経路
cells = shortest_path(maze, (0, 0), (19, 14))   # セルの並び
letters = to_directions(cells)                  # NESW 文字列
print(f"最短経路: {letters}")
```

エラーは `maze.maze.MazeError` の子クラスで、`MazeGenerator` からは `GenerationError`、`shortest_path` からは `SolveError` が送出されます。どちらのモジュールも何も表示しません。シードやエラーを表示するかは呼び出し側が決めます。

---

### 役割分担と進め方

#### 役割分担

- **`skusakab` (So) — コアエンジン & 生成ロジック (W01–W09, W11–W12, W18, W21。W10 の独立した検証器は、テストと `maze_analyzer.py` で代えられるため取りやめ):**
  - 設定パースおよび検証 (`maze/config.py`)
  - 迷路データ構造・壁ビットマスク・`open_passage` (`maze/maze.py`)
  - 迷路生成アルゴリズム・シード・「42」の配置・braiding・ループの補充 (`maze/generator.py`)
  - 最短経路探索 BFS ソルバ(経路のセルと NESW 文字列) (`maze/solver.py`)
  - コア単体テスト群 (`tests/test_config.py`, `tests/test_maze.py`, `tests/test_generator.py`, `tests/test_solver.py`)
- **`jperez-u` (Javier) — 出力・可視化・CLI・インフラ・パッケージング (W13–W17, W19–W20, W22–W24):**
  - 16進数出力およびメタデータ書き出し (`output/maze_writer.py`)
  - ターミナル ASCII レンダラー・色パレット・操作ハンドラ (`display/`)
  - メイン CLI 統合 (`a_maze_ing.py`)
  - Poetry / Makefile / `.gitattributes` の整備、`mazegen` のパッケージング
  - 出力および表示のテスト群 (`tests/test_output.py`, `tests/test_display.py`)
  - ライセンス選定 (`LICENSE.md`) およびプロジェクトドキュメント (`README.md`)

#### 計画の変遷

1. **キックオフ (2026-08-13):** 9/17 を締切とする約1か月の計画を策定。当初は `venv` + `pip` を採用予定でした。
2. **Poetry への移行 (2026-08-20 / 決定 2.1):** 異なる開発環境（Windows と Linux）での依存関係の完全な固定、開発ツールと実行時依存の分離、§VI のパッケージ配布を容易にするため、Javier の提案・実装により Poetry へ移行しました（[`Docs/pair_communication/03_poetry_switch.md`](Docs/pair_communication/03_poetry_switch.md)）。
3. **データ構造と座標系の統一 (2026-08-21〜2026-09-02):** 当初は境界で `(x, y)` と `[y][x]` を変換する計画でしたが、`Maze` クラスが内部で転置を吸収し、プロジェクト全体で `(x, y)` 順に統一することで座標変換バグを防止しました。
4. **不変条件の構造的保証 (2026-08-24):** 壁の不整合を防ぐため、壁の変更を `Maze.open_passage` の1つのみに制限しました。
5. **Braiding と 3x3 領域判定の洗練 (2026-09-01〜2026-09-13):** 3x3 開放領域を「内壁12枚がすべて開いている状態」と明確に定義し、壁開放時に影響を受ける最大6つの枠のみを判定する定数時間 $O(1)$ の判定法を確立しました。
6. **シード出力の責務分離 (2026-09-13):** 再利用ライブラリとしての純粋性を保つため、`MazeGenerator` は標準出力への出力を一切行わず、エントリポイントがプロパティからシードを取得して表示する設計に決定しました。
7. **最小の盤面のためのループ補充 (2026-09-15):** 3x2 の一本道に braiding をかけると、壁 1 枚で両方の行き止まりが直り、生成器が受け入れる大きさなのにループが 1 本しか残らないことが分かりました。最小サイズを引き上げる代わりに、足りない壁を開ける最終工程を加えました。木の通路はちょうど $V - 1$ 本なので、braiding が開けた壁の枚数がそのままループの数になり、数え直しは不要です。
8. **「42」の形と配置 (2026-09-15):** 形は subject の画像から読み取りました。最初の配置規則は幅 8 の盤面についての誤った理由で説明していましたが、全サイズをスクリプトで確かめて訂正しました。9x6 でも成り立つことが分かりましたが、「四方に 1 セルの余白」という単純な規則として 9x7 の境界を残しました。
9. **ソルバーの設計 (2026-09-17、キックオフ論点 3.8):** BFS はエンジン側に置き、`MazeGenerator` のメソッドではなく `maze/solver.py` の関数として公開しました。§VI が解へのアクセスを求めているのはモジュールだからです。セルと文字は別の関数で作り、経路が無い場合は `None` を返さず `SolveError` を送出します。
10. **日程 (2026-09-17):** 当初の 1 か月の締切では、両者の成果物を統合してレビューする時間が足りないため延長しました。新しい日程は未定です。

#### うまくいったこと / 改善できたこと

- **うまくいったこと:** コード実装前に `Docs/implementation_plans/` でインターフェース契約を綿密に定義したことで、モジュール統合時の不整合がほぼゼロに抑えられました。また、日々の作業ログ (`Docs/work_log/`) とバイリンガル解説 (`Docs/learning_log/`) により、言語差（日本語とスペイン語/英語）を超えて円滑に協働できました。
- **改善できたこと:** Windows 環境と Linux 環境における改行コード（CRLF）や Make のタブ文字問題で序盤に手戻りが発生したため、`.gitattributes` の導入を初期段階で行うべきでした。また、PR を介さない直マージ運用を採ったため、相手のコードを能動的に読み込む規律が強く求められました。

#### 使用したツール

- Python 3.10+, Poetry, Make, pytest, flake8, mypy, Git, GitHub, VS Code, `maze_analyzer.py`, Claude AI

---

### 参考資料 / AI の使い方

#### 参考資料

- Jamis Buck, _Mazes for Programmers_ (Pragmatic Bookshelf, 2015) — 全域木、バックトラッカー、braiding の基礎理論
- グラフ理論と全域木の性質（独立な閉路の数 $E - V + 1$。巡回数とも呼ばれる）
- 幅優先探索 (BFS) 最短経路アルゴリズム
- Python 公式ドキュメント (PEP 8, PEP 257, dataclasses, enum, typing, random, `collections.deque`)

#### AI の使い方 (§II & §VII)

42 の AI 指針 (§II) に従い、Claude をペアプログラミング・学習支援ツールとして活用しました:

- **学習ノートの草稿作成 (`Docs/learning_log/`):** ビット演算、Python の型システム、ジェネレータの評価タイミング、例外設計などの概念整理とバイリンガル解説の作成。
- **設計仕様の洗練とエッジケースの洗い出し:** `config-parser.md` の 31 個のエッジケースや、`generation-algorithm.md` の 3x3 判定アルゴリズムの幾何的検討。
- **Docstring と型ヒントの整理:** PEP 257 (NumPy スタイル) の docstring 整備や `mypy` エラーの原因究明。
- **ペア間コミュニケーション支援:** 日本語と英語の技術文書の相互翻訳およびニュアンスの確認。
- **生成器とソルバー(so の担当):** 実装コードは so が書き、Claude は概念の解説(全域木、ループ、キュー、BFS)、各版のレビュー、バグの指摘(修正ではなくヒント)を行いました。テストの一部(braiding、ループの補充、「42」、ソルバー)は Claude が書き、すべてのテストファイルをミューテーションテスト(コードをわざと 1 か所ずつ壊し、いずれかのテストが失敗することを確かめる)で検証しました。docstring、利用者向けのエラーメッセージ、ソルバーの計画書 (`Docs/implementation_plans/shortest-path-solver.md`)、キューと BFS の学習ノートの草稿も Claude が作成し、生成した迷路を `maze_analyzer.py` で検証しました。

AI 生成のコードを無批判に導入することは厳に戒め、すべてのアルゴリズム・不変条件・テストケースについてチーム両名が論理的に説明・検証できる状態を保っています。ディフェンス (§IX) における口頭試問およびライブコーディング修正にも十分に対応できる理解を備えています。

---

Documentation for our own process (work logs, learning notes, design plans) lives in [`Docs/`](Docs/README.md).
私たちの作業記録(作業ログ・学習ノート・設計計画)は [`Docs/`](Docs/README.md) にある。
