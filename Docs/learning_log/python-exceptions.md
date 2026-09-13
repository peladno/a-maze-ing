# Exceptions — reporting failure without a return value

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-09-05 |
| **Where it is used / 使い所** | `maze/config.py` — the `ConfigError` family, `_as_int`, `_read_pairs` |
| **Written with AI? / AI 併用** | yes — drafted with Claude while writing the config parser (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — `raise` stops the function and hands the problem upwards until something is prepared to catch it, so a
failure never has to be squeezed into the return value.
**JA** — `raise` は関数を止め、受け止める準備のあるところまで問題を上へ渡す。
**だから失敗を戻り値に押し込む必要がない。**

## 2. Why it is needed / なぜ必要か

**EN** — §IV.2 says the program must never crash unexpectedly and must always show a clear message. Those are two
requirements, not one: *something must fail*, and *someone must explain it*. Exceptions separate the two — the
place that detects the problem describes it, and one place far away decides what the user sees.

**JA** — §IV.2 は「予期せずクラッシュしない」ことと「常に明確なメッセージを示す」ことを求めている。
これは 1 つではなく 2 つの要求。**何かが失敗すること**と、**誰かがそれを説明すること**。
例外はこの 2 つを分ける。**問題を見つけた場所が内容を記述し、遠く離れた 1 か所が「ユーザーに何を見せるか」を決める。**

## 3. What you need to know first / 前提として知っておくこと

**EN** — There are two ways a function can report failure. C's `atoi` uses the first:

**JA** — 関数が失敗を伝える方法は 2 通りある。C の `atoi` は前者:

```text
Return a sentinel        atoi("abc") -> 0      and atoi("0") -> 0
                         the caller cannot tell them apart

Raise                    int("abc")  -> ValueError
                         int("0")    -> 0
                         the return value only ever means success
```

**EN** — This is why `ft_atoi` could not report a bad input: 0 is both a legitimate result and the failure signal.
Python removes the ambiguity by taking failure out of the return value entirely.
**JA** — `ft_atoi` が不正な入力を報告できなかったのはこのため。**0 は正当な結果でもあり、失敗の合図でもある。**
Python は失敗を戻り値から完全に追い出すことで、この曖昧さを消している。

## 4. How it works / 仕組み

### 4.1 An exception is a class / 例外はクラス

**EN** — Raising creates an instance and throws it. Our own types are classes with no body at all, because what
carries the meaning is the **type**, not any behaviour.
**JA** — `raise` はインスタンスを作って投げる。自前の型は本体が空のクラス。
**意味を運んでいるのは振る舞いではなく型そのもの**だから。

```text
ConfigError                 the one name a handler needs to catch
├── ConfigFileError         the file could not be read
├── ConfigSyntaxError       a line is not KEY=VALUE
├── ConfigValueError        the value cannot be used
└── ConfigMissingKeyError   a mandatory key never appeared
```

**EN** — `except ConfigError` catches all four, because catching checks the inheritance chain. That is the whole
reason for the base class.
**JA** — `except ConfigError` は 4 つすべてを捕まえる。捕捉は継承関係をたどるため。
**基底クラスを置く理由はこれ 1 つ。**

### 4.2 `try` / `except` / `try` と `except`

```text
try:
    number = int(value)          only the line that can fail
except ValueError as err:
    ...                          entered only when it did fail
```

**EN** — Three rules, each learned the hard way by somebody:

**JA** — 規則は 3 つ。どれも誰かが痛い目に遭って得たもの:

| Rule / 規則 | Why / 理由 |
| --- | --- |
| Name the type. Never bare `except:` / 型を必ず書く。裸の `except:` は書かない | Bare `except` swallows Ctrl-C, and the program can no longer be stopped / 裸の `except` は Ctrl-C まで飲み込み、プログラムを止められなくなる |
| Never `except Exception` here / ここで `except Exception` は書かない | It swallows our own bugs. A typo becomes "your config is wrong" / 自分たちのバグまで飲み込む。打ち間違いが「設定が不正です」に化ける |
| Keep the `try` block to the failing line / `try` は失敗しうる 1 行だけに | A wide block catches an unrelated `ValueError` and mislabels it / 広く囲むと無関係な `ValueError` まで「変換に失敗」と誤解する |

### 4.3 Translating, not leaking / 漏らさずに翻訳する

**EN** — `int()` raises `ValueError`, which means nothing to a user reading it. We catch it and raise our own type
with a message that names the file and the line. The original is kept with `from`:

**JA** — `int()` が投げる `ValueError` は、読まされるユーザーにとって意味がない。
これを捕まえ、ファイル名と行番号を含むメッセージを付けて**自前の型で投げ直す**。元の例外は `from` で残す:

```text
except ValueError as err:
    raise ConfigValueError(message) from err
```

**EN** — `from err` changes nothing the user sees. It changes the traceback a developer sees:
**JA** — `from err` はユーザーが見るものを変えない。変えるのは開発者が見るトレースバック:

```text
ValueError: invalid literal for int() with base 10: 'twenty'

The above exception was the direct cause of the following exception:

ConfigValueError: config.txt:2: WIDTH must be a whole number, got 'twenty'
```

### 4.4 Where it is caught / どこで捕まえるか

**EN** — Exactly once, near the entry point (decision 3.9 = A). Catching in many places produces messages nobody
can trace; catching nowhere produces the traceback §IV.2 forbids.
**JA** — エントリポイント付近で**ちょうど 1 回**(決定 3.9 = A)。
あちこちで捕まえると誰も追えないメッセージになり、どこでも捕まえないと §IV.2 が禁じるトレースバックが出る。

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — One bad line, followed from the file to the screen:
**JA** — 不正な 1 行が、ファイルから画面まで辿る道:

```text
config.txt          WIDTH=twenty
     │
     ▼
_read_pairs         splits it into ("WIDTH", "twenty") — no complaint,
                    the syntax is fine
     │
     ▼
_as_int             int("twenty")  ->  ValueError            raised by Python
                    caught, translated, re-raised            our type, our message
     │                    ConfigValueError:
     │                    "config.txt:2: WIDTH must be a whole number, got 'twenty'"
     ▼
a_maze_ing.py       except ConfigError as err:   ->  print(err), exit 1
     │
     ▼
the user            config.txt:2: WIDTH must be a whole number, got 'twenty'
```

**EN** — Note what did **not** happen: no function returned a sentinel, no caller checked a flag, and no code
between `_as_int` and the handler had to know a failure was passing through it.
**JA** — **起きなかったこと**に注目。番兵の値を返した関数はなく、フラグを確認した呼び出し元もなく、
`_as_int` とハンドラの間のコードは、失敗が自分を通り抜けたことを**知る必要すらなかった**。

### Why `int()` is enough / なぜ `int()` だけで足りるのか

```text
int('20')      -> 20              int('3.5')    -> ValueError
int(' 20 ')    -> 20              int('1e3')    -> ValueError
int('+20')     -> 20              int('')       -> ValueError
int('-5')      -> -5              int('20abc')  -> ValueError
int('020')     -> 20              int('0x10')   -> ValueError
```

**EN** — It converts **the whole text or none of it**, which is precisely what `atoi` does not do. Five of the
plan's edge cases (E16–E20) are covered by that one call.
**JA** — **全体を変換するか、まったく変換しないか**のどちらか。これが `atoi` との最大の違い。
計画のエッジケース 5 件(E16〜E20)が、この 1 回の呼び出しで覆われる。

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| `except:` is a convenient catch-all. / 万能で便利。 | It catches `KeyboardInterrupt` too, so Ctrl-C stops working. / `KeyboardInterrupt` まで捕まえ、Ctrl-C が効かなくなる。 |
| `except Exception` is close enough. / だいたい同じ。 | It hides our own bugs behind a user-facing message. / 自分たちのバグを、ユーザー向けメッセージの裏に隠す。 |
| A wide `try` block is simpler. / 広く囲む方が楽。 | It mislabels failures that came from elsewhere in the block. / ブロック内の別の場所で起きた失敗を誤って分類する。 |
| Exceptions are for exceptional cases only, like C. / C と同じで例外的な場合だけ。 | In Python a failed conversion is an ordinary event. `int()` has no other way to answer. / Python では変換の失敗はごく普通の出来事。`int()` に他の答え方はない。 |
| An empty class body needs `pass`. / 空のクラスには `pass` が要る。 | A docstring is a statement, so it satisfies the requirement on its own. / docstring は文なので、それだけで要件を満たす。 |
| `raise X from err` changes the message. / メッセージが変わる。 | It only adds the cause to the traceback. The user sees the same line. / トレースバックに原因が加わるだけ。ユーザーが見る行は同じ。 |

## 7. How we use it here / この課題での使い方

**EN** —
- Four types under one `ConfigError`, so W17 catches one name and still prints the specific message (3.9 = A).
- `_read_pairs` raises on syntax; the converters raise on values. **The layer that finds the problem is the layer
  that describes it.**
- `int()`'s `ValueError` is translated at once, because §IV.2 asks for a message that names the line — and by the
  time the handler sees it, the line number is long gone.
- `load_config` will do the same for `FileNotFoundError`, `IsADirectoryError`, `PermissionError` and
  `UnicodeDecodeError`, turning all four into `ConfigFileError` (edge cases E1–E4).

**JA** —
- 1 つの `ConfigError` の下に 4 つの型。W17 は 1 つの名前を捕まえるだけで、具体的なメッセージを出せる(3.9 = A)。
- `_read_pairs` は構文で、変換関数は値で送出する。**問題を見つけた層が、それを記述する層。**
- `int()` の `ValueError` はその場で翻訳する。§IV.2 が求めるのは行番号を含むメッセージであり、
  **ハンドラに届く頃には行番号はとうに失われている**ため。
- `load_config` も同じことをする。`FileNotFoundError` / `IsADirectoryError` / `PermissionError` /
  `UnicodeDecodeError` の 4 つを `ConfigFileError` に翻訳する(E1〜E4)。

## 8. Self-check / 確認問題

- [ ] Q1. Why can `ft_atoi` not report a bad input, while `int()` can? /
  `ft_atoi` に不正入力を報告できず、`int()` にできるのはなぜか
- [ ] Q2. What does `except ConfigError` catch, and why? /
  `except ConfigError` は何を捕まえ、それはなぜか
- [ ] Q3. Name two things a bare `except:` swallows that you did not want swallowed. /
  裸の `except:` が飲み込んでしまう、飲み込ませたくないものを 2 つ挙げよ
- [ ] Q4. Why is the `try` block one line long? /
  なぜ `try` は 1 行しか囲んでいないのか
- [ ] Q5. What would the user see differently if `from err` were removed? /
  `from err` を消したら、ユーザーの見るものはどう変わるか
- [ ] Q6. Why is `ValueError` translated in `_as_int` rather than caught in `a_maze_ing.py`? /
  なぜ `ValueError` を `a_maze_ing.py` で捕まえず、`_as_int` で翻訳するのか

## 9. Still unclear / まだ分かっていないこと

- [ ] Whether `try` / `except` / `else` reads better than putting the success path after the block. /
  `else` 節を使う形と、ブロックの後に成功時の処理を書く形のどちらが読みやすいか
- [ ] How `load_config` should map four OS-level exceptions onto one `ConfigFileError` without losing which one
  it was. / `load_config` が OS 由来の 4 例外を 1 つに畳むとき、どれだったかを失わずに済ませる方法

## 10. Related / 関連

- [`pytest-basics.md`](pytest-basics.md) — `pytest.raises`, and why an assertion after the raising call is never
  reached
- [`python-truthiness-and-none.md`](python-truthiness-and-none.md) — the other half of "failure without a return
  value": `None` as "no value"
- `Docs/implementation_plans/config-parser.md` §2, §4 — the four types and the cases that raise them

## 11. Sources

> **EN** — Pointers only. / **JA** — ポインタのみ。

- Python documentation — *Errors and Exceptions*, and the built-in exception hierarchy
- `Docs/subject/ja.subject.md` §IV.2 — never crash, always a clear message
- `Docs/pair_communication/01_kickoff.md` 3.9 — custom types, one handler
