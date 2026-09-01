# maze-data-structure

| | |
| --- | --- |
| **Owner / 担当** | so (W03, W04) |
| **Status / 状態** | draft — awaiting javi's review / javi のレビュー待ち |
| **Date / 日付** | 2026-08-20 |
| **Subject ref** | §IV.4, §IV.5, §VI |
| **Related / 関連** | `Docs/pair_communication/01_kickoff.md` § 3.1, 3.2, 3.3, 3.6; `Docs/learning_log/maze-generation-algorithms.md` |

> **New here? Read [`architecture-overview.md`](architecture-overview.md) first** — it shows where this module
> sits in the program, and follows one small maze through every stage of the pipeline.
> **はじめて読む場合は [`architecture-overview.md`](architecture-overview.md) から。**
> このモジュールがプログラムのどこに位置するかと、小さな迷路 1 つがパイプラインを通っていく様子が書いてある。

> **This is the contract W13 (hex output) and W15 (renderer) depend on.** Nothing on javi's side should index the
> grid directly — read it through the accessors in §2.
> **これは W13(16 進出力)と W15(描画)が依存する契約。** javi 側はグリッドを直接添字で触らない。§2 のアクセサ経由で読む。

---

## 1. Scope / 対象範囲

### In scope

- The in-memory representation of the maze: a rectangular grid of cells, each holding which of its four walls are
  closed.
- The single operation that changes walls, and the invariant it protects.
- Read access for the generator (W05), the validator (W10), the solver (W12), the output encoder (W13) and the
  renderer (W15).
- Marking cells as **reserved** for the "42" pattern, so the generator never carves into them (§IV.4, decision 3.6).

### Out of scope

| Not here / ここではやらない | Where it belongs / どこの担当か |
| --- | --- |
| Hexadecimal encoding and the output file | W13 / W14 (javi) — `Maze` yields plain `int`s, javi formats them |
| The generation algorithm itself | W05 (so) — `generation-algorithm.md` |
| Entry / exit coordinates and validation | W11 (so) — they come from the config, not from the structure |
| The shortest path | W12 (so) — `shortest-path-solver.md` |
| Deciding *which* cells spell "42" | W09 (so) — this plan only stores the result |

**JA** — 「やらないこと」を明示するのは、境界を曖昧にしないため。`Maze` は**構造だけ**を持ち、
意味づけ(入口・出口・解・出力形式)は外側が持つ。§VI が「再利用モジュールの公開構造は
出力ファイルと同じ形式である必要はない」と認めているので、この分離は subject 側からも支持されている。

### Requirements it satisfies

> §IV.4 — neighbouring cells must encode their shared wall identically; the "42" is drawn by fully closed cells
> §IV.5 — one hexadecimal digit per cell, bit 0 = N, 1 = E, 2 = S, 3 = W, **1 means the wall is closed**

## 2. Interface / インターフェース

> **Signatures only. No function bodies.** / **シグネチャのみ。関数本体は書かない。**

```python
from collections.abc import Iterator
from enum import IntEnum

# (x, y) — x is the column, y is the row, origin top-left. Decision 3.2 = A.
Coord = tuple[int, int]


class Direction(IntEnum):
    """The four walls of a cell, valued as their bit in the §IV.5 encoding."""

    NORTH = 1   # bit 0
    EAST = 2    # bit 1
    SOUTH = 4   # bit 2
    WEST = 8    # bit 3

    @property
    def opposite(self) -> "Direction": ...

    @property
    def delta(self) -> Coord: ...


class MazeError(Exception):
    """Base class for every error this module raises (decision 3.9 = A)."""


class OutOfBoundsError(MazeError): ...


class NotAdjacentError(MazeError): ...


class Maze:
    """A rectangular grid of cells, each stored as a 4-bit wall mask.

    Every wall starts closed. The only way to open one is open_passage().
    """

    def __init__(
        self,
        width: int,
        height: int,
        reserved: frozenset[Coord] = frozenset(),
    ) -> None: ...

    # --- shape ---------------------------------------------------------
    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    @property
    def reserved(self) -> frozenset[Coord]: ...

    # --- reading -------------------------------------------------------
    def contains(self, pos: Coord) -> bool: ...

    def is_reserved(self, pos: Coord) -> bool: ...

    def walls_at(self, pos: Coord) -> int: ...

    def is_open(self, pos: Coord, direction: Direction) -> bool: ...

    def neighbours(self, pos: Coord) -> Iterator[tuple[Direction, Coord]]: ...

    def open_neighbours(self, pos: Coord) -> Iterator[Coord]: ...

    def rows(self) -> Iterator[tuple[int, ...]]: ...

    # --- the only mutator ----------------------------------------------
    def open_passage(self, a: Coord, b: Coord) -> None: ...
```

