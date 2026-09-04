# Python objects behind Maze — enum, property, and four traps

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-08-23 |
| **Where it is used / 使い所** | `maze/maze.py` — `Direction`, `Maze.__init__`, the read-only properties |
| **Written with AI? / AI 併用** | yes — drafted with Claude while implementing steps 1–3 of `maze-data-structure.md` (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — An `Enum` gives a fixed set of named values, and a `@property` gives a **read-only** way out
of an object — neither of them stores anything for you.
**JA** — `Enum` は「取りうる値がこれだけ」に名前を付ける仕組み、`@property` はオブジェクトからの
**読み取り専用の出口**。**どちらも値を保存する道具ではない。**

## 2. Why it is needed / なぜ必要か

**EN** — Two things had to be impossible in `Maze`. A direction that is not one of the four, and a
`width` that disagrees with the grid. An `Enum` makes the first unrepresentable; a read-only
property makes the second unreachable from outside. Both are the same idea as decision 3.3: prevent
the bad state rather than detect it.
**JA** — `Maze` では 2 つのことを「起こりえなく」する必要があった。4 つ以外の方位と、
グリッドと矛盾した `width`。`Enum` が前者を表現不能にし、読み取り専用のプロパティが後者を
外から到達不能にする。**どちらも決定 3.3 と同じ発想** — 不正な状態を検出するのではなく、作れなくする。

## 3. What you need to know first / 前提として知っておくこと

**EN** — In a class, `__init__` runs once when an object is created, and `self` is that object.
`self.name = value` attaches a value to it; a plain local variable disappears when the method ends.
By convention a leading underscore (`self._grid`) means "internal, do not touch from outside" —
Python does not enforce it.
**JA** — クラスの `__init__` はオブジェクトが作られるときに 1 回だけ走り、`self` はそのオブジェクト自身。
`self.名前 = 値` で値が貼り付く。ただのローカル変数はメソッドが終われば消える。
先頭のアンダースコア(`self._grid`)は「内部用、外から触らない」という**慣習**で、
Python が強制するわけではない。

## 4. How it works / 仕組み

### 4.1 Enum, IntEnum, IntFlag

**EN** — All three name a fixed set of values. They differ in what happens when you do arithmetic.
**JA** — 3 つとも「決まった値の集合に名前を付ける」もの。違うのは計算したときの挙動。

| | Behaviour / 挙動 |
| --- | --- |
| `Enum` | Not a number. `Permission.READ + 1` is a `TypeError`. / 数ではない。足せない。 |
| `IntEnum` | Behaves as an `int`. `READ \| WRITE` gives a **plain `int`**, `3`. / `int` として振る舞う。組み合わせた結果は**素の `int`**。 |
| `IntFlag` | Built for combining. `READ \| WRITE` stays typed, and `WRITE in combo` works. / 組み合わせ用。型が残り、`in` で調べられる。 |

**EN** — `Direction` is an `IntEnum` because the grid stores plain `int` masks and callers ask about
**one** direction at a time. `IntFlag` would have been defensible too — see §9.
**JA** — `Direction` を `IntEnum` にしたのは、グリッドが持つのが素の `int` のマスクで、
呼ぶ側が聞くのは**単独の**方位だから。`IntFlag` も十分に正当な選択だった(§9 参照)。

### 4.2 Members belong to the class / メンバーはクラスに属する

**EN** — You never build an instance. The members are reached on the class itself, and the class is
iterable and callable-by-value.
**JA** — インスタンスは作らない。メンバーはクラスから直接たどり、クラス自体が反復可能で、
値から引くこともできる。

```python
Direction.NORTH          # the member itself
for d in Direction: ...  # all four, in definition order
Direction(4)             # look UP the member whose value is 4 -> SOUTH
Direction(15)            # ValueError: 15 is not a valid Direction
```

**EN** — `Direction(4)` **finds** a member; it does not create one. That is what `opposite` would
have needed if it computed the bit instead of looking it up in a table.
**JA** — `Direction(4)` は**探す**のであって作るのではない。
`opposite` を対応表ではなく計算で書いていたら、これが必要になっていた。

### 4.3 A property is an exit, not an entrance / property は出口であって入口ではない

```python
class Demo:
    def __init__(self, w: int) -> None:
        self._w = w          # storing is a plain assignment; no property involved

    @property
    def width(self) -> int:
        return self._w       # the only thing a property does: hand a value out
```

```text
d.width       -> 5                    read, no parentheses
d.width()     -> TypeError: 'int' object is not callable
d.width = 9   -> AttributeError: can't set attribute 'width'
```

**EN** — The third line is the point. **A property cannot be assigned to**, which is exactly why
`maze.width = 999` cannot put the object into a state its grid disagrees with. The stored attribute
and the public name must differ (`_w` vs `width`), or the property calls itself forever.
**JA** — 3 行目が要点。**property には代入できない**。だからこそ `maze.width = 999` で
グリッドと矛盾した状態を作れない。保存する名前と公開する名前は**別でなければならない**
(`_w` と `width`)。同じにすると自分自身を呼び続ける。

### 4.4 Methods live on the class / メソッドはクラスに属する

```python
from maze.maze import Maze     # the class, yes
from maze.maze import walls_at # ImportError: it is not module-level

m = Maze(5, 3)
m.walls_at((0, 0))             # call it through an instance
```

**EN** — Writing `m.walls_at(pos)` passes `m` as `self` automatically. That is all `self` is.
**JA** — `m.walls_at(pos)` と書くと、`m` が `self` として自動的に渡る。**`self` の正体はそれだけ。**

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — Where each name lives, and how it is reached:
**JA** — どの名前がどこに属し、どう到達するか:

```text
maze/maze.py  (module)
│
├── Coord              type alias        from maze.maze import Coord
├── _OPPOSITE          module constant   visible inside methods as a bare name
├── _DELTA             module constant   (functions can see module scope)
├── _ALL_WALLS         module constant
│
├── Direction          class             Direction.NORTH, for d in Direction
│   ├── NORTH..WEST    members
│   ├── opposite       property          Direction.NORTH.opposite
│   └── delta          property
│
└── Maze               class             m = Maze(5, 3)
    ├── _grid          instance attr     internal, never handed out
    ├── _width         instance attr
    ├── width          property          m.width          (read-only)
    └── walls_at       method            m.walls_at(pos)  (needs an instance)
```

**EN** — Note the asymmetry: a method can read `_OPPOSITE` by its bare name because that is module
scope, but it **cannot** read a name defined in a class body the same way — see §6.
**JA** — 非対称に注意。メソッドは `_OPPOSITE` を素の名前で読める(モジュールスコープだから)が、
**クラス本体で定義した名前は同じようには読めない** — §6。

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| A dict can sit in an `Enum` class body. / `Enum` のクラス本体に dict を置ける。 | `TypeError`. Everything in that body is treated as a member. Put lookup tables **after** the class, at module level. / 本体のものはすべてメンバー扱いになる。対応表はクラスの**後**、モジュールレベルへ。 |
| A name defined in a class body is visible inside its methods. / クラス本体の名前はメソッドから見える。 | `NameError`. A class body is not an enclosing scope. Use `self.NAME`, or make it a module constant. / クラス本体は外側のスコープにならない。`self.NAME` にするか、モジュール定数にする。 |
| `[[0] * w] * h` makes `h` independent rows. / 独立した行が `h` 個できる。 | It repeats **one** row `h` times. Writing one cell changes every row. Build rows in a comprehension. / 同じ行を `h` 回並べるだけ。1 セル書くと全行が変わる。内包表記で行ごとに作る。 |
| A default argument is re-created on every call. / デフォルト引数は呼ぶたびに作られる。 | It is evaluated **once**, at definition. A mutable default keeps the previous call's changes — which is why `reserved` defaults to `frozenset()`. / 定義時に **1 度だけ**評価される。可変なものだと前回の結果が残る。だから `frozenset()`。 |
| `tuple[-1, 0]` is a tuple. / これはタプル。 | It is a **type**: `types.GenericAlias`. It does not fail at runtime, so the wrong value travels. A tuple value uses `( )`. / これは**型**。実行時に落ちないので、間違った値が流れていく。値は `( )` で書く。 |
| `m.rows` gives the rows. / これで行が取れる。 | Without `()` it is the **method object**: `<bound method Maze.rows ...>`. Functions are values in Python, so naming one does not call it. Only `@property` methods are read without parentheses. / 括弧が無ければ**メソッドオブジェクト**。Python では関数も値なので、名前を書いただけでは呼ばれない。括弧なしで読めるのは `@property` だけ。 |
| `(x,)` and `(x)` are the same. / 同じ。 | **The comma makes the tuple, not the parentheses.** `((1,2))` is a 2-tuple; `((1,2),)` is a 1-tuple holding a pair. Needed whenever a sequence has exactly one element. / **タプルを作るのはカンマで、括弧ではない。**要素が 1 つのときだけカンマが必須になる。 |
| `is` compares values. / `is` は値を比べる。 | `is` compares **identity**. `15 is 15` is True only because small ints are cached. Use `==` for numbers, `is` for `None` and enum members. / `is` は**同一性**。整数には `==`、`None` と enum メンバーには `is`。 |

## 7. How we use it here / この課題での使い方

**EN** —
- `Direction` as an `IntEnum`, values equal to the §IV.5 bits, with `opposite` and `delta` as
  properties reading module-level tables.
- `Maze` stores `_grid`, `_width`, `_height`, `_reserved` and exposes only `width`, `height`,
  `reserved` — read-only, so the object cannot be made inconsistent from outside.
- `reserved: frozenset[Coord] = frozenset()` — immutable, so the mutable-default trap cannot bite,
  and the value is fixed at construction anyway.

**JA** —
- `Direction` は `IntEnum` で、値は §IV.5 のビットそのもの。`opposite` と `delta` は
  モジュールレベルの対応表を読むプロパティ。
- `Maze` は `_grid` / `_width` / `_height` / `_reserved` を持ち、公開するのは
  `width` / `height` / `reserved` だけ。読み取り専用なので、外から矛盾を作れない。
- `reserved: frozenset[Coord] = frozenset()` — 不変なのでデフォルト引数の罠に当たらないうえ、
  そもそも構築時に確定する値なので意味とも合う。

## 8. Self-check / 確認問題

- [ ] Q1. What does `@property` do that a plain attribute does not? / 素の属性にできないことは何か
- [ ] Q2. Inside `__init__`, which line actually stores the width? / どの行が実際に保存しているか
- [ ] Q3. Why must the stored name differ from the property name? / なぜ名前を分ける必要があるか
- [ ] Q4. Why can `opposite` read `_OPPOSITE` even though it is defined below the class? /
  クラスの下で定義された `_OPPOSITE` を、なぜ `opposite` から読めるのか
- [ ] Q5. `Direction(4)` returns `SOUTH`. Is it creating or finding? / 作っているのか探しているのか
- [ ] Q6. `[[0] * 3] * 3` then `grid[0][0] = 9`. What does the grid look like, and why? /
  グリッドはどうなり、それはなぜか
- [ ] Q7. Why does `reserved` default to `frozenset()` rather than `set()`? / なぜ `set()` ではないのか
- [ ] Q8. `m.width` needs no parentheses but `m.rows()` does. What makes the difference? / 何がその違いを作っているのか
- [ ] Q9. How do you write a tuple holding exactly one coordinate? / 座標を 1 つだけ持つタプルはどう書くか

## 9. Still unclear / まだ分かっていないこと

- [ ] Whether `IntFlag` would suit `Direction` better. It would let `walls_at()`'s result be queried
  with `in`, but the grid still stores plain ints. Worth revisiting if the validator (W10) ends up
  testing several walls at once. / `IntFlag` の方が合っていたか。W10 で複数の壁をまとめて調べる
  ことになったら再考の価値がある。
- [ ] Whether a separate `Offset` alias for `delta` would be worth it. mypy cannot tell it from
  `Coord`, so the benefit is only for the reader. / `delta` 用に別名を作るべきか。
  mypy は区別しないので、効果は読み手のみ。

## 10. Related / 関連

- [`bitmask-wall-encoding.md`](bitmask-wall-encoding.md) — why the `Direction` values are what they are
- [`pytest-basics.md`](pytest-basics.md) — how these were checked
- `Docs/implementation_plans/maze-data-structure.md` §2 — the contract, member by member

## 11. Sources

> **EN** — Pointers only.
> **JA** — ポインタのみ。

- Python documentation, `enum` module — `Enum`, `IntEnum`, `IntFlag`
- PEP 8 — leading underscore for internal names; PEP 257 — docstring conventions
- `Docs/subject/ja.subject.md` §III.1 — type hints, mypy and docstrings are graded
