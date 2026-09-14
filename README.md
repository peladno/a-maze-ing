_This project has been created as part of the 42 curriculum by skusakab, jperez-u._

# A-Maze-ing

## Description

**A-Maze-ing** is a Python 3.10+ maze generation, solving, and visualization application built as part of the 42 curriculum. The program reads a configuration file, generates a valid 2D maze (either a **perfect maze** with a unique path between any two cells or a **braided playable board** suitable for Pac-Man-style games), calculates the optimal shortest path from entry to exit using Breadth-First Search (BFS), serializes the maze to a file using a 4-bit hexadecimal wall bitmask format, and presents an interactive terminal-based ASCII interface.

### Key Features

- **Dual Generation Modes (§IV.4):**
  - `PERFECT=True`: Generates a perfect maze (spanning tree) with exactly one path between any two reachable cells and zero loops.
  - `PERFECT=False` (default): Generates a braided, playable board with full connectivity, at least two independent loops, and rare or zero dead ends.
- **Embedded "42" Logo:** When the maze dimensions are sufficiently large, cells representing a stylized "42" are reserved and kept fully closed (`0xf`), while guaranteeing corridor connectivity around the pattern. If the maze is too small to fit the logo, generation continues gracefully with a clear informational message.
- **4-Bit Hexadecimal Wall Encoding (§IV.5):** Each cell is encoded as a single hexadecimal character representing its four wall states (North=1, East=2, South=4, West=8; 1 = closed, 0 = open). Adjacent cells always maintain coherent shared wall states.
- **Interactive Terminal Visualizer (§V):** Provides clean ASCII rendering with dynamic color rotation (ANSI palettes), shortest path toggle, dynamic maze regeneration, and graceful exit.
- **Reusable Standalone Package (`mazegen`) (§VI):** Maze generation logic is encapsulated in a standalone class within the `mazegen` package, distributable as a Python wheel and source archive built via Poetry.
- **Strict Code Quality & Standards (§III.1):** Enforces 100% type annotations verified with `mypy`, compliance with `flake8` (PEP 8), NumPy-style docstrings (PEP 257), and zero unhandled crashes on invalid inputs.

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

### Test

Run the automated test suite, static type analysis, and style linters:

```bash
make test         # Run pytest test suite
make lint         # Run flake8 and mypy with subject §III.2 flags
make lint-strict  # Run flake8 and mypy in --strict mode
```

Clean temporary caches (`.mypy_cache`, `.pytest_cache`, `dist/`):

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

### Coordinate Convention

- The origin `(0, 0)` is at the **top-left corner**.
- `x` represents the horizontal column (`0` to `WIDTH - 1`).
- `y` represents the vertical row (`0` to `HEIGHT - 1`).
- The entire project consistently speaks `(x, y)` across configuration parsing, generator methods, and display renderers; internal transposition to `grid[y][x]` is encapsulated within `Maze`.

### Error Policy (§IV.2)

The application adheres to a strict error-handling contract: it will **never crash with an unhandled exception or raw stack trace**.

- Invalid configuration syntax, duplicate keys, missing keys, out-of-bounds coordinates, or unreachable file paths raise specialized subclasses of `ConfigError` (`ConfigSyntaxError`, `ConfigMissingKeyError`, `ConfigValueError`, `ConfigFileError`).
- Every configuration error provides exact location context formatted as `source:line: problem`.
- The top-level entry point in `a_maze_ing.py` intercepts errors, displays a clear, human-readable error message to `sys.stderr`, and terminates with exit code `1`.

---

## Maze generation algorithm

We implemented the **Iterative Recursive Backtracker (Depth-First Search)** algorithm, coupled with a targeted **dead-end braiding stage** for the default `PERFECT=False` mode.

### Execution Pipeline