### What each member is for / 各メンバーの役割

**EN** — One line per member: what it does, and who calls it.
**JA** — 1 メンバー 1 行で、何をするか・誰が呼ぶか。

| Member | What it does / 何をするか | Called by / 呼ぶ側 |
| --- | --- | --- |
| `Direction` | Names the four walls, and its **values are the §IV.5 bits themselves** (`NORTH = 1` *is* bit 0). Keeping the bit order in one place means no second table can drift from the spec. / 4 枚の壁に名前を付ける。**値が §IV.5 のビットそのもの**。ビット順が 1 か所にあるので、仕様とずれる第二の表が生まれない。 | everyone |
| `Direction.opposite` | "The opposite of north is south." Needed because opening a wall must clear it **on both sides** — the other side is `opposite`. / 「北の反対は南」。壁を開けるときに**両側**を消す必要があり、その反対側がこれ。 | `open_passage` |
| `Direction.delta` | How `(x, y)` changes when you step one cell that way. Turns "the neighbour to the north" into a coordinate. / その方向へ 1 歩動いたときの `(x, y)` の変化量。「北の隣」を座標に変える。 | `neighbours` |
| `MazeError` and friends | The error types this module raises. Decision 3.9 = A: our own types, so the top-level handler can tell a bad config from a bug in our code. / このモジュールが送出するエラーの型。決定 3.9 = A で自前の型にした。最上位のハンドラが「設定が不正」と「自分たちのバグ」を区別できるようにするため。 | `a_maze_ing.py` (W17) |
| `Maze.__init__` | Builds the grid **with every wall closed**, and remembers which cells are reserved for the "42". / **すべての壁が閉じた状態**でグリッドを作り、「42」用に確保するセルを覚える。 | `MazeGenerator` (W05) |
| `width`, `height` | The size. Read-only. / 大きさ。読み取り専用。 | W13, W15, validator |
| `reserved` | The set of "42" cells. Read-only — it is fixed at construction. / 「42」のセル集合。読み取り専用で、構築時に確定する。 | generator, W15 (optional colouring) |
| `contains` | Is this coordinate inside the grid? The building block of every bounds check. / この座標は盤内か。あらゆる境界チェックの土台。 | everywhere |
| `is_reserved` | Is this cell part of the "42"? The generator must never carve into one. / このセルは「42」の一部か。生成器はここを掘ってはいけない。 | generator (W05, W09) |
| `walls_at` | The cell's 4-bit mask, `0`–`15`. A set bit means **closed**. **This integer is the hex digit** W13 writes. / そのセルの 4 ビットのマスク(0〜15)。ビットが立っていると**閉**。**この整数が W13 の書く 16 進の桁そのもの**。 | W13, validator |
| `is_open` | Is this one wall open? The same question as `walls_at` but without the caller touching bits. / この 1 枚の壁は開いているか。`walls_at` と同じ問いを、呼ぶ側がビットを触らずに聞ける形にしたもの。 | solver (W12), renderer (W15) |
| `neighbours` | The neighbouring cells that exist and are not reserved, **with the direction to reach each**. The generator's basic step. / 実在して確保セルでもない隣を、**そこへ行く方向つきで**返す。生成器の基本操作。 | generator (W05) |
| `open_neighbours` | The cells you can actually **walk to** — those with an open passage. This is what BFS follows. / 実際に**歩いて行ける**隣、つまり通路が開いている先。BFS がたどるのはこれ。 | solver (W12), validator (W10) |
| `rows` | Walks the whole grid top to bottom, each row left to right, yielding one `int` per cell. **The only way the outside sees the whole grid.** / グリッド全体を上から下・各行を左から右に走査し、1 セル 1 つの `int` を返す。**外側が全体を見る唯一の手段。** | W13, W15, validator |
| `open_passage` | **The only thing that changes anything.** Opens the wall between two adjacent cells, updating **both** of them. / **唯一、状態を変える操作。** 隣接 2 セルの間の壁を開け、**両方**を更新する。 | generator (W05) |

