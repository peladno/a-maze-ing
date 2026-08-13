# A-Maze-ing — プロジェクト構成と2人での役割分担

## 1. プロジェクト概要

**A-Maze-ing** は、Python 3.10 以降を使用して迷路を生成するプロジェクトです。

設定ファイルから迷路を生成し、指定された16進数形式でファイルに保存するとともに、入口・出口・解答経路を含む迷路を視覚的に表示します。

プロジェクトでは、少なくとも以下を実装する必要があります。

- ランダムな迷路生成。
- seed による再現可能な迷路生成。
- `PERFECT=True` の場合、2つのセル間に経路が1つだけ存在する完全迷路。
- `PERFECT=False` の場合、複数の独立した経路を持つプレイ可能な迷路。
- 設定ファイルと迷路の検証。
- エラーを適切に処理し、予期せずプログラムがクラッシュしないようにする。
- 迷路が十分な大きさの場合、視覚的に確認できる `42` パターン。
- 指定された16進数形式での出力。
- 入口、出口、最短経路を含む視覚表示。
- 迷路の再生成、経路の表示/非表示、壁の色変更。
- 再利用可能な `MazeGenerator` クラス。
- `mazegen-*` パッケージとしてビルド可能な構成。
- `flake8`、`mypy`、type hints、docstrings、tests、Makefile、`.gitignore`、README、LICENSE。

---

# 2. 推奨プロジェクト構成

```text
a-maze-ing/
│
├── a_maze_ing.py                 # メインエントリーポイント
├── config.txt                    # デフォルト設定
├── Makefile
├── README.md
├── LICENSE.md
├── .gitignore
│
├── maze/
│   ├── __init__.py
│   ├── cell.py                   # Cell の定義
│   ├── maze.py                   # Maze データ構造
│   ├── generator.py              # 迷路生成アルゴリズム
│   ├── solver.py                 # 最短経路の計算
│   ├── validator.py              # 迷路・設定の検証
│   ├── config.py                 # 設定ファイルの解析
│   ├── output.py                 # 16進数形式での出力
│   └── pattern_42.py             # 42 パターン
│
├── display/
│   ├── __init__.py
│   ├── renderer.py               # 表示インターフェース
│   └── terminal.py               # ASCII ターミナル表示
│
├── mazegen/
│   ├── __init__.py
│   └── generator.py              # 再利用可能な MazeGenerator
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

> 実際の内部構成は簡略化しても構いません。重要なのは、迷路生成ロジックを再利用可能なクラスとして独立したモジュール/パッケージに実装し、`mazegen-*` パッケージをビルドできるようにすることです。

---

# 3. メンバーA — Maze Core & Generation

## 主な担当

**迷路エンジン**を担当します。

設定ファイル、データ構造、迷路生成、検証、再利用可能な generator パッケージなど、プロジェクトのアルゴリズム部分を中心に担当します。

### Tasks

- [ ] `Cell` のデータ構造を設計する。
- [ ] `Maze` のデータ構造を設計する。
- [ ] 迷路グリッドを実装する。
- [ ] 壁を以下の4方向で管理する。
  - North
  - East
  - South
  - West
- [ ] 選択した迷路生成アルゴリズムを実装する。
- [ ] seed による再現可能な生成を実装する。
- [ ] `PERFECT=True` を実装する。
- [ ] `PERFECT=False` を実装する。
- [ ] 隣接するセルの共有壁が常に一致するようにする。
- [ ] 全セルが到達可能であることを保証する。
- [ ] `42` パターンを実装する。
- [ ] 迷路サイズを検証する。
- [ ] Entry / Exit を検証する。
- [ ] 設定ファイルを解析する。
- [ ] 不正な設定を適切に処理する。
- [ ] 最短経路を計算する。
- [ ] 再利用可能な `MazeGenerator` クラスを作成する。
- [ ] `mazegen-*` パッケージを準備する。
- [ ] Core ロジックの unit tests を作成する。

### 主なファイル

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

# 4. メンバーB — Output, Visualisation & Infrastructure

## 主な担当

生成された迷路を**出力・表示・実行・テスト・ドキュメント化**する部分を担当します。

### Tasks

- [ ] ターミナルまたはグラフィカル renderer を実装する。
- [ ] 迷路の壁を明確に表示する。
- [ ] Entry を表示する。
- [ ] Exit を表示する。
- [ ] Solution path を表示する。
- [ ] Solution の表示/非表示を実装する。
- [ ] 新しい迷路の再生成を実装する。
- [ ] 壁の色変更を実装する。
- [ ] `42` パターン用の色を追加する。
- [ ] 16進数形式での出力を実装する。
- [ ] Entry coordinates を output file に書き込む。
- [ ] Exit coordinates を output file に書き込む。
- [ ] Shortest path を output file に書き込む。
- [ ] すべての出力行が `\n` で終わることを確認する。
- [ ] `a_maze_ing.py` の統合を行う。
- [ ] `Makefile` を作成する。
- [ ] `.gitignore` を作成する。
- [ ] `flake8` と `mypy` を設定する。
- [ ] Integration tests を作成する。
- [ ] メインの `README.md` を作成する。
- [ ] 選択したアルゴリズムをドキュメント化する。
- [ ] Configuration file をドキュメント化する。
- [ ] 再利用可能な package の使い方をドキュメント化する。
- [ ] Team roles と project planning を README に記載する。
- [ ] `LICENSE.md` を作成する。

### 主なファイル

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

# 5. 共同で担当する部分

以下は、どちらか一人だけが理解している状態にしないことを推奨します。

両方のメンバーが理解・レビューするもの：

- [ ] Maze data structure
- [ ] Maze generation algorithm
- [ ] `PERFECT` / non-perfect modes
- [ ] Wall encoding
- [ ] Shortest-path algorithm
- [ ] Configuration parser
- [ ] Error handling
- [ ] `MazeGenerator` API
- [ ] Final integration
- [ ] README
- [ ] Tests

特にこの課題では、評価時に自分たちのコードを説明できることが重要です。

そのため、

> 「自分が担当していない部分は分からない」

という状態にならないように、お互いに code review を行うことをおすすめします。

---

# 6. 別の分担方法：Backend vs Frontend

より明確に分けたい場合は、以下の方法もあります。

## メンバーA — Algorithm / Backend

担当：

- Configuration parser
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

## メンバーB — Frontend / Application

担当：

- Main program
- Output file generation
- Hexadecimal encoding
- Terminal / MLX rendering
- User interaction
- Path visualisation
- Maze regeneration
- Colours
- Integration tests
- Makefile
- README
- Package build
- License

### この分割のイメージ

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

# 7. 推奨する分担

2人でこのプロジェクトを作る場合、**Algorithm/Backend と Interface/Infrastructure** に分ける方法を推奨します。

理由は、迷路生成がこの課題のアルゴリズム上の中心である一方、表示・出力・package・testing・documentation は別のまとまった責任範囲になるためです。

ただし、

> 一人が documentation だけを書く

または

> 一人が rendering だけを書く

という分け方はおすすめしません。

両方のメンバーが十分な量の programming work を担当するべきです。

---

# 8. Git Workflow

以下のように feature branch を分けると管理しやすくなります。

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

### 推奨 Workflow

1. 両方とも `main` から作業を開始する。
2. 大きな機能ごとに feature branch を作る。
3. commit は小さく、内容が分かる名前にする。
4. 重要な変更は Pull Request にする。
5. もう一人が code review を行う。
6. 両方がコードを理解してから merge する。
7. 定期的に `main` の変更を取り込む。
8. 最後まで統合を待たず、早い段階から統合テストを行う。

---

# 9. 推奨する統合順序

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
12. Final integration
```

