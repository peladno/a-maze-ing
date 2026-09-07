# Truthiness and `None` — why "empty" and "absent" are not the same question

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-09-05 |
| **Where it is used / 使い所** | `maze/config.py` — `seed`, `minimum`, `_BOOL`, `_as_filename` |
| **Written with AI? / AI 併用** | yes — drafted with Claude after hitting the same trap three times (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — Every object is either true or false in a condition, and **"empty" counts as false** — so `if x` cannot
tell "there is no value" from "the value is 0, or empty, or False".
**JA** — あらゆるオブジェクトは条件式の中で真か偽になり、**「空」は偽として数えられる。**
だから `if x` は「値が無い」と「値が 0・空・False である」を区別できない。

## 2. Why it is needed / なぜ必要か

**EN** — The config parser has three places where "absent" and "falsy" collide, and all three are real settings a
user is allowed to write:

**JA** — 設定パーサには「未指定」と「偽の値」が衝突する箇所が 3 つあり、
**3 つともユーザーが書いてよい正当な設定**である:

| Setting / 設定 | Absent means / 未指定の意味 | The falsy value that is legal / 正当な偽の値 |
| --- | --- | --- |
| `SEED` | the file said nothing; the generator picks / ファイルが何も言っていない。生成器が決める | `SEED=0` — a perfectly good seed / まったく正当なシード |
| `minimum` | any integer will do / どんな整数でもよい | `minimum=0` — the bound for a coordinate / 座標の下限 |
| `PERFECT` | (mandatory, never absent) | `False` — the default mode of §IV.4 / §IV.4 の既定モード |

**EN** — Writing `if seed:` or `if minimum:` in any of those three lines produces a bug that only appears for the
value 0 — which is exactly the value a tester is least likely to try.
**JA** — この 3 か所で `if seed:` や `if minimum:` と書くと、**値が 0 のときだけ現れるバグ**になる。
そして 0 は、テストで最も試されにくい値。

## 3. What you need to know first / 前提として知っておくこと

**EN** — `if x` does not compare anything. It calls `bool(x)` and branches on the result. Every type decides for
itself what makes an instance false, and the rule is almost always "empty or zero".
**JA** — `if x` は何とも比較していない。**`bool(x)` を呼び、その結果で分岐している。**
各型が「どういうときに偽になるか」を自分で決めており、その規則はほぼ常に「空、またはゼロ」。

## 4. How it works / 仕組み

### 4.1 The complete list of falsy values / 偽になる値の一覧

```text
False        the boolean
None         the absence of a value
0  0.0       numeric zero
""           the empty string
[]  ()  {}   the empty list, tuple, dict
set()        the empty set
```

**EN** — **Everything else is true.** Including `"0"`, `"False"`, `" "`, `[0]` and `{"": None}` — a container with
one useless item in it is still non-empty.
**JA** — **それ以外はすべて真。** `"0"`、`"False"`、`" "`、`[0]`、`{"": None}` も含む。
**中身が無意味でも、空でなければ非空。**

### 4.2 The famous one / 有名な例

```text
bool("False")   ->  True        a non-empty string, whatever it says
bool("0")       ->  True        same
bool(0)         ->  False       the number, not the text
```

**EN** — This is why `PERFECT` is read through a table rather than through `bool()`. `bool(value)` would answer
True for every spelling a user could write, including `False` itself.
**JA** — `PERFECT` を `bool()` ではなく対応表で読む理由がこれ。
`bool(value)` は**ユーザーが書きうるあらゆる綴りに True を返す。`False` そのものを含めて。**

### 4.3 Three questions that look alike / 似て見える 3 つの問い

| Written / 書き方 | Asks / 聞いていること | True for / 真になるのは |
| --- | --- | --- |
| `if x:` | is it truthy? / 真値か | anything not in the list above / 上の一覧に無いものすべて |
| `if x == 0:` | does it equal zero? / 0 と等しいか | `0`, `0.0`, and `False` — because `False == 0` / `0`、`0.0`、そして `False`(`False == 0` のため) |
| `if x is None:` | **is it that one object?** / **あの 1 つのオブジェクトそのものか** | only `None` / `None` のみ |

**EN** — `is` asks about identity, not value. `None` exists exactly once in a running program, so `is None` is
the only one of the three that cannot be fooled.
**JA** — `is` は値ではなく**同一性**を問う。`None` は実行中のプログラムに**ただ 1 つしか存在しない**ので、
**3 つのうち騙されないのは `is None` だけ。**

### 4.4 The same trap in `dict.get` / `dict.get` に潜む同じ罠

```text
_BOOL.get("False")   ->  False       found it. The value is False
_BOOL.get("yes")     ->  None        not found
```

**EN** — Both are falsy, so `if not result:` treats a successful lookup of `False` as a failure. Either compare
with `is None`, or ask `in` first and index second — which is what the code does, because it reads plainly.
**JA** — どちらも偽なので、`if not result:` は **`False` の取得成功を失敗として扱う。**
`is None` で比べるか、先に `in` で確かめてから添字で引くか。
**コードは後者を採っている。素直に読めるため。**

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — The bound check in `_as_int`, written both ways, against three inputs:
**JA** — `_as_int` の下限チェックを 2 通りで書き、3 つの入力に当てたもの:

```text
                          if minimum:          if minimum is not None:
minimum = 1               checks the bound     checks the bound          same
minimum = None            skips the check      skips the check           same
minimum = 0               SKIPS THE CHECK      checks the bound          DIFFERENT
                             │                     │
                             │                     └─ ENTRY=-1,0 is rejected
                             └─ ENTRY=-1,0 is accepted, and a negative
                                coordinate reaches the maze
```

**EN** — Only one row differs, and it is the row the coordinates use. `if minimum:` would pass every test written
with `minimum=1`, then fail silently on the one case it was introduced for.
**JA** — 違うのは 1 行だけ。そしてそれが**座標が使う行**。
`if minimum:` は `minimum=1` で書かれたテストをすべて通過し、
**そのあと、まさに導入した目的の場面で静かに壊れる。**

### The three sightings in this module / このモジュールでの 3 回

| # | Where / 場所 | What "falsy but legal" means there / そこでの「偽だが正当」 |
| --- | --- | --- |
| 1 | `Config.seed: int | None` | `SEED=0` is a usable seed; `None` means the file was silent / `SEED=0` は使えるシード。`None` は「ファイルが黙っていた」 |
| 2 | `_as_int(..., minimum)` | `minimum=0` is the bound for coordinates; `None` means unbounded / `minimum=0` は座標の下限。`None` は下限なし |
| 3 | `_BOOL` instead of `bool()` | `False` is a legitimate answer, not a failed conversion / `False` は正当な答えであって、変換の失敗ではない |

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| `if x:` and `if x is not None:` are interchangeable. / どちらでも同じ。 | They differ for every falsy value: 0, "", [], False. / 偽になる値すべてで違う。0、""、[]、False。 |
| `bool("False")` is False. / False になる。 | True. The string is non-empty, and its contents are never read. / True。空でない文字列であり、中身は読まれない。 |
| `x == None` is fine. / 問題ない。 | It works, but `is None` states identity, which is what you mean. / 動くが、意図しているのは同一性。`is None` がそれを言う。 |
| `if not d.get(k):` tests whether the key is missing. / キーの有無を調べている。 | It also fires when the key exists and holds a falsy value. / 値が偽のときも真になる。 |
| An empty string is the same as no value. / 空文字列と未指定は同じ。 | `OUTPUT_FILE=` is a key that was written with nothing after it — a different mistake from not writing the key. / `OUTPUT_FILE=` は「書いたが中身が無い」。キーを書かなかったのとは別の誤り。 |

## 7. How we use it here / この課題での使い方

**EN** —
- `seed: int | None` and `minimum: int | None` both use `None` for "not specified", and both are tested with
  `is None`. The type says out loud that absence is possible.
- `_BOOL` exists because `bool()` cannot read a spelling. The table is also what builds the rejection message.
- `if not filename:` is deliberate: at that point the value has already been stripped, so the **only** falsy string
  it can be is `""` — the E30 case.
- `if line == "":` in `_read_pairs` says the same thing more explicitly. Either reads correctly; being consistent
  matters more than which one.

**JA** —
- `seed: int | None` と `minimum: int | None` はどちらも「未指定」を `None` で表し、どちらも `is None` で判定する。
  **型が「無い可能性がある」と明言している。**
- `_BOOL` があるのは、`bool()` に綴りが読めないため。**表は拒否メッセージの材料にもなっている。**
- `if not filename:` は意図的。その時点で値は strip 済みなので、**偽になりうる文字列は `""` だけ**(E30)。
- `_read_pairs` の `if line == "":` は同じことをより明示的に言っている。**どちらも正しく、揃っていることの方が重要。**

## 8. Self-check / 確認問題

- [ ] Q1. List the falsy values from memory. /
  偽になる値を思い出して列挙せよ
- [ ] Q2. `bool("False")` — what does it return, and why? /
  何を返し、それはなぜか
- [ ] Q3. Which row of the `if minimum:` trace differs, and what breaks because of it? /
  トレースのどの行が異なり、その結果何が壊れるか
- [ ] Q4. Why can `is None` not be fooled, while `== None` and `if x` can? /
  なぜ `is None` は騙されず、`== None` と `if x` は騙されうるのか
- [ ] Q5. `_BOOL.get("False")` returns False. Why is `if not result:` wrong after it? /
  そのあとの `if not result:` はなぜ誤りか
- [ ] Q6. `OUTPUT_FILE=` and a missing `OUTPUT_FILE` line raise different exception types. Which, and why? /
  この 2 つが別の例外型になるのはなぜか

## 9. Still unclear / まだ分かっていないこと

- [ ] Whether `if not x:` or `if x == "":` should be the house style for empty strings — the module currently uses
  both. / 空文字列の判定をどちらに統一するか。現状は両方使っている
- [ ] Whether `Config` should keep `seed` as `int | None` or resolve it at construction — that is decision 3.10,
  still open. / `seed` を `int | None` のまま持つか、構築時に解決するか(決定 3.10、未決)

## 10. Related / 関連

- [`python-exceptions.md`](python-exceptions.md) — the other way a function avoids overloading its return value
- [`python-enum-and-property.md`](python-enum-and-property.md) — `is` versus `==`, first met with `Direction`
- `Docs/implementation_plans/config-parser.md` D5 — why `PERFECT` is read from a table

## 11. Sources

> **EN** — Pointers only. / **JA** — ポインタのみ。

- Python documentation — *Truth Value Testing*, and `object.__bool__`
- `Docs/subject/ja.subject.md` §IV.3, §IV.4 — `PERFECT` and the mandatory seed