**EN** — Reading the table, three groups appear: `Direction` and the errors are **vocabulary**, most of `Maze` is
**questions** the outside asks, and exactly one member is an **action**. That shape is the design: a structure
that answers questions freely, and changes only through one door.

**JA** — 表を眺めると 3 つの群が見える。`Direction` とエラー型は**語彙**、`Maze` のほとんどは外側が投げる**質問**、
そして**動作**はただ 1 つ。この形自体が設計そのもの。
質問には自由に答え、変更は 1 つの扉からしか通さない構造。

### Which caller uses what / 誰が何を使うか

| Caller / 呼ぶ側 | Members it needs / 使うメンバー |
| --- | --- |
| Generator W05 — so | `neighbours`, `is_reserved`, `open_passage` |
| Validator W10 — so | `rows`, `walls_at`, `open_neighbours`, `contains` |
| Solver W12 — so | `open_neighbours`, `contains` |
| **Hex encoder W13 — javi** | `width`, `height`, `rows` |
| **Renderer W15 — javi** | `width`, `height`, `rows` or `is_open`, `reserved` |

**EN** — Note that **only the generator calls `open_passage`.** Everyone else reads. That is not a rule anyone has
to remember — it falls out of the fact that there is nothing else to call.

**JA** — **`open_passage` を呼ぶのは生成器だけ**である点に注目。他は全員が読むだけ。
これは誰かが覚えておくべきルールではない。**他に呼べるものが存在しないから、自然にそうなる。**

### A typical sequence / 典型的な流れ

**EN** — What actually happens, in order, for one run:

**JA** — 1 回の実行で実際に起きること、順番に:

```text
1. MazeGenerator     Maze(width, height, reserved=<"42" cells>)   ← every wall closed
2. MazeGenerator     neighbours(pos)      "where can I go from here?"
3. MazeGenerator     open_passage(a, b)   "carve" — repeated until the maze is done
4. Solver W12        open_neighbours(pos) walks the finished maze, breadth first
5. Encoder W13       rows()               nine ints -> "bd3 / c3a / d46"
6. Renderer W15      rows() / is_open()   draws the same nine ints on screen
```

**EN** — Steps 1–3 build, steps 4–6 read. **The maze never changes after step 3.**
**JA** — 1〜3 が構築、4〜6 が読み取り。**ステップ 3 以降、迷路は二度と変化しない。**

### For javi — the four members W13 and W15 need / javi 向け:必要なのはこの 4 つ

```python
maze.width          # int
maze.height         # int
maze.rows()         # Iterator[tuple[int, ...]] — top to bottom, left to right, one int per cell
maze.is_open(pos, Direction.NORTH)   # bool, if you prefer asking per wall
```

**EN** — For W13 the whole output grid is `for row in maze.rows(): ...` — each `int` is already the value of the
hex digit, so the encoder is a formatting step, not a translation. For W15 use `is_open` if that reads better than
masking bits by hand.
**JA** — W13 は `maze.rows()` を回すだけで出力グリッドが得られる。各 `int` がそのまま 16 進桁の値なので、
エンコーダは変換ではなく整形の工程になる。W15 はビットを自分でマスクするより `is_open` の方が読みやすければそちらを。

## 3. Implementation steps / 実装手順

<!-- One commit per step. What each achieves, not how. -->

1. `Direction` with its bit values, `opposite` and `delta`, plus its unit tests.
2. `Maze.__init__` — allocate the grid with **every wall closed**, store `reserved`.
3. Bounds checking and the read accessors (`contains`, `walls_at`, `is_open`).
4. `open_passage` — the invariant: update both cells or neither.
5. `neighbours` / `open_neighbours`.
6. `rows`.

**EN** — Note step 2: cells start fully closed (`15` / `0xf`), so a **reserved cell that is never touched stays
`0xf` by construction** — which is exactly §IV.4's "the 42 is drawn by fully closed cells". No extra code paints
the pattern; it is what remains when the generator does not carve.
**JA** — ステップ 2 に注目。セルは全壁が閉じた状態(`15` / `0xf`)から始まるので、
**一度も触らない確保セルは自動的に `0xf` のまま残る**。これは §IV.4 の「42 は完全に閉じたセルで描かれる」そのもの。
パターンを描くコードは要らない。生成器が掘らなかった結果として現れる。

## 4. Edge cases / エッジケース

> §IV.2: the program must never crash unexpectedly. Every row here becomes a test.

