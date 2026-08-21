# generation-algorithm

| | |
| --- | --- |
| **Owner / 担当** | so (W05, W06, W07, W08, W09) |
| **Status / 状態** | draft — three open questions below must be settled before step 6 / 下の未解決 3 件はステップ 6 の前に決める |
| **Date / 日付** | 2026-08-20 |
| **Subject ref** | §IV.4, §VIII |
| **Related / 関連** | `maze-data-structure.md`; `Docs/pair_communication/01_kickoff.md` § 3.4, 3.5, 3.6, 3.7, 3.10; `Docs/learning_log/maze-generation-algorithms.md` |

---

## 1. Scope / 対象範囲

### In scope

- Filling a `Maze` with passages so that it satisfies §IV.4, in both modes.
- `PERFECT=True` — a spanning tree over the walkable cells.
- `PERFECT=False` (**the default**) — full connectivity, at least two independent loops, dead ends rare.
- Reproducibility from a seed.
- Computing the reserved "42" cells and leaving them untouched.

### Out of scope

| Not here / ここではやらない | Where it belongs |
| --- | --- |
| The grid, the wall bits, `open_passage` | W03 / W04 — `maze-data-structure.md` |
| Independent verification of the result | W10 — the validator checks what this module claims |
| Shortest path, hex output, rendering | W12 / W13 / W15 |
| The public API of the reusable package | W18 — `mazegen-package-api.md` (this class is its core) |

### Requirements it satisfies

> §IV.4 — random but reproducible from a seed; full connectivity; coherent shared walls; no corridor wider than
> 2 cells (**no 3x3 open area**); a visible "42" drawn by fully closed cells; with `PERFECT=True` exactly one path
> between any two cells; by default a playable board — four corners and the centre open, **at least two
> independent routes**, dead ends rare (none is the §VIII bonus).

## 2. Interface / インターフェース

> **Signatures only. No function bodies.** / **シグネチャのみ。関数本体は書かない。**

```python
from random import Random

from maze.maze import Coord, Maze, MazeError


class GenerationError(MazeError):
    """Raised when the requested maze cannot be built (decision 3.9 = A)."""


class MazeGenerator:
    """Builds a maze. This is the reusable class §VI requires."""

    def __init__(
        self,
        width: int,
        height: int,
        *,
        perfect: bool = False,
        seed: int | None = None,
    ) -> None: ...

    @property
    def seed(self) -> int: ...

    def generate(self) -> Maze: ...

    # --- pipeline stages, private ---------------------------------------
    def _pattern_cells(self) -> frozenset[Coord]: ...

    def _carve_spanning_tree(self, maze: Maze, rng: Random) -> None: ...

    def _dead_ends(self, maze: Maze) -> list[Coord]: ...

    def _braid(self, maze: Maze, rng: Random) -> None: ...
```

**EN** — `perfect` defaults to `False` because §IV.4's default is the playable board, not the perfect maze. Making
the signature agree with the subject removes a whole class of "which one is the default again?" bugs.
**JA** — `perfect` の既定を `False` にしているのは、§IV.4 の既定が完全迷路ではなく遊べる盤面だから。
シグネチャを subject に一致させておくと、「どっちが既定だったか」に由来するバグが丸ごと消える。

**EN** — `seed` is a property, not just a constructor argument: when the config gives none we generate one, and the
caller must be able to read it back. A maze you cannot reproduce is a bug report you cannot write.
**JA** — `seed` を property にしているのは、設定にシードがないとき自分で生成するから。
呼び出し側が読み戻せないと意味がない。再現できない迷路は、バグ報告が書けない迷路。

## 3. The pipeline / 生成の流れ

<!-- What each stage achieves, not how it achieves it. One commit per stage. -->

| # | Stage | What it achieves |
| --- | --- | --- |
| 1 | Resolve the seed | One `Random` instance owned by this object. Nothing else in the program touches it. |
| 2 | Compute the "42" cells | The set of cells the pattern occupies. If the maze is too small to hold it, **skip the pattern and print an error to the console** — §IV.4 says so explicitly. |
| 3 | Construct the `Maze` | Passing that set as `reserved`. Every wall starts closed, so untouched reserved cells stay `0xf` on their own. |
| 4 | Carve a spanning tree | Recursive backtracker, **iteratively with an explicit stack** (decision 3.5). Walks only non-reserved cells. Result: every walkable cell reachable, exactly one path between any two. |
| 5 | If `perfect` | Done. Return the maze. |
| 6 | Otherwise, braid | Remove walls at dead ends until the default-mode conditions hold: at least two independent loops, dead ends rare, and no 3x3 open area created in the process. |

