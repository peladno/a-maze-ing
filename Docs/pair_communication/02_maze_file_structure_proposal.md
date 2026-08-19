# A-Maze-ing — Final Project Structure
# A-Maze-ing — 最終プロジェクト構成

> This document describes the proposed final repository structure, component responsibilities, architecture, development order, and final checks.
>
> このドキュメントでは、最終的なリポジトリ構成、各コンポーネントの役割、アーキテクチャ、開発順序、最終チェックをまとめます。

---

## 1. Final Repository Structure / 最終リポジトリ構成

```text
a-maze-ing/
│
├── a_maze_ing.py
├── config.txt
│
├── Makefile
├── README.md
├── LICENSE.md
├── .gitignore
├── pyproject.toml
├── poetry.lock
│
├── maze/
│   ├── __init__.py
│   ├── cell.py
│   ├── maze.py
│   ├── generator.py
│   ├── solver.py
│   ├── validator.py
│   ├── config.py
│   └── pattern_42.py
│
├── output/
│   ├── __init__.py
│   └── maze_writer.py
│
├── display/
│   ├── __init__.py
│   ├── renderer.py
│   ├── terminal_renderer.py
│   ├── colors.py
│   └── input_handler.py
│
├── mazegen/
│   ├── __init__.py
│   └── generator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_cell.py
│   ├── test_maze.py
│   ├── test_generator.py
│   ├── test_solver.py
│   ├── test_validator.py
│   ├── test_pattern_42.py
│   ├── test_output.py
│   └── test_display.py
│
├── docs/
│   ├── architecture.md
│   └── generator.md
│
└── dist/
    ├── mazegen-*.whl
    └── mazegen-*.tar.gz
```

### 日本語

上記は最終的な構成案です。

- `maze/` — 迷路そのもののロジック
- `output/` — 出力ファイルの生成
- `display/` — 視覚表示とユーザー操作
- `mazegen/` — 再利用可能な `MazeGenerator`
- `tests/` — テスト
- `docs/` — 技術ドキュメント
- `a_maze_ing.py` — メインエントリーポイント

課題では、迷路生成を再利用可能な `MazeGenerator` のようなクラスとして独立した module/package に実装し、`mazegen-*` package をソースから再構築できるようにする必要があります。 fileciteturn3file0

---

# 2. Root Files / ルートファイル

## `a_maze_ing.py`

**English**

This is the main entry point. It should coordinate the components instead of containing the maze-generation algorithm itself.

```text
config.txt
    ↓
Configuration
    ↓
MazeGenerator
    ↓
Maze
    ├────────→ MazeWriter → maze.txt
    │
    └────────→ Renderer → Display
```

The program must be executable as:

```bash
python3 a_maze_ing.py config.txt
```

**日本語**

`a_maze_ing.py` はメインエントリーポイントです。

迷路生成アルゴリズムを直接大量に持たせるのではなく、Configuration、Generator、Output、Display などを組み合わせる役割にします。

課題では `python3 a_maze_ing.py config.txt` で実行する形式が指定されています。 fileciteturn3file12

---

## `config.txt`

**English**

Contains the maze-generation parameters.

Example:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

A seed can also be supported for reproducible generation.

**日本語**

迷路生成に必要な設定を保存します。

最低限、`WIDTH`、`HEIGHT`、`ENTRY`、`EXIT`、`OUTPUT_FILE`、`PERFECT` を扱える構成にします。

再現可能な生成のため `SEED` を追加することもできます。

---

## `Makefile`

**English**

Recommended targets:

```bash
make
make test
make lint
make typecheck
make package
make clean
```

**日本語**

Build、test、lint、type checking、package build、clean などを簡単に実行できるようにします。

---

## `README.md`

**English**

The subject requires a root `README.md`. It must describe the project, instructions, configuration format, selected generation algorithm and its justification, reusable code, team roles, planning and its evolution, tools, AI usage, and resources. fileciteturn3file1

The first line must contain the required 42 wording:

```text
*This project has been created as part of the 42 curriculum by <login1>, <login2>.*
```

**日本語**

README には、プロジェクト概要、実行方法、Configuration、選択したアルゴリズムとその理由、再利用可能なコード、チーム分担、Planning とその変化、使用したツール、AI の使用方法、Resources などを記載します。 fileciteturn3file7

---

## `LICENSE.md`

**English**