1. **Seed Initialization:** A dedicated `random.Random(seed)` instance is created. If `SEED` is omitted in the config, a random seed is generated and preserved in the `MazeGenerator.seed` property so `a_maze_ing.py` can output it for full reproducibility.
2. **"42" Pattern Reservation:** If the grid is large enough (at least 5 rows tall and 13 columns wide) and does not overlap the 4 corners or all center candidates, the pattern cells are computed and marked as `reserved`. These cells remain untouched throughout generation and naturally stay fully closed (`0xf`). If the grid is too small, an informational warning is issued and generation proceeds without the logo.
3. **Maze Initialization:** A `Maze` object is initialized where every cell starts with all four walls closed (`15` / `0xf`).
4. **Spanning Tree Carving (DFS):** Starting from an unreserved cell, the backtracker iteratively visits neighbouring unvisited cells using an explicit, heap-allocated stack. As passages are carved, `Maze.open_passage(a, b)` removes shared walls simultaneously on both adjacent cells. This stage guarantees complete connectivity and reaches every non-reserved cell in $O(V)$ time.
5. **Mode Branching:**
   - If `PERFECT=True`: Generation completes. The resulting maze is a spanning tree with exactly $V - 1$ open passages, zero loops, and exactly one path between entry and exit.
   - If `PERFECT=False` (default): Proceed to Stage 6 (Braiding).
6. **Braid Dead Ends & Enforce Open Space Limits:**
   - Walkable cells with only 1 open passage facing a standard interior cell are identified as "real dead ends" (as defined by `maze_analyzer.py`).
   - Walls at real dead ends are selectively opened to create alternative loops.
   - **Corridor Width Constraint:** Before any wall between cell $a$ and cell $b$ is opened, `_completes_open_3x3(maze, a, b)` verifies that opening the wall will not complete a $3 \times 3$ open area (defined as 9 cells with all 12 internal walls open). Because only the $\le 6$ overlapping $3 \times 3$ windows containing both cells can be affected, this check is executed in constant $O(1)$ time.
   - Braiding continues until at least 2 independent cycles are created ($E - V + 1 \ge 2$) and dead ends are minimized ($\le 2$, reaching $0$ for bonus criteria).

---

### Why this algorithm

We evaluated three classic spanning-tree algorithms (Recursive Backtracker, Randomized Prim's, and Randomized Kruskal's) and selected the Recursive Backtracker for concrete technical reasons:

1. **Fewer Initial Dead Ends for Braiding:**
   The default and primary mode required by §IV.4 is `PERFECT=False`, which mandates a playable board with rare dead ends.
   - The Recursive Backtracker naturally carves long, winding corridors with high directional persistence, yielding an initial dead-end ratio of only ~10%.
   - In contrast, Randomized Prim's and Kruskal's algorithms grow outward uniformly from frontiers, producing highly branched mazes with ~30% dead ends (roughly $3\times$ more dead ends to eliminate during braiding). Starting with fewer dead ends minimizes the post-processing wall removals required to braid the maze.
2. **Eliminating Recursion Overhead via Explicit Stack:**
   Standard recursive DFS hits Python's default recursion limit (`sys.getrecursionlimit() \approx 1000`) on moderate mazes (e.g., $40 \times 40 = 1600$ cells). By implementing the backtracker iteratively using an explicit Python `list` as a stack, execution occurs on the heap with $O(V)$ time and space complexity, completely eliminating recursion limit bottlenecks.
3. **Clean Handling of Non-Rectangular Reserved Zones:**
   Reserving the "42" pattern cells _before_ generation means the backtracker simply treats those coordinates as out-of-bounds. The spanning tree naturally navigates around the obstacle. Carving around reserved cells guarantees perimeter connectivity by construction, avoiding the need to forcefully close cells and repair broken graphs afterwards.
4. **Structural Coherence via Single Mutator:**
   All wall modifications route through `Maze.open_passage(a, b)`. This guarantees that cell $a$'s wall and cell $b$'s opposite wall are updated in a single atomic step, making mismatched neighbour wall encodings mathematically unrepresentable.

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
from mazegen import MazeGenerator
from maze.solver import solve_maze

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

