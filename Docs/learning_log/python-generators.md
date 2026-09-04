# Generators — functions that hand out values one at a time

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-09-01 |
| **Where it is used / 使い所** | `maze/maze.py` — `neighbours`, `open_neighbours`, `rows` |
| **Written with AI? / AI 併用** | yes — drafted with Claude while implementing the three iterator methods (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — Write `yield` instead of `return` and the function stops building a list: it hands out one
value, pauses, and continues from there when the next value is asked for.
**JA** — `return` の代わりに `yield` と書くと、その関数はリストを作るのをやめる。
**値を 1 つ渡して止まり、次を求められたら続きから再開する。**

## 2. Why it is needed / なぜ必要か

**EN** — Three methods on `Maze` are declared as returning `Iterator[...]`, so the contract promises
values one at a time rather than a finished list. The caller writes the same `for` loop either way,
but nothing has to be collected first — and, more importantly for us, **the type says out loud that
the result is walked once**.
**JA** — `Maze` の 3 つのメソッドは `Iterator[...]` を返すと宣言している。
つまり契約が約束しているのは「完成したリスト」ではなく「1 つずつ渡すこと」。
呼ぶ側の `for` は同じだが、先に全部を集める必要がなくなる。そして我々にとってより重要なのは、
**型が「これは 1 回しか回せない」と明言している**こと。

## 3. What you need to know first / 前提として知っておくこと

**EN** — A `for` loop does not need a list. It needs something it can ask "give me the next value"
until that thing says it has none left. A list can answer that, and so can a generator — the
difference is that a list has every value stored already, while a generator computes each one on
demand.
**JA** — `for` はリストを必要としない。「次の値をくれ」と聞ける相手がいればよく、
相手が「もう無い」と言うまで繰り返す。リストもそれに答えられるし、ジェネレータも答えられる。
違いは、**リストは全部を既に保持しているのに対し、ジェネレータは求められた分だけ計算する**こと。

## 4. How it works / 仕組み

### 4.1 `yield` turns a function into a generator function / `yield` が関数を変える

**EN** — One `yield` anywhere in the body is enough. The function no longer runs when called.
**JA** — 本体のどこかに `yield` が 1 つあれば十分。**その関数は、呼ばれても実行されなくなる。**

```text
def gen():
    print("<- the body ran")
    yield 1

g = gen()        prints nothing. A generator object was created, that is all
                 type(g) -> generator

list(g)          "<- the body ran"   the body starts only now
```

**EN** — This is the part that surprises people, and it surprised our test suite: the body — including
any validation at the top — does not execute until the first value is requested.
**JA** — ここが驚かれる点で、実際に我々のテストを驚かせた。
**本体は、冒頭の検証も含めて、最初の値を求められるまで実行されない。**

### 4.2 A generator is walked once / ジェネレータは使い切り

```text
g = maze.open_neighbours((1, 1))

list(g)   ->  [(1, 0), (2, 1)]
list(g)   ->  []                    exhausted; there is no rewind
```

**EN** — A list can be looped over as many times as you like. A generator cannot: once it has handed
out its last value it is finished. If the same values are needed twice, either wrap the call in
`list()` or call the method again — each call produces a fresh generator.
**JA** — リストは何度でも回せる。ジェネレータは回せない。最後の値を渡した時点で終わり、巻き戻しはない。
同じ値が 2 回要るなら、`list()` で受けるか、メソッドをもう一度呼ぶ(**呼ぶたびに新しいジェネレータができる**)。

### 4.3 Filtering without building anything / 何も作らずに絞り込む

**EN** — With a list you create an empty one, append to it, and return it. With `yield` there is no
container at all: you simply yield the values that qualify, and skip the rest.
**JA** — リストなら、空のリストを作り、`append` して、返す。`yield` なら入れ物が存在しない。
**条件に合うものを yield するだけで、残りは何もしなくてよい。**

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — What the three methods on `Maze` hand out, and how they build on each other:
**JA** — `Maze` の 3 つが何を渡し、どう積み上がっているか:

```text
neighbours((1,1))          yields (Direction, Coord) pairs, walls ignored
    NORTH -> (1, 0)
    EAST  -> (2, 1)        at a corner only two are yielded; positions outside
    SOUTH -> (1, 2)        the grid and reserved cells are simply skipped
    WEST  -> (0, 1)
        │
        │  open_neighbours filters this stream with is_open
        ▼
open_neighbours((1,1))     yields Coord only, for walls that are open
    (1, 0)                 after carving north and east
    (2, 1)

rows()                     yields one tuple per row, top to bottom
    (15, 15, 15, 15, 15)
    (15, 15, 15, 15, 15)   printing each int as a hex digit gives a line
    (15, 15, 15, 15, 15)   of the output file
```

**EN** — `open_neighbours` never builds a list of neighbours to filter. It consumes the stream from
`neighbours` and yields the ones that pass, so at no point does a container of candidates exist.
**JA** — `open_neighbours` は絞り込むためのリストを作らない。
`neighbours` の流れをそのまま受けて、通ったものを yield する。
**候補の入れ物は、どの瞬間にも存在しない。**

### The failure that taught us this / これを教えてくれた失敗

```text
def test_neighbours_raises_outside_grid() -> None:
    with pytest.raises(OutOfBoundsError):
        m.neighbours((6, 4))        ->  Failed: DID NOT RAISE
```

**EN** — The bounds check is the first line of `neighbours`, so this looked certain to raise. It did
not: calling the method only created the generator. Forcing it with `list(...)` raised as expected.
The test was right and revealed a real property of the code.
**JA** — 境界チェックは `neighbours` の 1 行目にあるので、確実に例外が出ると思われた。出なかった。
呼び出しはジェネレータを作っただけだった。`list(...)` で回すと期待どおり例外が出た。
**テストは正しく、コードの実際の性質を暴いた。**

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| Calling a generator function runs its body. / 呼べば本体が動く。 | It creates a generator object and returns. The body starts at the first requested value. / ジェネレータオブジェクトを作って返すだけ。本体は最初の値を求められたときに始まる。 |
| Validation at the top of the function protects the caller immediately. / 冒頭の検証はすぐ効く。 | Not in a generator function — it runs when the generator is first advanced. Say so in the docstring, or validate in a normal function that returns the generator. / ジェネレータでは効かない。docstring に書くか、検証だけ普通の関数で行う。 |
| A generator can be looped over twice. / 2 回回せる。 | It is exhausted after one pass. Wrap it in `list()` if the values are needed again. / 1 周で使い切り。再利用するなら `list()` に受ける。 |
| `Iterator[...]` and `list[...]` are interchangeable in a signature. / 宣言はどちらでもよい。 | `Iterator` tells the caller the result is single-use. Declaring a list and returning a generator misleads them. / `Iterator` は「使い切り」を伝える。宣言と実物が食い違うと誤解を招く。 |
| `m.rows` gives you the rows. / これで行が取れる。 | Without `()` it is the method object itself, not a result. Only `@property` methods are read without parentheses. / 括弧が無ければメソッドそのもの。括弧なしで読めるのは `@property` だけ。 |

## 7. How we use it here / この課題での使い方

**EN** —
- `neighbours` yields `(Direction, Coord)` pairs, skipping positions outside the grid and reserved
  cells, so no caller has to check for either.
- `open_neighbours` consumes that stream and yields only the cells whose shared wall is open. Path
  finding and connectivity checks walk these.
- `rows` yields one tuple per row. Tuples, not the stored lists, so a row handed to the encoder or
  the renderer cannot write back into the maze.
- Its docstring records that `OutOfBoundsError` arrives "when the generator is first advanced",
  because §IV.2 asks for predictable failure and the timing here is not the obvious one.

**JA** —
- `neighbours` は `(Direction, Coord)` の組を渡し、盤外と確保セルを飛ばす。
  だから呼ぶ側はどちらも確認しなくてよい。
- `open_neighbours` はその流れを受け、共有する壁が開いているセルだけを渡す。
  経路探索と連結性の確認がこれを辿る。
- `rows` は 1 行 1 タプル。保持しているリストではなくタプルなので、
  エンコーダや描画に渡した行から迷路を書き換えられない。
- docstring に「例外はジェネレータが最初に進んだときに来る」と明記した。
  §IV.2 が予測可能な失敗を求めており、**ここのタイミングは自明ではない**ため。

## 8. Self-check / 確認問題

- [ ] Q1. What single thing turns a function into a generator function? /
  関数をジェネレータ関数に変えるのは何か
- [ ] Q2. `g = gen()` prints nothing although `gen` starts with a `print`. Why? /
  `gen` の先頭に `print` があるのに何も出ないのはなぜか
- [ ] Q3. Why did `pytest.raises` report `DID NOT RAISE` for a check on the function's first line? /
  1 行目の検査なのに `DID NOT RAISE` になったのはなぜか
- [ ] Q4. `list(g)` twice gives values then nothing. What would a list do instead? /
  リストならどうなるか
- [ ] Q5. `open_neighbours` filters `neighbours`. How many containers exist while it runs? /
  実行中、入れ物はいくつ存在するか
- [ ] Q6. Why is `m.rows` different from `m.rows()`, while `m.width` needs no parentheses? /
  なぜ `m.rows` と `m.rows()` は違い、`m.width` には括弧が要らないのか

## 9. Still unclear / まだ分かっていないこと

- [ ] Whether the eager-validation shape (a plain function that checks, then returns an inner
  generator) is worth it for consistency with `walls_at`, which fails on call. /
  検証だけ先に走らせる形にして `walls_at` と揃えるべきか
- [ ] `yield from`, for a generator that delegates to another one — not needed yet. /
  別のジェネレータに委譲する `yield from` — まだ必要になっていない

## 10. Related / 関連

- [`python-enum-and-property.md`](python-enum-and-property.md) — properties, and why `m.width` needs
  no parentheses while `m.rows()` does
- [`pytest-basics.md`](pytest-basics.md) — the test that exposed the laziness
- `Docs/implementation_plans/maze-data-structure.md` §2 — the three signatures

## 11. Sources

> **EN** — Pointers only.
> **JA** — ポインタのみ。

- Python documentation — generators, `yield`, and `collections.abc.Iterator`
- `Docs/subject/ja.subject.md` §III.1 — type hints are graded, so the declared `Iterator` matters