The reusable maze generator must have a license that explicitly permits reuse and distribution by later projects. fileciteturn3file0

**日本語**

再利用可能な MazeGenerator を将来のプロジェクトで利用・配布できるよう、適切なライセンスを選択し、ルートに `LICENSE.md` を配置します。

---

## `pyproject.toml`

**English**

This is the central project configuration file and is managed with **Poetry**.

It should contain:

- Project metadata.
- Python version requirement.
- Runtime dependencies.
- Development dependencies.
- Package configuration.
- Build/package configuration.
- Tool configuration when appropriate.

Example structure:

```toml
[tool.poetry]
name = "mazegen"
version = "1.0.0"
description = "Reusable maze generation package"
authors = ["<login1>", "<login2>"]

[tool.poetry.dependencies]
python = "^3.10"

[tool.poetry.group.dev.dependencies]
pytest = "*"
mypy = "*"
flake8 = "*"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```

The exact dependency versions and Poetry syntax must be adjusted to the Poetry version used by the team.

**日本語**

`pyproject.toml` はプロジェクトの中心となる設定ファイルで、**Poetry** によって管理します。

ここには以下をまとめます。

- Project metadata
- Python version
- Runtime dependencies
- Development dependencies
- Package configuration
- Build/package configuration
- 必要に応じた tool configuration

実際の dependency version や Poetry の syntax は、チームで使用する Poetry のバージョンに合わせます。

---

## `poetry.lock`

**English**

`poetry.lock` records the exact dependency versions resolved by Poetry.

It should be committed to Git so both team members can install the same dependency set.

Recommended installation command:

```bash
poetry install
```

**日本語**

`poetry.lock` には Poetry が解決した依存関係の具体的なバージョンが保存されます。

2人の開発環境をできるだけ同じ状態にするため、Git に commit します。

基本的なインストールは:

```bash
poetry install
```

です。

---

# 3. `maze/` — Maze Core / 迷路コア

```text
maze/
├── cell.py
├── maze.py
├── generator.py
├── solver.py
├── validator.py
├── config.py
└── pattern_42.py
```

## `cell.py`

**English**

Represents one maze cell, including its position and wall information:

```text
North
East
South
West
```

**日本語**

迷路の1マスを表します。座標と4方向の壁情報を管理します。

---

## `maze.py`

**English**

Represents the complete internal maze structure and provides the API used by Solver, Output, and Display.

Possible interface:

```python
maze.width
maze.height
maze.cells
maze.entry
maze.exit
maze.solution
```

The exact API should be agreed by both members before frontend implementation.

**日本語**

迷路全体を表すデータ構造です。

Backend と Frontend の境界になるため、実装前に2人で API を決めます。

---

## `generator.py`

**English**

Contains the maze-generation algorithm and supports:

- Random generation.
- Seed-based reproducibility.
- `PERFECT=True`.
- `PERFECT=False`.
- Consistent shared walls.
- Full connectivity.
- The required `42` pattern.

**日本語**

迷路生成アルゴリズムを担当します。

ランダム生成、seed、Perfect/Playable mode、壁の整合性、全セルの接続、`42` pattern などを扱います。

---

## `solver.py`

**English**

Calculates a valid shortest path from Entry to Exit.

The required output path uses:

```text
N E S W
```

**日本語**

Entry から Exit までの有効な最短経路を計算します。

Output file では `N E S W` を使用します。 fileciteturn3file5

---

## `validator.py`

**English**

Validates configuration, maze dimensions, coordinates, connectivity, wall consistency, and the required maze properties.

**日本語**

Configuration、サイズ、Entry/Exit、Connectivity、Wall consistency、Perfect/Playable の条件などを検証します。

---

## `config.py`

**English**

Reads and validates `config.txt` and exposes a clean configuration object.

**日本語**

`config.txt` を読み込み、値を検証して他のコンポーネントから利用しやすい Configuration object にします。

---

## `pattern_42.py`

**English**

Contains the logic related to the required `42` pattern.

**日本語**

課題で要求される `42` pattern に関する処理をまとめます。

---

# 4. `output/` — Output File / 出力ファイル

```text
output/
├── __init__.py
└── maze_writer.py
```

## `maze_writer.py`

**English**

Converts the internal Maze structure into the required output format.

The output contains:

1. One hexadecimal character per cell.
2. One row per maze row.
3. An empty line.
4. Entry coordinates.
5. Exit coordinates.
6. The shortest path.
7. Every line ending with `\n`.