# 5. Compute the optimal shortest path
entry_point = (0, 0)
exit_point = (19, 14)
path_str = solve_maze(maze, entry=entry_point, exit=exit_point)
print(f"Shortest path ({len(path_str)} steps): {path_str}")
```

---

## Work assignments

### Team Member Roles

The project responsibilities were divided between `skusakab` (So) and `jperez-u` (Javier) according to design seams and module contracts:

- **`skusakab` (So) — Maze Core & Generation Engine (W01–W12, W18, W21):**
  - **Configuration:** Lexical and semantic parsing of `config.txt` (`maze/config.py`), syntax verification, type conversion, and boundary checks.
  - **Data Structure:** `Maze` grid implementation (`maze/maze.py`), `Direction` enum, bitmask manipulation, and the atomic `open_passage` mutator.
  - **Generation:** Iterative DFS backtracker (`mazegen/generator.py`), seed management, "42" pattern reservation (`maze/pattern_42.py`), and braiding logic with $O(1)$ $3 \times 3$ open area detection.
  - **Solving:** Shortest-path BFS solver (`maze/solver.py`) producing optimal `NESW` direction strings.
  - **Testing:** Core unit test suite (`tests/test_config.py`, `tests/test_maze.py`, `tests/test_generator.py`).
- **`jperez-u` (Javier) — Output, Visualisation, CLI & Packaging (W13–W17, W20, W22–W24):**
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
  - `PERFECT=False`（既定）: 完全な連結性を保ちつつ、2本以上の独立したループを持ち、行き止まりを最小限（2個以下、ボーナスで0個）に抑えた遊べる盤面。
- **「42」パターンの描画:** 盤面のサイズが十分な場合、中央付近に完全に閉じたセル（`0xf`）で「42」の形状を埋め込み、その周囲に通路を形成します。サイズが不足する場合は警告メッセージを表示し、パターンを省略して生成を継続します。
- **16進数ウォール表現 (§IV.5):** 各セルの方位ごとの壁（北=1, 東=2, 南=4, 西=8; 閉=1, 開=0）を 1 桁の 16 進数で出力します。隣接するセル間で共有壁の状態は常に一致します。
- **ターミナル ASCII 可視化 (§V):** 壁の色変更（ANSI エスケープシーケンス）、最短経路の表示/非表示切り替え、迷路の再生成、終了などのインタラクティブ操作が可能です。
- **再利用可能モジュール `mazegen` (§VI):** 将来のプロジェクトで容易に import して利用できるよう、単一のクラス `MazeGenerator` として設計・パッケージ化されています。Poetry を用いて `.whl` および `.tar.gz` としてビルド可能です。
- **厳格なコーディング規約 (§III.1):** すべての関数に型ヒント（`mypy` 準拠）、`flake8`（PEP 8）準拠、NumPy スタイルの docstring（PEP 257）を適用し、例外を適切に捕捉して予期せぬクラッシュを防止しています。

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

#### テストとビルド

```bash
make test         # pytest によるテスト実行
make lint         # flake8 および mypy による静的検証
make lint-strict  # mypy --strict を含む厳格検証
make clean        # キャッシュディレクトリの削除
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

#### 座標系規約

- 原点 `(0, 0)` は**左上隅**です。`x` は列（横方向）、`y` は行（縦方向）を表します。
- プログラム全体（パーサ、生成器、描画器）で `(x, y)` 順を一貫して採用し、内部配列 `_grid[y][x]` への転置は `Maze` クラス内に完全に隠蔽されています。

#### エラー処理方針 (§IV.2)

- 構文エラー、必須キーの欠落、重複キー、範囲外座標、アクセス不可能なファイルパスなどの不正入力に対して、自前の `ConfigError` サブクラスを送出し、エントリポイントで `source:line: problem` 形式のエラーメッセージを標準エラー出力へ表示して終了コード `1` で終了します（未処理例外でクラッシュすることはありません）。

---

### 生成アルゴリズムと選定理由

#### 採用アルゴリズム

**再帰的バックトラッカー（深さ優先探索 / DFS）** を明示的スタックによる反復処理で実装し、既定モード（`PERFECT=False`）向けに**行き止まり解消（braiding）処理**を組み合わせています。