**EN** — Stages 4 and 6 are the whole design: **one pipeline, one algorithm, and `PERFECT=True` is simply the
pipeline stopping early** (decision 3.4 = A). There is no second generator to keep in step with the first.
**JA** — ステージ 4 と 6 が設計の本体。**パイプラインは 1 本、アルゴリズムも 1 つで、
`PERFECT=True` は途中で止めるだけ**(決定 3.4 = A)。もう 1 つの生成器を同期させ続ける必要がない。

## 4. Three consequences worth knowing before writing this / 書く前に知っておくべき 3 つの帰結

### 4.1 Stage 4 cannot produce a 3x3 open area — only stage 6 can / 3x3 を作りうるのはステージ 6 だけ

**EN** — A perfect maze cannot contain even a 2x2 open block: four mutually connected cells are a loop of four
nodes and four edges, and a tree has no loops. So §IV.4's corridor-width rule is satisfied by stage 4 **for free**,
and it constrains only stage 6. That is what decision 3.7 is actually about — see Q1.

**JA** — 完全迷路には 2x2 の開放ブロックすら存在しえない。4 セルが互いに繋がれば 4 点 4 辺の輪になり、
木の定義に反するため。したがって §IV.4 の通路幅の規則はステージ 4 では**無料で**満たされ、
制約するのはステージ 6 だけ。決定 3.7 が実際に扱っているのはそこ(Q1 参照)。

### 4.2 "At least two independent loops" is a subtraction, not a search / 独立ループ数は引き算で出る

**EN** — For a connected graph, the number of independent cycles is `E − V + 1`, where `E` is the number of carved
passages and `V` the number of walkable cells. So the §IV.4 condition is:

```text
carved_passages − walkable_cells + 1 ≥ 2        i.e.   carved_passages ≥ walkable_cells + 1
```

Stage 4 leaves exactly `V − 1` passages, so **every wall stage 6 removes adds exactly one independent loop.**
Braiding twice already satisfies the requirement; the hard part is the dead-end count, not the loops.

**JA** — 連結なグラフでは、独立な閉路の数は `E − V + 1`(`E` は開通した通路の数、`V` は歩けるセルの数)。
つまり §IV.4 の条件は上の不等式そのものになる。
ステージ 4 はちょうど `V − 1` 本を残すので、**ステージ 6 で壁を 1 枚取り除くたびに独立ループが 1 つ増える。**
2 枚取れば要件は満たされる。難しいのはループの方ではなく行き止まりの数。

> **EN** — This affects Q2 in `01_kickoff.md`, which listed union-find as the candidate tool for counting loops.
> Counting does not need it — a subtraction does. Union-find would still be a reasonable way to check
> **connectivity** (the `C` in `E − V + C`), which is a different question.
> **JA** — これは `01_kickoff.md` の Q2 に影響する。ループ数の計数に union-find は要らない(引き算で済む)。
> ただし**連結性**の確認(`E − V + C` の `C`)には依然として妥当な道具で、そちらは別の問い。

### 4.3 The "42" must not cover the corners or the centre / 「42」は四隅と中央を覆えない

**EN** — §IV.4's default mode requires the four corners and the centre to be open passages. Every non-reserved
cell is part of the spanning tree, so this is automatically true **unless the reserved pattern covers one of those
cells**. Since the "42" is naturally placed in the middle of the maze, the centre is the one at real risk. This is
a constraint on stage 2, not a separate stage.

**JA** — §IV.4 の既定モードは四隅と中央が通路であることを要求する。
確保セル以外はすべて全域木の一部になるので、**確保パターンがそれらのセルを覆わない限り**自動的に満たされる。
「42」は迷路の中央に置くのが自然なので、実際に危ないのは中央。
これはステージ 2 への制約であって、独立したステージではない。

## 5. Edge cases / エッジケース

| # | Input / situation | Expected behaviour |
| --- | --- | --- |
| E1 | Maze too small for the "42" | Skip the pattern, print an error to the console, **continue** (§IV.4) |
| E2 | The pattern would cover a corner or the centre, in default mode | Reposition or skip it — never produce a board that violates §IV.4 |
| E3 | The reserved cells disconnect the walkable region | `GenerationError` — a spanning tree cannot cover a disconnected region |
| E4 | `width` or `height` of 1 | Still valid: a single row or column is a legal spanning tree. Default mode cannot hold two loops, so `PERFECT=False` must fail explicitly rather than return a board that violates §IV.4 |
| E5 | Default mode on a maze too small for two independent loops | `GenerationError` with a message naming the minimum |
| E6 | Same seed, same parameters | Byte-identical maze, always |
| E7 | Braiding removes a wall that would create a 3x3 open area | Must not happen — see Q1 |
| E8 | `generate()` called twice on the same object | Returns an equivalent maze; the second call must not continue from the first one's state |