The four wall bits represent:

```text
Bit 0 → North
Bit 1 → East
Bit 2 → South
Bit 3 → West
```

The internal maze structure does not have to be identical to the output format. fileciteturn3file5

**日本語**

内部の `Maze` を課題指定の output file に変換します。

```text
maze rows in hexadecimal

<empty line>

entry
exit
shortest path
```

という構造を作り、各セルの壁を4 bit の hexadecimal で表現します。 fileciteturn3file5

---

# 5. `display/` — Visualisation / 視覚表示

The subject allows either Terminal ASCII or MiniLibX rendering. fileciteturn3file5

課題では Terminal ASCII または MiniLibX を使用できます。

```text
display/
├── renderer.py
├── terminal_renderer.py
├── colors.py
└── input_handler.py
```

## `renderer.py`

**English**

Defines the general renderer interface.

```python
class Renderer:
    def render(self, maze) -> None:
        ...
```

The renderer consumes a Maze; it does not generate it.

**日本語**

Renderer の基本インターフェースを定義します。

重要なのは、

```text
Renderer → Maze を表示する
Renderer → Maze を生成しない
```

という責任分離です。

---

## `terminal_renderer.py`

**English**

Draws the maze in the terminal and clearly displays walls, Entry, Exit, and the solution path.

**日本語**

Terminal 上に迷路を描画し、Walls、Entry、Exit、Solution path を表示します。

---

## `colors.py`

**English**

Centralises display colours:

```text
WALL_COLOR
PATH_COLOR
ENTRY_COLOR
EXIT_COLOR
PATTERN_42_COLOR
```

**日本語**

Wall、Path、Entry、Exit、`42` pattern などの色をまとめて管理します。

---

## `input_handler.py`

**English**

Handles the required interactions:

```text
Regenerate maze
Show / hide shortest path
Change wall colours
```

Additional interactions may be added. fileciteturn3file5

**日本語**

最低限、迷路の再生成、Shortest path の表示/非表示、壁の色変更を処理します。 fileciteturn3file5

---

# 6. Poetry / パッケージ管理

**English**

The project will use **Poetry** as the package manager and build tool.

Poetry will be used for:

- Creating/managing the project virtual environment.
- Installing dependencies.
- Locking dependency versions.
- Managing development dependencies.
- Building the reusable `mazegen-*` package.
- Keeping project/package metadata in `pyproject.toml`.

Recommended workflow:

```bash
poetry install
poetry shell
poetry run pytest
poetry run flake8 .
poetry run mypy .
poetry build
```

If the installed Poetry version does not provide `poetry shell`, use:

```bash
poetry env activate
```

The team should use the same Poetry version where practical.

The generated distribution files should appear in:

```text
dist/
├── mazegen-*.whl
└── mazegen-*.tar.gz
```

The source repository should contain `pyproject.toml` and `poetry.lock`; generated build artifacts in `dist/` should only be committed if the subject/evaluation explicitly requires them.

**日本語**

このプロジェクトでは **Poetry** を package manager と build tool として使用します。

Poetry の役割:

- Virtual environment の管理
- Dependencies のインストール
- Dependency versions の lock
- Development dependencies の管理
- `mazegen-*` package の build
- `pyproject.toml` による project/package metadata の管理

推奨 workflow:

```bash
poetry install
poetry shell
poetry run pytest
poetry run flake8 .
poetry run mypy .
poetry build
```

使用している Poetry のバージョンによって `poetry shell` が利用できない場合は:

```bash
poetry env activate
```

を使用します。

可能な限り、チーム内で同じ Poetry version を使用します。

Build された package は通常:

```text
dist/
├── mazegen-*.whl
└── mazegen-*.tar.gz
```

に生成されます。

ソースリポジトリには `pyproject.toml` と `poetry.lock` を含めます。`dist/` の生成物を Git に commit するかどうかは、subject/evaluation の要求を優先します。

---

# 7. `mazegen/` — Reusable Package / 再利用可能パッケージ

```text
mazegen/
├── __init__.py
└── generator.py
```

**English**

This is a key requirement.

The reusable module should expose a unique generator class such as:

```python
MazeGenerator
```

The documentation must explain how to:

- Instantiate it.
- Pass custom parameters.
- Use a seed.
- Access the generated maze structure.
- Access at least one solution.