1. **シード解決:** 専用の `random.Random(seed)` インスタンスを生成。未指定時は乱数シードを自動生成し、呼び出し元が表示・再利用できるようにプロパティとして保持。
2. **「42」パターンの確保:** 迷路が十分なサイズを持ち、四隅および中央候補を塞がない場合に、該当セルを予約領域として設定（全壁閉の `0xf` を維持）。
3. **全域木の掘削 (DFS):** 未訪問のセルを探索しながら `Maze.open_passage(a, b)` で壁を開放。反復処理により、Python の再帰深度上限（約1000）を回避。
4. **分岐:** `PERFECT=True` の場合は全域木（ループ数0、経路1本）の時点で完了。
5. **Braiding (既定モード):** 本物の行き止まり（外周や42パターン以外に面する壁を持つセル）を選択的に開放し、2本以上の独立ループを形成。開放前に `_completes_open_3x3` により最大6個の $3 \times 3$ 枠を $O(1)$ で検査し、幅2を超える開放領域が絶対に生成されないよう構造的に保証。

#### 選定理由

- **初期行き止まりの少なさ:** 既定モード（`PERFECT=False`）では行き止まりを潰す必要があります。再帰的バックトラッカーは通路が長く伸びる特性上、初期状態の行き止まり率が約 10% と極めて低く（Prim 法や Kruskal 法は約 30%）、braiding で取り除くべき壁の枚数を大幅に削減できます。
- **反復版による再帰深度の克服:** 明示的なスタック（ヒープメモリ上のリスト）を使用することで、大きな盤面でもスタックオーバーフローを起こさず線形時間 $O(V)$ で安定動作します。
- **非矩形領域への適応性:** 「42」パターンのセルを初期段階で範囲外扱いとするだけで、バックトラッカーはその周囲を自然に迂回して木を構成でき、後から壁を閉じてグラフを修復する手間やリスクが発生しません。
- **共有壁の整合性保証:** 壁の変更を `Maze.open_passage` の1箇所に集約することで、隣接する両セルの壁ビットが同時に更新され、壁の食い違い（不整合）が原理的に発生しません。

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
from mazegen import MazeGenerator
from maze.solver import solve_maze

# インスタンス化 (カスタムパラメータ: サイズ、モード、シード)
gen = MazeGenerator(width=20, height=15, perfect=False, seed=42)

# 迷路の生成
maze = gen.generate()
print(f"使用シード値: {gen.seed}")

# 構造へのアクセス
for row in maze.rows():
    print("".join(f"{mask:x}" for mask in row))