## 6. Complexity / 計算量とその根拠

Let `V = width × height` be the cell count.

| Stage | Time | Space | Why acceptable |
| --- | --- | --- | --- |
| 4 — carve | O(V) | O(V) for the stack and the visited set | every cell is pushed and popped once |
| 6 — dead-end scan | O(V) | O(V) for the list | each cell's degree is at most 4 |
| 6 — braid | O(V) per pass | — | bounded by the number of dead ends, itself ≤ V |
| whole `generate()` | **O(V)** | O(V) | 20×15 = 300 cells is instant; 500×500 = 250k is still linear |

**EN** — The iterative form matters here: written recursively, stage 4's depth reaches O(V) *on the interpreter's
stack*, which Python caps around 1000. With an explicit stack the same O(V) lives on the heap and the limit
disappears.
**JA** — ここで反復版であることが効く。再帰で書くとステージ 4 の深さが**インタプリタのスタック上で** O(V) に達し、
Python の上限(1000 前後)に当たる。明示的スタックなら同じ O(V) がヒープ上に載り、上限が消える。

## 7. Test plan / テスト方針

| Test | Kind | Checks |
| --- | --- | --- |
| `test_same_seed_same_maze` | property | two generators with the same seed produce identical `rows()` output |
| `test_perfect_is_a_tree` | invariant | carved passages == walkable cells − 1, and every cell reachable |
| `test_all_cells_reachable` | invariant | both modes; BFS from any walkable cell reaches all of them |
| `test_pattern_cells_stay_closed` | invariant | every reserved cell is still `0xf` after `generate()` |
| `test_default_mode_has_two_loops` | unit | `E − V + 1 ≥ 2` (see §4.2) |
| `test_default_mode_dead_ends` | unit | dead ends below the agreed threshold (Q1) |
| `test_no_3x3_open_area` | edge | after braiding, in default mode |
| `test_too_small_for_pattern_warns` | edge | E1 — error printed, generation continues |
| `test_generate_twice` | edge | E8 |

- Verified with `maze_analyzer.py`: **yes, and this is the module where it matters most.** The analyzer reports
  whether the output is perfect or playable, which is exactly what stages 4 and 6 claim. Run it on both modes at
  every integration checkpoint.

## 8. Rejected alternatives / 却下した案

| Option | Why rejected |
| --- | --- |
| Randomized Prim (3.5 B) | Roughly three times as many dead ends to start from — precisely the work stage 6 has to undo. |
| Randomized Kruskal (3.5 C) | On a grid, adjacency follows from the coordinates, so an edge list plus union-find is more machinery for the same result. |
| Two separate generation paths (3.4 B) | Twice the surface to write, test and explain, for two modes that share everything except the last stage. |
| Carve first, then close the "42" (3.6 B) | Closing cells afterwards can disconnect the maze, and the repair can break the corridor-width or dead-end rules — a fix that needs a fix. |
| Recursive form of the backtracker (3.5 A, recursive) | Depth reaches O(V) on the interpreter stack; §IV.3 lets the config ask for a maze large enough to hit the limit. |

## 9. Open questions / 未解決

- [ ] **Q1 — decision 3.7, now narrowed.** Since only stage 6 can create a wide corridor (§4.1), how do we stop it?
  Check each candidate wall before removing it, or braid freely and re-validate? Checking first is cheaper and
  always terminates. **This must be settled before stage 6 is written.** /
  3.7 の論点は「ステージ 6 で広い通路を作らせない方法」に絞られた。取り除く前に判定するか、自由に取ってから再検証するか。
- [ ] **Q2 — decision 3.10, seed handling.** Proposed: own `Random` instance, and when the config gives no seed,
  generate one and **print it**. Needs so's confirmation. /
  3.10。提案は「自前の `Random` を持ち、設定にシードがなければ生成して表示する」。要確認。
- [ ] **Q3 — how rare is "rare"?** §IV.4 says dead ends should be rare and §VIII rewards zero. What number do we
  target, and does the analyzer's `--max-dead-ends` define it for us? /
  「稀」とは何個か。analyzer の `--max-dead-ends` がその定義を与えてくれるか。
- [ ] **Q4 — where is "the centre"?** For an even `WIDTH` or `HEIGHT` there is no single centre cell. Define it
  once, here, before §4.3 becomes a bug. / `WIDTH` や `HEIGHT` が偶数のとき中央のセルは一意でない。先に定義する。

## 10. Changelog / 変更履歴

| Date | Change | Reason |
| --- | --- | --- |
| 2026-08-20 | initial draft | 3.5 decided; W05 can start once Q1–Q4 are answered |