The repository must contain everything required to rebuild the `mazegen-*` package. fileciteturn3file0

**日本語**

ここは課題の重要要件です。

`MazeGenerator` の作成方法、custom parameters、seed、maze structure、solution の取得方法を説明します。

また、リポジトリから `mazegen-*` package を再ビルドできるようにします。

---

# 8. `tests/` — Testing / テスト

```text
tests/
├── test_config.py
├── test_cell.py
├── test_maze.py
├── test_generator.py
├── test_solver.py
├── test_validator.py
├── test_pattern_42.py
├── test_output.py
└── test_display.py
```

**English**

Core tests:

```text
test_config.py
test_cell.py
test_maze.py
test_generator.py
test_solver.py
test_validator.py
test_pattern_42.py
```

Frontend/integration tests:

```text
test_output.py
test_display.py
```

**日本語**

Backend の Core logic と Frontend の Output/Display の両方をテストします。

---

# 9. `docs/` — Documentation / ドキュメント

```text
docs/
├── architecture.md
└── generator.md
```

## `architecture.md`

**English**

Explains how the components communicate:

```text
Configuration
      ↓
MazeGenerator
      ↓
Maze
 ┌────┼─────────────┐
 ↓    ↓             ↓
Solver Validator   Pattern
 ↓
Solution
 ┌───────────────┐
 ↓               ↓
Output         Display
```

**日本語**

プロジェクトの各コンポーネントがどのようにつながっているかを説明します。

---

## `generator.md`

**English**

Contains the required short documentation for the reusable generator.

Example:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    seed=42
)

maze = generator.generate()
solution = generator.solve()
```

**日本語**

再利用可能な `MazeGenerator` の基本的な使用例、custom parameters、seed、maze structure、solution の取得方法などを説明します。

---

# 10. Team Responsibilities / チーム分担

## Member A — Backend / Maze Core

```text
maze/
├── cell.py
├── maze.py
├── generator.py
├── solver.py
├── validator.py
├── config.py
└── pattern_42.py

mazegen/
└── generator.py
```

**English**

Main responsibilities:

- Maze data structures.
- Configuration.
- Generation algorithm.
- Perfect/non-perfect modes.
- Validation.
- Solver.
- `42` pattern.
- Reusable generator.
- Core tests.

**日本語**

Member A は迷路の内部ロジックを担当します。

---

## Member B — Frontend / Output / Infrastructure

```text
a_maze_ing.py

output/
└── maze_writer.py

display/
├── renderer.py
├── terminal_renderer.py
├── colors.py
└── input_handler.py

tests/
├── test_output.py
└── test_display.py

Makefile
README.md
LICENSE.md
.gitignore
pyproject.toml
poetry.lock
```

**English**

Main responsibilities:

- Output file generation.
- Hexadecimal encoding.
- Visual rendering.
- Entry/Exit display.
- Solution path display.
- User interactions.
- Main application integration.
- Build/test infrastructure.
- Documentation.

**日本語**

Member B は Frontend、Output、Integration、Infrastructure を担当します。

---

# 11. Component Communication / コンポーネント間通信

```text
                 config.txt
                     │
                     ▼
              ┌──────────────┐
              │ Configuration │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ MazeGenerator│
              └──────┬───────┘
                     │
                     ▼
                ┌─────────┐
                │  Maze   │
                └────┬────┘
                     │
          ┌──────────┼───────────┐
          │          │           │
          ▼          ▼           ▼
       Solver    Validator    Pattern
          │
          ▼
       Solution
          │
     ┌────┴─────┐
     ▼          ▼
  Output      Display
     │          │
     ▼          ▼
 maze.txt    Terminal