# 最短経路の取得 (NESW 文字列)
path = solve_maze(maze, (0, 0), (19, 14))
print(f"最短経路: {path}")
```

---

### 役割分担と進め方

#### 役割分担

- **`skusakab` (So) — コアエンジン & 生成ロジック (W01–W12, W18, W21):**
  - 設定パースおよび検証 (`maze/config.py`)
  - 迷路データ構造・壁ビットマスク・`open_passage` (`maze/maze.py`)
  - 迷路生成アルゴリズム・シード・「42」・braiding (`mazegen/generator.py`, `maze/pattern_42.py`)
  - 最短経路探索 BFS ソルバ (`maze/solver.py`)
  - コア単体テスト群 (`tests/test_config.py`, `tests/test_maze.py`, `tests/test_generator.py`)
- **`jperez-u` (Javier) — 出力・可視化・インフラ・CLI (W13–W17, W20, W22–W24):**
  - 16進数出力およびメタデータ書き出し (`output/maze_writer.py`)
  - ターミナル ASCII レンダラー・色パレット・操作ハンドラ (`display/`)
  - メイン CLI 統合 (`a_maze_ing.py`)
  - Poetry / Makefile / `.gitattributes` / CI インフラ整備
  - 出力および表示のテスト群 (`tests/test_output.py`, `tests/test_display.py`)
  - ライセンス選定 (`LICENSE.md`) およびプロジェクトドキュメント (`README.md`)

#### 計画の変遷

1. **キックオフ (2026-08-13):** 9/17 を締切とする約1か月の計画を策定。当初は `venv` + `pip` を採用予定でした。
2. **Poetry への移行 (2026-08-20 / 決定 2.1):** 異なる開発環境（Windows と Linux）での依存関係の完全な固定、開発ツールと実行時依存の分離、§VI のパッケージ配布を容易にするため、Javier の提案・実装により Poetry へ移行しました（[`Docs/pair_communication/03_poetry_switch.md`](Docs/pair_communication/03_poetry_switch.md)）。
3. **データ構造と座標系の統一 (2026-08-21〜2026-09-02):** 当初は境界で `(x, y)` と `[y][x]` を変換する計画でしたが、`Maze` クラスが内部で転置を吸収し、プロジェクト全体で `(x, y)` 順に統一することで座標変換バグを防止しました。
4. **不変条件の構造的保証 (2026-08-24):** 壁の不整合を防ぐため、壁の変更を `Maze.open_passage` の1つのみに制限しました。
5. **Braiding と 3x3 領域判定の洗練 (2026-09-01〜2026-09-13):** 3x3 開放領域を「内壁12枚がすべて開いている状態」と明確に定義し、壁開放時に影響を受ける最大6つの枠のみを判定する定数時間 $O(1)$ の判定法を確立しました。
6. **シード出力の責務分離 (2026-09-13):** 再利用ライブラリとしての純粋性を保つため、`MazeGenerator` は標準出力への出力を一切行わず、エントリポイントがプロパティからシードを取得して表示する設計に決定しました。

#### うまくいったこと / 改善できたこと

- **うまくいったこと:** コード実装前に `Docs/implementation_plans/` でインターフェース契約を綿密に定義したことで、モジュール統合時の不整合がほぼゼロに抑えられました。また、日々の作業ログ (`Docs/work_log/`) とバイリンガル解説 (`Docs/learning_log/`) により、言語差（日本語とスペイン語/英語）を超えて円滑に協働できました。
- **改善できたこと:** Windows 環境と Linux 環境における改行コード（CRLF）や Make のタブ文字問題で序盤に手戻りが発生したため、`.gitattributes` の導入を初期段階で行うべきでした。また、PR を介さない直マージ運用を採ったため、相手のコードを能動的に読み込む規律が強く求められました。

#### 使用したツール

- Python 3.10+, Poetry, Make, pytest, flake8, mypy, Git, GitHub, VS Code, `maze_analyzer.py`, Claude AI

---

### 参考資料 / AI の使い方

#### 参考資料

- Jamis Buck, _Mazes for Programmers_ (Pragmatic Bookshelf, 2015) — 全域木、バックトラッカー、braiding の基礎理論
- グラフ理論と全域木の性質（オイラーの公式 $E - V + 1$ による閉路計算）
- 幅優先探索 (BFS) 最短経路アルゴリズム
- Python 公式ドキュメント (PEP 8, PEP 257, dataclasses, enum, typing, random)

#### AI の使い方 (§II & §VII)

42 の AI 指針 (§II) に従い、Claude をペアプログラミング・学習支援ツールとして活用しました:

- **学習ノートの草稿作成 (`Docs/learning_log/`):** ビット演算、Python の型システム、ジェネレータの評価タイミング、例外設計などの概念整理とバイリンガル解説の作成。
- **設計仕様の洗練とエッジケースの洗い出し:** `config-parser.md` の 31 個のエッジケースや、`generation-algorithm.md` の 3x3 判定アルゴリズムの幾何的検討。
- **Docstring と型ヒントの整理:** PEP 257 (NumPy スタイル) の docstring 整備や `mypy` エラーの原因究明。
- **ペア間コミュニケーション支援:** 日本語と英語の技術文書の相互翻訳およびニュアンスの確認。

AI 生成のコードを無批判に導入することは厳に戒め、すべてのアルゴリズム・不変条件・テストケースについてチーム両名が論理的に説明・検証できる状態を保っています。ディフェンス (§IX) における口頭試問およびライブコーディング修正にも十分に対応できる理解を備えています。

---

Documentation for our own process (work logs, learning notes, design plans) lives in [`Docs/`](Docs/README.md).
私たちの作業記録(作業ログ・学習ノート・設計計画)は [`Docs/`](Docs/README.md) にある。
