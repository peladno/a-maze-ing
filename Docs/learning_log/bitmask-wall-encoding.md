# Bitmask wall encoding — how four walls fit in one number

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-08-23 |
| **Where it is used / 使い所** | `maze/maze.py` (`Direction`, `walls_at`, `is_open`), W13 hex encoder, subject §IV.5 |
| **Written with AI? / AI 併用** | yes — drafted with Claude while implementing `Direction` and the accessors (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — Each cell's four walls are stored as four bits of a single number, so one cell is one
hexadecimal digit.
**JA** — 1 セルの 4 枚の壁を 1 つの数の 4 ビットとして持つ。だから 1 セルが 16 進 1 桁になる。

## 2. Why it is needed / なぜ必要か

**EN** — §IV.5 requires the output file to carry **one hexadecimal digit per cell**. A digit has
16 values, which is exactly four yes/no answers — one per wall. Storing the walls any other way
would mean converting at the edge; storing them like this means the encoder only has to format.
**JA** — §IV.5 は出力ファイルに **1 セル 1 桁の 16 進数**を要求する。1 桁は 16 通り、
つまり「はい/いいえ」4 つ分に正確に一致する — 壁 1 枚につき 1 つ。
他の持ち方をすると端で変換が要るが、この持ち方なら**エンコーダは整形するだけ**で済む。

## 3. What you need to know first / 前提として知っておくこと

**EN** — A number written in base 2 is a row of `0`s and `1`s, and **each digit is a bit**. Bits are
numbered from the right, starting at 0. A bit is **"set"** when it is `1`.
**JA** — 2 進で書いた数は `0` と `1` の並びで、**その 1 桁ずつがビット**。番号は右から 0 で数える。
ビットが `1` のとき「**立っている**」という。

```text
11 in base 2 is 1011
                ↑↑↑↑
                │││└ bit0   set
                ││└─ bit1   set
                │└── bit2   not set
                └─── bit3   set
```

## 4. How it works / 仕組み

**EN** — Think of four switches in a row, one per wall. §IV.5 fixes which switch is which, and
**ON means the wall is closed** — the counter-intuitive half of the rule.
**JA** — 壁 1 枚につき 1 つ、スイッチが 4 つ並んでいると考える。どのスイッチがどの壁かは §IV.5 が
決めている。そして **ON が「閉じている」** — ここが直感に反する側。

```text
   bit3   bit2   bit1   bit0
    W      S      E      N          set bit = wall closed

NORTH  =  1  ->  0 0 0 1
EAST   =  2  ->  0 0 1 0
SOUTH  =  4  ->  0 1 0 0
WEST   =  8  ->  1 0 0 0
```

**EN** — Every `Direction` value has **exactly one bit set, and it is its own**. That is not a
coincidence; it is what makes the two operations below work without any lookup table.
**JA** — `Direction` の各値は「**自分の桁だけが立っている**」形になっている。偶然ではなく、
下の 2 つの操作を対応表なしで成立させるためにそうした。

### `|` sets and combines / `|` は立てる・合わせる

**EN** — OR keeps a bit if **either** side has it.
**JA** — OR は「**どちらか**にあれば残す」。

```text
    0001   (NORTH)
  | 0010   (EAST)
  = 0011   -> 3

  NORTH | EAST | SOUTH | WEST  =  1111  =  15  =  _ALL_WALLS
```

### `&` isolates and tests / `&` は取り出す・調べる

**EN** — AND keeps a bit only if **both** sides have it. Since a `Direction` has exactly one bit,
ANDing with it **erases every other bit** and leaves only that wall's state. That is what "masking"
means.
**JA** — AND は「**両方**にあるときだけ残す」。`Direction` はビットが 1 つだけなので、
AND を取ると**他の桁がすべて消え**、その壁の状態だけが残る。これが「マスクする」ということ。

```text
    1011   (mask = 11)          1011   (mask = 11)
  & 0001   (NORTH)            & 0100   (SOUTH)
  = 0001   -> closed          = 0000   -> open
```

| a | b | `a \| b` | `a & b` |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | **1** | 0 |
| 1 | 0 | **1** | 0 |
| 1 | 1 | **1** | **1** |

**EN** — OR is generous, AND is strict.
**JA** — OR は甘く、AND は厳しい。

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — Take the top-left cell of the 3x3 maze traced in
[`maze-generation-algorithms.md`](maze-generation-algorithms.md) §2.2. Only its south passage was
carved; north and west are the outer border, and the wall to its east was never opened.
**JA** — [`maze-generation-algorithms.md`](maze-generation-algorithms.md) §2.2 で手で追った 3x3 の
迷路の、左上のセルを取る。開通したのは南だけで、北と西は外周、東との間の壁は開けていない。

```text
wall    state    bit    contributes
------------------------------------
North   closed   bit0   + 1
East    closed   bit1   + 2
South   OPEN     bit2   + 0
West    closed   bit3   + 8
                        ------
                          11   ->  0b1011  ->  hex 'b'
```

**EN** — `walls_at((0, 0))` returns `11`. W13 prints it as `b`, and that is the **first character of
the output file**. Nothing is converted — the stored integer already *is* the digit.
**JA** — `walls_at((0, 0))` が返すのは `11`。W13 はそれを `b` と表示し、それが**出力ファイルの
1 文字目**になる。変換は起きていない。保存している整数が**すでに桁そのもの**。

```text
bd3        <- row 0, the cell above is its first digit
c3a
d46
```

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| A set bit means the wall is open. / ビットが立っている = 開いている。 | The opposite. **Set means closed**, so a fresh cell is `15`, not `0`. / 逆。**立っている = 閉**。だから新しいセルは `0` ではなく `15`。 |
| `+` and `\|` are interchangeable for combining bits. / ビットを合わせるのに `+` と `\|` は同じ。 | Same result *only* while the bits do not overlap. `1 + 1 = 2` carries into another digit; `1 \| 1 = 1` does not. / ビットが重ならない間だけ同じ。`+` は繰り上がって別の桁に化ける。 |
| `mask & direction == 0` groups as `(mask & direction) == 0`. / そう解釈される。 | **No.** `&` binds *looser* than `==` in Python, so it reads `mask & (direction == 0)`. Parenthesise the AND. / **違う。** Python では `&` の方が `==` より優先度が低い。AND を括ること。 |
| `walls_at` computes something. / 何かを計算している。 | It reads `self._grid[y][x]` and returns it. The bounds check is the only other line. / `self._grid[y][x]` を読んで返すだけ。他の行は境界チェックだけ。 |

## 7. How we use it here / この課題での使い方

**EN** —
- `Direction` holds the bit order in one place, so no second table can drift from §IV.5.
- `walls_at(pos)` hands out the raw mask — W13's hexadecimal digit.
- `is_open(pos, d)` masks with `&` and negates, so the solver (W12) and the renderer (W15) never
  touch bits.
- `_ALL_WALLS` is `NORTH | EAST | SOUTH | WEST`, which is the state every cell starts in — and the
  state a reserved "42" cell keeps, because nothing ever carves it.

**JA** —
- `Direction` がビット順を 1 か所に閉じ込めるので、§IV.5 とずれる第二の表が生まれない。
- `walls_at(pos)` は生のマスクを渡す。これが W13 の 16 進の桁。
- `is_open(pos, d)` は `&` でマスクして反転するので、ソルバ(W12)も描画(W15)もビットに触らない。
- `_ALL_WALLS` は `NORTH | EAST | SOUTH | WEST`。全セルの初期状態であり、
  **「42」の確保セルが保ち続ける状態**でもある(誰も掘らないため)。

## 8. Self-check / 確認問題

- [ ] Q1. Why does one hexadecimal digit hold exactly one cell? / なぜ 16 進 1 桁がちょうど 1 セル分か
- [ ] Q2. A cell reads `6`. Which walls are open? / あるセルが `6` だった。開いている壁はどれか
- [ ] Q3. Why does `&` with a `Direction` leave only that wall's state? / なぜ `Direction` との `&` で
  その壁の状態だけが残るのか
- [ ] Q4. What goes wrong if `_ALL_WALLS` used `+` and two directions shared a bit? /
  もし 2 つの方位が同じビットを共有していたら、`+` で何が起きるか
- [ ] Q5. Why is `mask & direction == 0` not what it looks like? / なぜ見た目どおりに解釈されないのか
- [ ] Q6. A reserved "42" cell always reads the same value. Which, and why? /
  確保セルは常に同じ値になる。いくつで、なぜか

## 9. Still unclear / まだ分かっていないこと

- [ ] Whether `IntFlag` would have read better than `IntEnum` here — see
  [`python-enum-and-property.md`](python-enum-and-property.md) §6 /
  ここは `IntFlag` の方が読みやすかったか
- [ ] How the renderer decides how many characters a cell occupies (decision 4.3, javi's call) /
  描画が 1 セルを何文字で描くか(決定 4.3、javi の判断)

## 10. Related / 関連

- [`python-enum-and-property.md`](python-enum-and-property.md) — why `Direction` is an `IntEnum`
- [`maze-generation-algorithms.md`](maze-generation-algorithms.md) §2.2 — the maze traced above
- `Docs/implementation_plans/maze-data-structure.md` — the contract for `walls_at` and `is_open`
- `Docs/implementation_plans/architecture-overview.md` §2 — the same maze in four forms

## 11. Sources

> **EN** — Pointers only.
> **JA** — ポインタのみ。

- `Docs/subject/en.subject.pdf` §IV.5 — the bit order and the output format
- `maze_analyzer.py` — checks that neighbouring cells encode a shared wall identically