| # | Input / situation | Expected behaviour |
| --- | --- | --- |
| E1 | `open_passage` on two cells that are not orthogonally adjacent | `NotAdjacentError` |
| E2 | `open_passage` where `a == b` | `NotAdjacentError` |
| E3 | `open_passage` on a cell outside the grid | `OutOfBoundsError` |
| E4 | `open_passage` touching a **reserved** cell | `MazeError` — the "42" must stay closed |
| E5 | `walls_at` / `is_open` on a position outside the grid | `OutOfBoundsError` |
| E6 | `width` or `height` below 1 | `ValueError` at construction |
| E7 | `neighbours` at a corner | yields 2 entries, never an out-of-bounds one |
| E8 | reserved cells disconnect the walkable region | **not detected here** — W10's validator owns it |
| E9 | `open_passage` called twice on the same pair | idempotent, no error |

## 5. Complexity / 計算量とその根拠

| Operation | Time | Space | Why acceptable |
| --- | --- | --- | --- |
| `walls_at`, `is_open`, `open_passage` | O(1) | — | direct indexing plus one bit operation |
| `neighbours`, `open_neighbours` | O(1) | — | at most 4 candidates |
| `rows` (full pass) | O(W·H) | O(W) per row | one tuple per row, not per maze |
| construction | O(W·H) | O(W·H) ints | 20×15 = 300 ints; even 500×500 = 250k ints is unremarkable |

**EN** — The realistic input is the config's `WIDTH`/`HEIGHT`. At ten times the subject's example the structure is
still trivial; the cost that grows is the generator's, not this module's.
**JA** — 現実的な入力は設定の `WIDTH`/`HEIGHT`。subject の例の 10 倍でもこの構造は些細なまま。
効いてくるのはこのモジュールではなく生成器側のコスト。

## 6. Test plan / テスト方針

| Test | Kind | Checks |
| --- | --- | --- |
| `test_all_walls_closed_on_init` | unit | every cell is `0xf` after construction |
| `test_open_passage_updates_both_cells` | **invariant** | after opening, `a` lost the wall **and** `b` lost `opposite` — the §IV.4 coherence rule |
| `test_open_passage_rejects_*` | edge | E1–E4 each raise the right type |
| `test_rows_shape_and_order` | unit | `height` rows, `width` ints each, top-to-bottom and left-to-right |
| `test_reserved_cells_stay_closed` | property | after any sequence of `open_passage` calls, every reserved cell is still `0xf` |
| `test_no_wall_can_be_opened_except_via_open_passage` | design | the grid attribute is private; nothing else writes it |

- Verified with `maze_analyzer.py`? Not directly — this module produces no file. The analyzer checks the coherence
  invariant on the **output**, so it validates this design indirectly once W13 exists.

## 7. Rejected alternatives / 却下した案

| Option | Why rejected |
| --- | --- |
| A `Cell` class holding four wall flags (3.1 option B) | The shared wall would still be stored twice, so the invariant problem is unchanged, and the hex conversion comes back. Readability is recovered at the boundary by wrapping the grid in `Maze` instead. **javi agreed on 2026-08-20 that the skeleton file could go, and `maze/cell.py` was removed.** |
| An explicit graph of nodes and edges (3.1 option C) | The invariant becomes unbreakable, but every geometric requirement — the 3x3 rule, placing the "42", rendering — needs the grid rebuilt each time. |
| `grid[x][y]` (3.2 option B) | Output and rendering are both row-oriented; storing columns first would make javi's side read transposed on every loop. |

## 8. Open questions / 未解決

- [ ] **Q1.** Does `Maze` know the entry and exit? This plan says **no** — they come from the config and mean
  nothing structurally. `MazeGenerator` (W18) would hold them instead. javi: does W13 need them from the maze, or
  will it take them from the config? / `Maze` は入口と出口を持つか。この計画では**持たない**。
- [ ] **Q2.** Should `rows()` yield `tuple[int, ...]` or a `list`? Tuples are immutable, so a caller cannot corrupt
  the grid through a returned row. / 返すのはタプルかリストか。タプルなら呼び出し元から壊せない。
- [ ] **Q3.** Where is `reserved` computed? W09 builds the "42" cells and passes them in at construction — confirm
  that ordering with 3.6 = A. / `reserved` はどこで計算するか。

## 9. Changelog / 変更履歴

| Date | Change | Reason |
| --- | --- | --- |
| 2026-08-20 | initial draft | unblocks javi's W13 / W15 (his work log of 2026-08-19) |
