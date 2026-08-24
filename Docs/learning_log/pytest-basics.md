# pytest basics — and the ways a test can prove nothing

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-08-23 |
| **Where it is used / 使い所** | `tests/test_maze.py`, `make test`, subject §III.3 |
| **Written with AI? / AI 併用** | yes — drafted with Claude while writing the first tests for `Maze` (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — A test is a function whose name starts with `test_`, and the only thing that makes it a
test rather than a script is the `assert`.
**JA** — テストとは `test_` で始まる名前の関数のこと。そしてそれをスクリプトではなくテストにして
いるのは、**`assert` があること**だけ。

## 2. Why it is needed / なぜ必要か

**EN** — §III.3 says tests are **not submitted and not graded**. So their only value is to us, which
means the question is not "do we have tests" but "would this test have caught the bug". Two of the
first tests written for `Maze` would not have, and both are recorded in §6.
**JA** — §III.3 はテストを「**提出物でも採点対象でもない**」と言っている。
つまり価値は自分たちにしかなく、問うべきは「テストがあるか」ではなく「**そのバグを捕まえたか**」。
`Maze` に最初に書いた 2 つは捕まえられなかった。どちらも §6 に記録した。

## 3. What you need to know first / 前提として知っておくこと

**EN** — `assert expr` raises `AssertionError` when `expr` is false and does nothing when it is
true. It is plain Python, not a pytest feature. What pytest adds is the report: it rewrites the
expression so a failure shows the actual values.
**JA** — `assert 式` は式が偽なら `AssertionError` を起こし、真なら何もしない。
**pytest の機能ではなく素の Python**。pytest が足しているのは表示で、
式を書き換えて失敗時に実際の値を見せてくれる。

```text
>       assert broken_add(1, 1) == 2
E       assert 1 == 2
E        +  where 1 = broken_add(1, 1)
```

## 4. How it works / 仕組み

### 4.1 Discovery / 検出

| What / 対象 | Rule / 条件 |
| --- | --- |
| File / ファイル | `test_*.py` or `*_test.py` |
| Function / 関数 | name starts with `test_` |

**EN** — Nothing is registered by hand. Run from the repository root, or imports of `maze` fail.
**JA** — 登録作業は要らない。**リポジトリのルートから実行**すること。でないと `maze` の import が失敗する。

```bash
poetry run pytest -q          # what `make test` runs
poetry run pytest -v          # one line per test, with its name
poetry run pytest tests/test_maze.py::test_contains_only_accepts_positions_inside_grid
```

### 4.2 Expecting an exception / 例外を期待する

```python
with pytest.raises(ValueError):
    Maze(0, 3)
```

**EN** — The block must raise, or the test fails with `DID NOT RAISE`. **Where you put the loop
decides how much is actually checked**: `pytest.raises` is satisfied by the *first* exception and
stops the block there.
**JA** — ブロックの中で必ず例外が起きなければ `DID NOT RAISE` で失敗する。
**ループをどちらに置くかで、実際に検査される量が変わる。**
`pytest.raises` は*最初の*例外で満足し、ブロックはそこで終わる。

```text
with pytest.raises(...):      loop inside  -> only the first case is ever run
    for n in cases: f(n)

for n in cases:               with inside   -> every case is judged on its own
    with pytest.raises(...):
        f(n)
```

### 4.3 One test, one claim / 1 テスト 1 主張

**EN** — When a test asserts two things and fails, the name cannot tell you which broke, and the
second assertion is never reached. Name tests after **what should hold**, not after the function
being exercised — then `pytest -v` reads as the list of guarantees.
**JA** — 1 つのテストが 2 つを主張すると、失敗したとき名前からどちらが壊れたか分からないうえ、
2 つ目には到達しない。名前は「**何が成り立つはずか**」にする(関数名ではなく)。
そうすると `pytest -v` の出力が、そのまま**保証の一覧**として読める。

```text
test_new_maze_has_no_open_wall            <- reads as a property
test_is_open                              <- reads as "some function was run"
```

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — The same claim, checked two ways, against a function that is wrong on purpose
(`broken_add` returns `a * b`):
**JA** — わざと壊した関数(`broken_add` は `a * b` を返す)に対して、同じ主張を 2 通りで検査した結果:

```text
def test_with_print() -> None:
    print("1 + 1 =", broken_add(1, 1))        ->  PASSED

def test_with_assert() -> None:
    assert broken_add(1, 1) == 2              ->  FAILED   assert 1 == 2
```

**EN** — The print version passes, and pytest hides the output by default, so nothing is even
visible. **A test without an `assert` is a test that cannot fail.**
**JA** — print 版は通る。しかも pytest は既定で出力を捨てるので、**その print は画面にすら出ない**。
**`assert` のないテストは、落ちようのないテスト。**

### The bug a square maze hides / 正方形が隠したバグ

**EN** — `_grid` is indexed `[y][x]`. A test written `grid[w][h]` — the wrong order — passes on a
3x3 maze because both indices have the same range. On `Maze(5, 3)` it fails immediately.
**JA** — `_grid` の添字は `[y][x]`。順序を逆にした `grid[w][h]` は、
**3x3 では両方の範囲が同じなので通ってしまう**。`Maze(5, 3)` にすると即座に落ちる。

```text
Maze(4, 2)._grid  ->  [[15, 15, 15, 15],
                       [15, 15, 15, 15]]

len(_grid)     -> 2   rows    = height
len(_grid[0])  -> 4   columns = width

_grid[3][1]  -> IndexError        the wrong order
_grid[1][3]  -> 15                the right one
```

**EN** — The lesson generalises: **symmetric inputs hide mistakes.** Squares, equal values, `0` and
`1`, and a position outside on *both* axes all let a wrong test pass.
**JA** — 一般化するとこうなる。**対称な入力は間違いを隠す。**
正方形、同じ値、`0` や `1`、そして**両方の軸で範囲外**の座標は、どれも間違ったテストを通す。

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| A test that prints the values is checking them. / 値を print していれば検査している。 | It passes whatever happens, and pytest hides the output. Only `assert` judges. / 何が起きても通り、出力も表示されない。判定するのは `assert` だけ。 |
| `assert x, y == (0, 0)` compares the pair. / 対を比較している。 | `assert` has a **two-argument form**: condition, message. This asserts `x` alone. Wrap the pair: `assert (x, y) == (0, 0)`. / `assert 条件, メッセージ` の形。`x` だけを検査している。 |
| `assert value == True` is clearer than `assert value`. / の方が明確。 | The value is already a bool, so the comparison adds nothing; flake8 flags it as `E712`. Use `assert value` and `assert not value`. / 既に bool なので何も足していない。`E712` で指摘される。 |
| Putting the loop inside `pytest.raises` checks every case. / 全ケースを検査できる。 | The first exception ends the block; the rest never run. Put the `with` inside the loop. / 最初の例外でブロックが終わり、残りは実行されない。`with` をループの内側に。 |
| A passing test means the code is right. / 通れば正しい。 | It means **this** input behaved. A 3x3 grid passed an index-order bug for two rounds. / **その入力で**そう振る舞っただけ。3x3 は添字順のバグを 2 回通した。 |
| Reaching into `_grid` from a test is fine. / テストから内部を触ってよい。 | It works, but the test then breaks whenever the internals change. Prefer the public accessor once one exists. / 動くが、内部を変えた瞬間にテストが壊れる。公開アクセサができたらそちらへ。 |

## 7. How we use it here / この課題での使い方

**EN** —
- `tests/test_maze.py` holds seven tests covering `Direction`, construction, the boundary, and the
  accessors. `make test` runs them.
- The boundary test uses `Maze(5, 3)` and includes `(4, 3)` — inside on one axis, outside on the
  other. That single case is what catches an `or` written where `and` was meant.
- `test_new_maze_has_given_size_and_all_walls_closed` reads through `walls_at` rather than `_grid`,
  so it survives a change of internals.
- Tests for an *opened* wall wait for step 4: once `open_passage` exists, the state can be built
  through the public API instead of poking `_grid`.

**JA** —
- `tests/test_maze.py` に 7 件。`Direction`、構築、境界、アクセサを覆う。`make test` で走る。
- 境界のテストは `Maze(5, 3)` を使い、`(4, 3)` を含む — **片方の軸だけ範囲外**。
  `and` のつもりで `or` と書いた誤りを捕まえられるのは、この 1 ケースだけ。
- `test_new_maze_has_given_size_and_all_walls_closed` は `_grid` ではなく `walls_at` 経由で読むので、
  内部を変えても壊れない。
- 「開いた壁」のテストはステップ 4 待ち。`open_passage` ができれば、
  `_grid` を突かずに公開 API で状態を作れる。

## 8. Self-check / 確認問題

- [ ] Q1. What makes a function a test, and what makes a test able to fail? /
  何が関数をテストにし、何がテストを「落ちうるもの」にするか
- [ ] Q2. Why does `assert x, y == (0, 0)` not do what it looks like? / なぜ見た目どおりでないのか
- [ ] Q3. Loop inside `pytest.raises` or `with` inside the loop — what is the difference in what
  gets checked? / どちらに置くかで、検査される量がどう変わるか
- [ ] Q4. Why did the index-order bug survive on a 3x3 maze? / なぜ 3x3 では生き残ったのか
- [ ] Q5. Name a test in this project and say which bug it would catch. /
  このプロジェクトのテストを 1 つ挙げ、どのバグを捕まえるか言えるか
- [ ] Q6. Tests are not graded. What is the argument for writing them anyway? /
  採点されないのに書く理由は何か

## 9. Still unclear / まだ分かっていないこと

- [ ] `pytest.mark.parametrize` — turns one loop into N independent tests so the failing case is
  named in the report. Worth it once a loop covers more than a handful of cases. /
  ループを N 個の独立したテストに分ける仕組み。ケースが増えたら検討する。
- [ ] Whether to check the output with `maze_analyzer.py` from the test suite or from the
  `Makefile` (decision 2.4, still open). / analyzer をテストから呼ぶか Makefile から呼ぶか。

## 10. Related / 関連

- [`python-enum-and-property.md`](python-enum-and-property.md) — `is` versus `==`, and the traps the
  tests were written against
- [`bitmask-wall-encoding.md`](bitmask-wall-encoding.md) — what the asserted values mean
- `Docs/implementation_plans/maze-data-structure.md` §6 — the planned test list

## 11. Sources

> **EN** — Pointers only.
> **JA** — ポインタのみ。

- pytest documentation — test discovery, `pytest.raises`, assertion rewriting
- `Docs/subject/ja.subject.md` §III.3 — tests are neither submitted nor graded