```

**English**

The main architectural rule is that the internal Maze structure should be independent from how it is written to a file or displayed.

**日本語**

最も重要な設計原則は、

```text
Maze generation ≠ Output ≠ Display
```

です。

迷路を生成する処理、ファイルに保存する処理、画面に表示する処理を分離します。

---

# 12. Final Integration Checklist / 最終統合チェック

Before submission:

- [ ] `python3 a_maze_ing.py config.txt` works.
- [ ] Configuration errors are handled.
- [ ] Maze generation works.
- [ ] `PERFECT=True` works.
- [ ] `PERFECT=False` works.
- [ ] Shared walls are coherent.
- [ ] Entry and Exit are valid.
- [ ] A valid shortest path exists.
- [ ] Output format is correct.
- [ ] Visualisation works.
- [ ] Regeneration works.
- [ ] Show/hide path works.
- [ ] Wall-colour changes work.
- [ ] `flake8` passes.
- [ ] `mypy` passes.
- [ ] Tests pass.
- [ ] `mazegen-*` can be rebuilt.
- [ ] The package installs in a clean virtual environment.
- [ ] `LICENSE.md` exists.
- [ ] `README.md` contains all required sections.
- [ ] All required files are committed.

### 日本語

提出前に以下を2人で確認します。

- [ ] `python3 a_maze_ing.py config.txt` が動く。
- [ ] Configuration error を処理できる。
- [ ] Maze generation が動く。
- [ ] `PERFECT=True` が動く。
- [ ] `PERFECT=False` が動く。
- [ ] Shared walls が正しい。
- [ ] Entry / Exit が有効。
- [ ] Shortest path が存在する。
- [ ] Output format が正しい。
- [ ] Visualisation が動く。
- [ ] Regeneration が動く。
- [ ] Path の表示/非表示が動く。
- [ ] Wall colour の変更が動く。
- [ ] `flake8` が通る。
- [ ] `mypy` が通る。
- [ ] Tests が通る。
- [ ] `mazegen-*` を再ビルドできる。
- [ ] Clean virtual environment に install できる。
- [ ] `LICENSE.md` が存在する。
- [ ] README に必要な項目がある。
- [ ] 必要なファイルがすべて Git に commit されている。

---

# 13. Recommended Development Order / 推奨開発順序

```text
1. Configuration
        ↓
2. Cell / Maze
        ↓
3. Generator
        ↓
4. Validator
        ↓
5. Solver
        ↓
6. Output
        ↓
7. Display
        ↓
8. User interactions
        ↓
9. Reusable mazegen package
        ↓
10. Tests
        ↓
11. Poetry environment + dependencies
        ↓
12. flake8 + mypy
        ↓
13. README + LICENSE
        ↓
14. Clean package build with Poetry
        ↓
15. Final evaluation rehearsal
```

**English**

This order allows both members to work in parallel after the Maze API is agreed.

**日本語**

この順番なら、Maze API が決まった段階から Backend と Frontend を並行して開発できます。

---

# 14. Evaluation / 評価

**English**

Both members should understand the complete architecture.

The subject states that a small modification may be requested during evaluation. Therefore, neither member should depend exclusively on the other member's knowledge. fileciteturn3file7

Both members should be able to explain:

```text
Configuration
Maze generation
Maze representation
Validation
Shortest path
Output
Visualisation
Reusable package
```

**日本語**

評価では小さな変更を求められる可能性があります。

そのため、どちらか一人だけが特定部分を理解している状態は避けます。

2人とも最低限、

```text
Configuration
Maze generation
Maze representation
Validation
Shortest path
Output
Visualisation
Reusable package
```

の流れを説明できるようにします。

---

# 15. Subject-Based Requirements / 課題仕様に基づく要件

**English**

This structure follows the A-Maze-ing v2.2 requirements for:

- Python 3.10+.
- `a_maze_ing.py`.
- Configuration-based generation.
- Perfect and playable maze behaviour.
- Hexadecimal output.
- Visual representation.
- Required user interactions.
- Reusable `MazeGenerator`.
- Rebuildable `mazegen-*` package.
- `LICENSE.md`.
- Root `README.md`.
- Error handling.
- Type hints, `mypy`, and `flake8`.
- Poetry-based dependency and package management.
- Reproducible dependency installation through `poetry.lock`.
- Testing and evaluation readiness.

The exact implementation must always be checked against the official subject before submission.

**日本語**

この構成は A-Maze-ing v2.2 の以下の要件を基準にしています。

- Python 3.10+
- `a_maze_ing.py`
- Configuration による生成
- Perfect / Playable maze
- Hexadecimal output
- Visual representation
- 必須 User interactions
- 再利用可能な `MazeGenerator`
- 再ビルド可能な `mazegen-*` package
- `LICENSE.md`
- Root `README.md`
- Error handling
- Type hints、`mypy`、`flake8`
- Poetry による dependency / package management
- `poetry.lock` による再現可能な dependency installation
- Testing と evaluation への準備

提出前には必ず公式 subject の最新版と照合します。