---

# 10. Milestones

## Milestone 1 — Skeleton

- [ ] Repository を作成。
- [ ] 基本的な folder structure。
- [ ] `a_maze_ing.py`。
- [ ] `Makefile`。
- [ ] Configuration example。
- [ ] Basic tests。

## Milestone 2 — Core Maze

- [ ] Maze representation。
- [ ] Cell representation。
- [ ] Generation algorithm。
- [ ] Seed support。
- [ ] Perfect mode。
- [ ] Non-perfect mode。

## Milestone 3 — Validation & Solver

- [ ] Configuration validation。
- [ ] Maze validation。
- [ ] Wall consistency。
- [ ] Connectivity。
- [ ] Entry / Exit validation。
- [ ] Shortest path。
- [ ] `42` pattern。

## Milestone 4 — Output & Display

- [ ] Hexadecimal output。
- [ ] Entry / Exit / Path output。
- [ ] Visual rendering。
- [ ] Maze regeneration。
- [ ] Show/hide path。
- [ ] Wall colours。

## Milestone 5 — Reusable Package

- [ ] `MazeGenerator` reusable class。
- [ ] Public API。
- [ ] Package metadata。
- [ ] `.whl` を build。
- [ ] `.tar.gz` を build。
- [ ] Clean virtual environment で install を確認。

## Milestone 6 — Finalisation

- [ ] Full test suite。
- [ ] `flake8`。
- [ ] `mypy`。
- [ ] Error handling。
- [ ] README。
- [ ] LICENSE。
- [ ] Final peer review。
- [ ] 提供されている maze analyzer でテスト。
- [ ] Evaluation の準備。

---

# 11. 重要なプロジェクト要件

Subject によると、プロジェクトは **Python 3.10 以降**で作成し、`flake8`、type hints、`mypy`、docstrings を使用し、エラーを適切に処理する必要があります。 fileciteturn0file0

プログラムは以下の形式で実行します。

```bash
python3 a_maze_ing.py config.txt
```

Configuration には最低限、以下が含まれます。

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

再現可能な maze generation のために seed を追加することもできます。 fileciteturn0file0

生成された迷路では、隣接セルの共有壁が一致している必要があり、全セルが接続され、Entry / Exit が有効で、`PERFECT` と non-perfect のそれぞれの条件を満たす必要があります。 fileciteturn0file0

Output format では、各セルを1つの hexadecimal digit で表現します。

4つの bit は以下を表します。

```text
Bit 0 → North
Bit 1 → East
Bit 2 → South
Bit 3 → West
```

迷路の後には Entry、Exit、Shortest path を記録します。 fileciteturn0file0

Visual representation では maze、Entry、Exit、Solution path を表示する必要があります。また、maze の regeneration、path の表示/非表示、wall colour の変更が必要です。 fileciteturn0file0

Maze generation は再利用可能な `MazeGenerator` class として独立した module/package に実装し、`mazegen-*` package を build できる必要があります。 fileciteturn0file0

README には project の説明、実行方法、configuration、選択した algorithm とその理由、再利用可能なコード、team roles、planning、AI の使用方法などを記載する必要があります。 fileciteturn0file0

---

# 12. チーム開発で重要なルール

このプロジェクトでは、

> 「あなたはあなたのコード、私は私のコード」

という完全分離ではなく、**担当を分けながら、お互いのコードを理解する**方法を推奨します。

最終的には2人とも、以下の流れを説明できるようにしてください。

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

評価時には、コードの一部を短時間で変更することを求められる可能性があります。そのため、担当外の部分についても基本的な理解を持っておくことが重要です。
