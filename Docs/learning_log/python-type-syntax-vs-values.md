# Type syntax and value syntax — the same symbols, two worlds

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-09-05 |
| **Where it is used / 使い所** | `maze/maze.py`, `maze/config.py` — every annotation, and four bugs |
| **Written with AI? / AI 併用** | yes — drafted with Claude after the same class of mistake appeared four times (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — `[]`, `{}`, `()` and `|` mean one thing where a **type** is expected and something else where a **value**
is expected, and Python almost never complains when the wrong one is written.
**JA** — `[]`、`{}`、`()`、`|` は、**型**が来る場所と**値**が来る場所で意味が違う。
そして**書き間違えても、Python はほとんど文句を言わない。**

## 2. Why it is needed / なぜ必要か

**EN** — This one class of mistake has now appeared **four times** across two modules. None of the four raised an
error at the point they were written; two of them would have shipped wrong output to the user.

**JA** — この 1 種類の間違いが、2 つのモジュールで**すでに 4 回**現れている。
**4 つとも、書いた場所ではエラーにならなかった。** うち 2 つは、そのままならユーザーに誤った出力を届けていた。

## 3. What you need to know first / 前提として知っておくこと

**EN** — An annotation is not a comment. `dict[str, int]` is an expression that is **evaluated** and produces a
real object — a `types.GenericAlias`. That object accepts almost anything inside its brackets without checking,
because checking is mypy's job, not the interpreter's.

**JA** — 型注釈はコメントではない。`dict[str, int]` は**評価される式**であり、実体のあるオブジェクト
(`types.GenericAlias`)を作る。**そのオブジェクトは括弧の中身をほぼ何でも受け付ける。**
検査するのはインタプリタではなく mypy の仕事だから。

```text
type(dict[str, int])   ->  <class 'types.GenericAlias'>
dict['WIDTH']          ->  dict['WIDTH']        no error. It is a type object
tuple[-1, 0]           ->  tuple[-1, 0]         no error either
```

**EN** — That silence is the whole problem.
**JA** — **この沈黙こそが問題の本体。**

## 4. How it works / 仕組み

### 4.1 The four brackets in the value world / 値の世界での 4 種類

```text
(a, b)      a tuple, or just grouping when there is no comma
[a, b]      a list
{a, b}      a set
{a: b}      a dict
x[i]        subscription: read item i out of x
```

### 4.2 The same symbols in the type world / 型の世界での同じ記号

```text
list[int]              a list of ints
dict[str, int]         a dict from str to int
tuple[str, int]        a tuple of exactly two, in that order
tuple[int, ...]        a tuple of any length
int | None             either an int or None
```

**EN** — Note that `x[...]` is doing the same thing in both worlds — subscription. On a **value** it reads an item;
on a **class** it builds a type. `dict` is a class, so `dict[key]` builds a type, silently.
**JA** — `x[...]` は両方の世界で**同じ操作**(添字)をしている点に注意。
**値に対しては要素を読み、クラスに対しては型を作る。**
`dict` はクラスなので、`dict[key]` は**黙って型を作る。**

### 4.3 `|` / `|` について

```text
int | None       in an annotation: "either of these"
5 | 3            between values: bitwise OR -> 7
"a" | "b"        TypeError: str does not define |
```

**EN** — This one at least fails loudly, because `str` has no `|`. It is the only member of the family that does.
**JA** — これだけは大きな音で落ちる。`str` に `|` が定義されていないため。
**この仲間の中で、失敗が即座に分かる唯一の例。**

### 4.4 What catches them / 何が見つけてくれるか

| Tool / 道具 | Catches / 見つけるもの |
| --- | --- |
| the interpreter / インタプリタ | only `"" \| "#"` — the others are valid expressions / `"" \| "#"` のみ。他は正当な式 |
| **mypy** | **all of them, if the surrounding code is annotated** / **周囲に型注釈があれば、すべて** |
| flake8 | none of them / どれも見つけない |
| tests / テスト | sometimes — and sometimes the wrong output still passes a substring assertion / ときどき。**誤った出力が部分文字列 assert を通ってしまうこともある** |

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — All four sightings, in order:
**JA** — 4 回すべてを、起きた順に:

| # | Written / 書いたもの | Meant / 意図 | What Python made / Python が作ったもの | Found by / 発見者 |
| --- | --- | --- | --- | --- |
| 1 | `tuple[-1, 0]` | the coordinate `(0, -1)` / 座標 | a type object / 型オブジェクト | a failing test / テストの失敗 |
| 2 | `("" \| "#")` | a tuple of two prefixes / 2 つの接頭辞のタプル | `TypeError` at runtime / 実行時の `TypeError` | running it / 実行 |
| 3 | `dict[key]` | `pairs[key]` — read the entry / 要素の読み出し | `dict['WIDTH']`, a type object / 型オブジェクト | review — **no tool** / レビュー。**道具は無力** |
| 4 | `message = {f"..."}` | parentheses around a string / 文字列を括る括弧 | a set holding one string / 文字列 1 つを持つ集合 | **mypy** |

**EN** — Trace the third one, because it is the one nothing would have caught:
**JA** — 3 番目を追う。**何にも捕まらなかった唯一の例**だから:

```text
f"first defined on line {dict[key]}"

    dict[key]           ->  dict['WIDTH']          a GenericAlias, not the entry
    f"...{that}"        ->  "first defined on line dict['WIDTH']"

the user sees:
    config.txt:9: duplicate key 'WIDTH', first defined on line dict['WIDTH']
```

**EN** — No exception, no lint warning, and a test asserting `"config.txt:9" in message` still passes. The only
thing that fails is the user's ability to find the line.
**JA** — 例外も出ず、lint も黙り、`"config.txt:9" in message` という assert も通る。
**壊れるのは、ユーザーが行を見つけられることだけ。**

### And the fourth, which mypy caught / 4 番目は mypy が捕まえた

```text
message: str  =  {f"config.txt:2: ..."}

mypy:  Incompatible types in assignment
       (expression has type "set[str]", variable has type "str")
```

**EN** — It was caught **because the variable had been used as a string elsewhere**, so mypy knew what it should
be. Annotations are not decoration; they are what makes this class of bug findable.
**JA** — 捕まえられたのは、**その変数が他の場所で文字列として使われていたから。** mypy は「何であるべきか」を知っていた。
**型注釈は飾りではない。この種のバグを発見可能にしているのは、それ自体。**

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| Annotations are ignored at runtime. / 実行時には無視される。 | They are evaluated. `dict[key]` runs and builds an object. / 評価される。`dict[key]` は実行され、オブジェクトを作る。 |
| `{}` groups a long string across lines. / 長い文字列を括る。 | `()` does that. `{}` builds a set or a dict. / それは `()`。`{}` は集合か辞書を作る。 |
| A wrong bracket will raise something. / 何かしら落ちる。 | Three of the four sightings raised nothing at all. / 4 例のうち 3 例は何も起こさなかった。 |
| `tuple[int, int]` is a value I can compare to. / 比較できる値。 | It is a type. `(1, 2) == tuple[int, int]` is False. / 型である。比較すると False。 |
| mypy is a formality for the grade. / 採点のための形式。 | It is the only tool that sees this whole class of mistake. / この種の間違いを見られる唯一の道具。 |

## 7. How we use it here / この課題での使い方

**EN** —
- §III.1 has mypy run over the project, and `--disallow-untyped-defs` means every function is annotated. That is
  what gave mypy enough information to catch sighting 4.
- `Coord = tuple[int, int]` is an alias, so `(x, y)` order is stated in every signature that uses it. Writing
  `tuple[-1, 0]` where a `Coord` was wanted is sighting 1 — the alias did not prevent it, but the annotation on the
  function is what made the failing test legible.
- The habit that follows: **when mypy prints a type in its message, that type is usually the answer.** The fix for
  `-> Config` on `_read_pairs` was sitting inside mypy's own sentence: `got "dict[str, tuple[str, int]]"`.

**JA** —
- §III.1 で mypy がプロジェクト全体に走り、`--disallow-untyped-defs` により全関数に注釈が付く。
  **4 番目を mypy が捕まえられたのは、その情報があったから。**
- `Coord = tuple[int, int]` は別名なので、使うすべてのシグネチャに `(x, y)` の順序が書かれる。
  1 番目はそれでも防げなかったが、**関数の注釈があったからこそ、失敗したテストが読めた。**
- ここから来る習慣:**mypy がメッセージの中に型を印字したら、その型がたいてい答え。**
  `_read_pairs` の `-> Config` を直したときの正解は、mypy の文の中にあった(`got "dict[str, tuple[str, int]]"`)。

## 8. Self-check / 確認問題

- [ ] Q1. `dict['WIDTH']` — does it raise? What does it produce? /
  例外は出るか。何ができるか
- [ ] Q2. Which of the four sightings failed at runtime, and why only that one? /
  4 例のうち実行時に落ちたのはどれで、なぜそれだけか
- [ ] Q3. What is the difference between `{"a"}` and `("a")`? /
  この 2 つの違いは何か
- [ ] Q4. Why did mypy catch sighting 4 but not sighting 3? /
  なぜ mypy は 4 番目を捕まえ、3 番目を捕まえなかったのか
- [ ] Q5. `x[i]` on a value and on a class — what is the same, what is different? /
  値に対する `x[i]` とクラスに対する `x[i]`、同じ点と違う点は
- [ ] Q6. Where, in a mypy error message, does the correct annotation usually appear? /
  mypy のエラーメッセージのどこに、正しい注釈が書かれていることが多いか

## 9. Still unclear / まだ分かっていないこと

- [ ] Whether running mypy in `--strict` (the `lint-strict` rule) would have caught sighting 3. /
  `--strict` なら 3 番目を捕まえられたか
- [ ] Whether a linter plugin flags subscripting a builtin type by mistake. /
  組み込み型への誤った添字を指摘するプラグインが存在するか

## 10. Related / 関連

- [`python-enum-and-property.md`](python-enum-and-property.md) — sighting 1, met while writing `Direction.delta`
- [`python-exceptions.md`](python-exceptions.md) — sighting 4 was in an error message that would have shipped
- `Docs/subject/ja.subject.md` §III.1 — the mypy flags that make this findable

## 11. Sources

> **EN** — Pointers only. / **JA** — ポインタのみ。

- Python documentation — *Generic Alias Type*, and PEP 585 / PEP 604
- mypy documentation — the meaning of `Incompatible types in assignment`
