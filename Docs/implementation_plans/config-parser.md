# config-parser

|                          |                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| **Owner / 担当**   | so (W01, W02)                                                                                    |
| **Status / 状態**  | implemented 2026-09-13 — javi's review of §2 still pending / 実装済み。§2 の javi レビューは未了                                            |
| **Date / 日付**    | 2026-09-02                                                                                       |
| **Subject ref**    | §IV.2, §IV.3, §IV.4                                                                           |
| **Related / 関連** | `Docs/pair_communication/01_kickoff.md` § 3.2, 3.9, 3.10; `architecture-overview.md` step 1 |

> **This is the first thing that runs, and the only place the outside world enters the program.**
> Everything downstream — the generator, the solver, javi's writer — receives values that this module has already
> declared trustworthy.
> **これはプログラムで最初に走るものであり、外の世界が入ってくる唯一の入口。**
> 下流(生成器・ソルバ・javi の writer)が受け取るのは、このモジュールが「信用できる」と宣言し終えた値。

---

## 0. What the config file is for / 設定ファイルは何のためにあるのか

> **EN** — Read this section first if the module's purpose is not obvious. The rest of the file assumes it.
> **JA** — このモジュールの目的がぴんと来ない場合は、まずここを読む。以降はこの節を前提にする。

### 0.1 The program has exactly one input / このプログラムの入力は 1 つだけ

**EN** — §IV.2 fixes the command:

```bash
python3 a_maze_ing.py config.txt
```

There are no command-line flags, no prompts, no environment variables. **Every choice the user is allowed to make
is a line in that file.** How big the maze is, where you enter it, where you leave it, where the result is
written, whether it is a perfect maze — all of it arrives as text, through one file, at one moment.

**JA** — §IV.2 は実行コマンドを上記に固定している。コマンドラインオプションも、対話入力も、環境変数もない。
**ユーザーに許された選択は、すべてこのファイルの 1 行として届く。**
迷路の大きさ、どこから入るか、どこから出るか、結果をどこに書くか、完全迷路かどうか — 全部が、
1 つのファイルを通して、1 回の瞬間に、テキストとしてやってくる。

### 0.2 What the module actually does / このモジュールが実際にやること

**EN** — It turns **text the user wrote** into **values our code can trust**. That is the whole job, and both
halves of the sentence matter:

**JA** — **ユーザーが書いたテキスト**を、**我々のコードが信用できる値**に変える。仕事はこれだけだが、
この文の前半と後半の両方に意味がある:

```text
config.txt (text, untrusted)              Config (values, trusted)
┌──────────────────────────┐              ┌──────────────────────────────┐
│ # my first maze          │              │ width       = 20      int    │
│ WIDTH=20                 │  ─ parse ─▶  │ height      = 15      int    │
│ HEIGHT=15                │  ─ check ─▶  │ entry       = (0, 0)  Coord  │
│ ENTRY=0,0                │              │ exit        = (19, 14) Coord │
│ EXIT=19,14               │              │ output_file = "maze.txt"     │
│ OUTPUT_FILE=maze.txt     │              │ perfect     = False   bool   │
│ PERFECT=False            │              │ seed        = None            │
└──────────────────────────┘              └──────────────────────────────┘
    strings, any shape,                       right types, right ranges,
    possibly nonsense                         checked once, never again
```

**EN** — On the left, `20` is the two characters `2` and `0`. On the right it is the integer 20, and it is already
known to be at least 1. **The line between them is the only place in the program where "is this even a number?"
is a legitimate question.**

**JA** — 左側の `20` は `2` と `0` という 2 文字。右側では整数の 20 であり、しかも 1 以上であることが確認済み。
**この 2 つの間の線が、「そもそもこれは数か?」という問いが正当でいられる、プログラム内で唯一の場所。**

### 0.3 Why that boundary is worth a whole module / なぜそこに 1 モジュールを割くのか

**EN** — Think of it as passport control. Checks happen **once**, at the border. Past that point nobody asks again:
the generator does not wonder whether `width` might be the string `"abc"`, and javi's writer does not wonder
whether `entry` might have three numbers in it. If the checking were spread out instead, every one of those
questions would have to be asked in every function that touches the value — and the one place that forgot would be
the one that crashes.

**JA** — 入国審査だと思えばよい。検査は国境で**一度だけ**行われ、そこを通ったあとは誰も再確認しない。
生成器は `width` が文字列 `"abc"` かもしれないと疑わないし、javi の writer は `entry` に数が 3 つ入っているかも
と疑わない。もし検査が分散していたら、その値に触るすべての関数で同じ問いを繰り返すことになり、
**そして忘れた 1 か所が落ちる。**

### 0.4 Why this is the most crash-prone module in the project / ここが最も落ちやすい理由

**EN** — Every other module receives its input from us. This one receives it from a human with a text editor. §IV.2
is unambiguous about what that means:

**JA** — 他のモジュールは、入力を我々自身から受け取る。ここだけは、テキストエディタを持った人間から受け取る。
§IV.2 はその意味について曖昧さを残していない:

> §IV.2 — プログラムはすべてのエラーを丁寧に処理しなければならない:不正な設定、ファイルが見つからない、
> 構文エラー、実現不可能な迷路パラメータなど。
> **予期せずクラッシュしてはならず、常にユーザに明確なエラーメッセージを示すこと。**

**EN** — Note that three of the four examples the subject gives — a bad config, a missing file, a syntax error —
are **this module**. The fourth, impossible maze parameters, is this module and W11. §IV.2 is, in practice, mostly
a requirement about `config.py`.

**JA** — subject が挙げた 4 つの例のうち 3 つ(不正な設定・ファイルが見つからない・構文エラー)が
**このモジュール**である点に注目。4 つ目の「実現不可能なパラメータ」も、ここと W11 の話。
**§IV.2 は実質的に、その大半が `config.py` への要求。**

**EN** — Concretely, this is the failure the subject forbids:

**JA** — 具体的には、subject が禁じているのはこの落ち方:

```text
WIDTH=twenty

Traceback (most recent call last):
  File "a_maze_ing.py", line 12, in <module>
ValueError: invalid literal for int() with base 10: 'twenty'
```

and this is what it asks for instead / 求められているのはこちら:

```text
config.txt:2: WIDTH must be a positive integer, got 'twenty'
```

**EN** — Same underlying event. The difference is that the second one names the file, the line, the key, the rule
and the offending value — so the user can fix it without reading our source.

**JA** — 起きている出来事は同じ。違いは、2 つ目がファイル名・行番号・キー・規則・問題の値を名指ししていること。
**ユーザーが我々のソースを読まずに直せる。**

### 0.5 Who consumes each key / 各キーを誰が使うか

**EN** — The six mandatory keys are not decoration; each one is somebody's input:

**JA** — 必須 6 キーは飾りではなく、それぞれが誰かの入力:

| Key                   | Who reads it / 読む側                                    | What it decides / 何を決めるか                                                                                                             |
| --------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `WIDTH`, `HEIGHT` | `Maze.__init__` (W03), generator (W05), renderer (W15) | the size of the grid, so the very first object built / グリッドの大きさ。最初に作られるオブジェクトそのもの                                |
| `ENTRY`, `EXIT`   | validator (W11), solver (W12), writer (W14 — javi)      | where the path starts and ends, and the last two lines of the output file / 経路の始点と終点。出力ファイル末尾の 2 行                      |
| `OUTPUT_FILE`       | writer (W14 — javi)                                     | where the result is written / 結果の書き込み先                                                                                             |
| `PERFECT`           | generator (W05)                                          | whether the pipeline stops after the spanning tree or goes on to braiding (decision 3.4) / 全域木で止めるか、braiding まで進むか(決定 3.4) |
| `SEED` (extra)      | generator (W05)                                          | reproducibility, which §IV.4 makes mandatory / 再現性。§IV.4 が必須としているもの                                                        |

**EN** — Two of those rows are javi's, which is why this plan is worth his review even though the module is mine.

**JA** — このうち 2 行は javi 側。モジュール自体は so の担当でも、この計画を彼にレビューしてもらう価値があるのはそのため。

---

## 1. Scope / 対象範囲

### In scope

- Reading the file named on the command line, and reporting clearly when it cannot be read.
- Parsing `KEY=VALUE` lines and ignoring `#` comment lines (§IV.3).
- Converting each value to its proper type: `int`, `bool`, `Coord`, `str`.
- Rejecting anything unusable **before** a maze is generated, with a message naming the line and the reason.
- Producing **one object** that carries the whole configuration to the rest of the program.
- The default `config.txt` committed to the repository, which §IV.3 requires.

### Out of scope

| Not here / ここではやらない                                                                                                            | Where it belongs / どこの担当か                                               |
| -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Anything that needs the generated maze to be checked (is the entry reachable? is it on the outer wall? does it collide with the "42"?) | W11 (so) — see D2 below                                                      |
| Choosing a seed when none was given                                                                                                    | W05 (so) — decision 3.10, still open                                         |
| Building the maze                                                                                                                      | W05 (so) — `generation-algorithm.md`                                        |
| Printing the error to the user, and the exit code                                                                                      | W17 (javi) — `a_maze_ing.py` catches, this module raises (decision 3.9 = A) |
| Reading `sys.argv`                                                                                                                    | W17 (javi) — this module is handed a path, not a command line                |

**EN** — The last row matters for testing: because the module never looks at `sys.argv`, every test can call it
with a path or a string and needs no subprocess.

**JA** — 最後の行はテストに効く。`sys.argv` を見ないので、**すべてのテストはパスか文字列を渡すだけで済み、
サブプロセスを起こす必要がない。**

### Requirements it satisfies / 対応する要件

> §IV.3 — 設定ファイルは 1 行につき 1 つの `KEY=VALUE` の組を含む。`#` で始まる行はコメントであり、無視しなければならない。
> 必須キー:`WIDTH` `HEIGHT` `ENTRY` `EXIT` `OUTPUT_FILE` `PERFECT`。
> 有用であれば追加のキー(seed、algorithm、display mode など)を足してよい。
> **デフォルトの設定ファイルを git リポジトリに用意しなければならない。**

> §IV.2 — 予期せずクラッシュしてはならず、常にユーザに明確なエラーメッセージを示すこと。

## 2. Interface / インターフェース

> **Signatures only. No function bodies.** / **シグネチャのみ。関数本体は書かない。**

### Public API

```python
from dataclasses import dataclass
from pathlib import Path

# Same alias as maze/maze.py — (x, y), x is the column. Decision 3.2 = A.
Coord = tuple[int, int]


class ConfigError(Exception):
    """Base class for every error this module raises (decision 3.9 = A)."""


class ConfigFileError(ConfigError):
    """The file could not be read at all: missing, a directory, no permission."""


class ConfigSyntaxError(ConfigError):
    """A line exists but is not a KEY=VALUE pair."""


class ConfigValueError(ConfigError):
    """A key is present but its value cannot be used."""


class ConfigMissingKeyError(ConfigError):
    """A mandatory key never appeared."""


@dataclass(frozen=True)
class Config:
    """The whole configuration, validated, as one immutable object."""

    width: int
    height: int
    entry: Coord
    exit: Coord
    output_file: str
    perfect: bool
    seed: int | None = None


def load_config(path: str | Path) -> Config: ...


def parse_config(text: str, source: str = "<config>") -> Config: ...
```

### Why two functions / なぜ関数が 2 つあるのか

**EN** — `load_config` does one thing the tests would rather not deal with: touch the filesystem. `parse_config`
takes the text directly, so **every syntax and value test is a string literal in the test file** — no temporary
files, no cleanup, no path handling. `load_config` is then thin enough that the only thing left to test in it is
"a missing file raises `ConfigFileError`".

**JA** — `load_config` はテストが触りたくない仕事、すなわちファイルシステムへのアクセスを担当する。
`parse_config` はテキストを直接受け取るので、**構文と値のテストはすべてテストファイル内の文字列リテラルで書ける。**
一時ファイルも後片付けもパス処理も要らない。そうすると `load_config` は薄くなり、
そこに残るテストは「ファイルが無ければ `ConfigFileError`」だけになる。

**EN** — `source` exists only so the message can say `config.txt:2:` instead of `line 2:`. When the subject's own
example command is `python3 a_maze_ing.py config.txt`, naming the file costs nothing and helps when the user keeps
several.

**JA** — `source` は、メッセージを `line 2:` ではなく `config.txt:2:` と書けるようにするためだけにある。
subject の例が `python3 a_maze_ing.py config.txt` である以上、ファイル名を出すコストはゼロで、
ユーザーが設定を複数持っているときに効く。

### Exceptions raised / 送出する例外

| Exception                 | Raised when / 条件                                                             | Who catches it / 誰が捕まえるか |
| ------------------------- | ------------------------------------------------------------------------------ | ------------------------------- |
| `ConfigFileError`       | the path does not exist, is a directory, cannot be read, or is not valid UTF-8 | `a_maze_ing.py` (W17)         |
| `ConfigSyntaxError`     | a non-empty, non-comment line has no `=`, or an empty key                     | `a_maze_ing.py` (W17)         |
| `ConfigValueError`      | the key is known but the value is not usable (E7–E18 below)                   | `a_maze_ing.py` (W17)         |
| `ConfigMissingKeyError` | one of the six mandatory keys never appeared                                   | `a_maze_ing.py` (W17)         |

**EN** — All four inherit `ConfigError`, so W17 can catch that one name and still print the specific message.
**Every message includes the source, the line number and the offending text**, the same habit `open_passage`
follows by naming the offending coordinate.

**JA** — 4 つとも `ConfigError` を継承するので、W17 はその 1 つを捕まえるだけで具体的なメッセージを出せる。
**すべてのメッセージに、ソース名・行番号・問題の文字列を含める。**
`open_passage` が問題の座標を名指しするのと同じ習慣。

### Data it owns / 保持するデータ

| Name                  | Type           | Meaning / 意味                                          | Invariant / 不変条件                         |
| --------------------- | -------------- | ------------------------------------------------------- | -------------------------------------------- |
| `width`, `height` | `int`        | grid size in cells                                      | `>= 1`; large enough to hold a maze at all |
| `entry`, `exit`   | `Coord`      | `(x, y)`, origin top-left                             | both inside the grid; `entry != exit`       |
| `output_file`       | `str`        | destination path                                        | non-empty                                    |
| `perfect`           | `bool`       | §IV.4 mode selector                                    | —                                           |
| `seed`              | `int \| None` | `None` means "not given"; W05 decides what that means | —                                           |

**EN** — `Config` is `frozen=True` for the same reason `Maze` keeps its grid private: **the configuration is what
the user asked for, and no later stage gets to quietly change it.** If W05 wants a seed when none was given, it
generates and prints one — it does not write into the config and hide the fact that the file did not say so.

**JA** — `Config` を `frozen=True` にするのは、`Maze` がグリッドを private にしているのと同じ理由。
**設定は「ユーザーが要求した内容」であり、後段が黙って書き換えてよいものではない。**
W05 がシード未指定時にシードを欲しければ、生成して表示する。設定に書き込んで「ファイルにそう書いてなかった」事実を
隠すのではなく。

## 3. Implementation steps / 実装手順

<!-- One commit per step. What each achieves, not how. -->

1. **The exception hierarchy and `Config`.** No logic yet — just the vocabulary both this module and W17 will use.
   Agreeing the type names before the code exists is the point of decision 3.9 = A.
2. **The line loop — `_read_pairs`.** Strip, skip blanks and comments, split on the first `=`, collect into a
   `dict[str, tuple[str, int]]`: each value keyed by its name and carrying its line number. Syntax errors only; no
   value has a meaning yet. Covers E6–E15.
3. **Value conversion.** One converter per type — `_as_int` (with a `minimum` every caller must state), `_as_coord`,
   `_as_bool`, `_as_filename` — each taking the value and a message prefix built by `_where`. Covers E16–E24 and
   E28–E31.
4. **Mandatory keys and cross-field checks — `parse_config`.** All six present, and all missing ones reported
   together; each value read through `_take`, so its key is named once; `entry` and `exit` inside the grid
   (`_require_inside`) and different. Covers E5 and E25–E27 (see D2).
5. **`load_config`.** Read the file, translate every OS-level failure into `ConfigFileError`, delegate to
   `parse_config`.
6. **The default `config.txt`.** §IV.3 requires one in the repository; the file currently at the repo root is
   **empty**. Fill it with a commented, working example — it doubles as the documentation of our key names.

**EN** — Steps 2 and 3 are separate on purpose. A line that is not `KEY=VALUE` and a value that is not a number are
different problems for the user, and keeping them in different steps keeps them in different messages.

**JA** — ステップ 2 と 3 を分けるのは意図的。`KEY=VALUE` になっていない行と、数でない値は、
ユーザーにとって別の問題。**工程を分けておくと、メッセージも自然に分かれる。**

## 4. Edge cases / エッジケース

> §IV.2: the program must never crash unexpectedly. Every row here becomes a test.
> §IV.2:予期せぬクラッシュは絶対にしない。ここの各行がそのままテストになる。

### 4.1 The file itself / ファイルそのもの

| #  | Input / situation                                | Expected behaviour                                                    |
| -- | ------------------------------------------------ | --------------------------------------------------------------------- |
| E1 | the path does not exist                          | `ConfigFileError` — "no such file"                                 |
| E2 | the path is a directory                          | `ConfigFileError`                                                   |
| E3 | the file exists but cannot be read (permissions) | `ConfigFileError`                                                   |
| E4 | the file is not valid UTF-8                      | `ConfigFileError` — decoding is a read failure, not a syntax error |
| E5 | the file is empty                                | `ConfigMissingKeyError` listing all six                             |
| E6 | the file contains only comments and blank lines  | same as E5                                                            |

### 4.2 Line syntax / 行の構文

| #   | Input / situation                                  | Expected behaviour                                                                             |
| --- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| E7  | `WIDTH` (no `=`)                               | `ConfigSyntaxError` with the line number                                                     |
| E8  | `=20` (empty key)                                | `ConfigSyntaxError`                                                                          |
| E9  | `  # comment` (leading whitespace)               | treated as a comment — whitespace is stripped before the `#` test                            |
| E10 | `OUTPUT_FILE=my#maze.txt`                        | the value**keeps** the `#` — see D3                                                   |
| E11 | ` WIDTH = 20 ` (whitespace around key and value) | accepted, `width == 20`                                                                       |
| E12 | `WIDTH=20` appearing twice                       | `ConfigValueError` — a duplicate is a mistake, not an override; see D4                      |
| E13 | `COLOUR=blue` (unknown key)                      | accepted and ignored; §IV.3 allows extra keys, so an unknown one may be one we removed        |
| E14 | `width=20` (lower case key)                      | `ConfigMissingKeyError` for `WIDTH` — keys are case-sensitive, as the subject writes them |
| E15 | CRLF line endings                                  | accepted; `\r` is stripped with the rest of the whitespace                                    |

### 4.3 Values / 値

| #   | Input / situation                | Expected behaviour                                                            |
| --- | -------------------------------- | ----------------------------------------------------------------------------- |
| E16 | `WIDTH=` (empty value)         | `ConfigValueError`                                                          |
| E17 | `WIDTH=twenty`                 | `ConfigValueError` naming the key and the value                             |
| E18 | `WIDTH=0` or `WIDTH=-5`      | `ConfigValueError` — a maze needs at least one cell                        |
| E19 | `WIDTH=3.5`                    | `ConfigValueError` — cells are counted, not measured                       |
| E20 | `WIDTH=1e3`                    | `ConfigValueError` — `int()` rejects it, and so do we                    |
| E21 | `ENTRY=0` (one number)         | `ConfigValueError` — a coordinate is two numbers                           |
| E22 | `ENTRY=0,0,0` (three numbers)  | `ConfigValueError`                                                          |
| E23 | `ENTRY= 0 , 0 `                | accepted, `(0, 0)` — whitespace around each number is stripped              |
| E24 | `ENTRY=a,b`                    | `ConfigValueError`                                                          |
| E25 | `ENTRY=20,0` with `WIDTH=20` | `ConfigValueError` — outside the grid (`x` runs 0..19); see D2           |
| E26 | `ENTRY=-1,0`                   | `ConfigValueError` — negative coordinates are outside the grid             |
| E27 | `ENTRY` equal to `EXIT`      | `ConfigValueError` — §IV.4 requires them to differ                        |
| E28 | `PERFECT=True` / `False`     | accepted                                                                      |
| E29 | `PERFECT=maybe`                | `ConfigValueError` listing what is accepted; see D5                         |
| E30 | `OUTPUT_FILE=` (empty)         | `ConfigValueError`                                                          |
| E31 | `SEED=abc`                     | `ConfigValueError` — the key is optional, its value is not optional-shaped |

**EN** — E25 deserves attention: `WIDTH=20` means x runs `0..19`, so `ENTRY=20,0` is out. The subject's own example
config uses `EXIT=19,14` with `WIDTH=20`, `HEIGHT=15` — it is written to demonstrate exactly this.

**JA** — E25 は注目に値する。`WIDTH=20` なら x は `0..19` なので `ENTRY=20,0` は範囲外。
subject の例が `WIDTH=20`, `HEIGHT=15` に対して `EXIT=19,14` になっているのは、まさにこれを示すため。

## 5. Complexity / 計算量とその根拠

| Operation        | Time             | Space           | Why this is acceptable                                           |
| ---------------- | ---------------- | --------------- | ---------------------------------------------------------------- |
| `parse_config` | O(L) for L lines | O(K) for K keys | a config is under 20 lines; at 10 000 lines it is still one pass |
| `load_config`  | O(file size)     | O(file size)    | the file is read whole, which is what makes line numbers easy    |

**EN** — Nothing here is a performance question. It is listed because the plan template asks, and because the
honest answer — "one pass, and the input is tiny" — is the reason the module can afford to be exhaustive about
error messages instead of fast.

**JA** — ここに性能の論点は無い。テンプレートが求めるから書いているが、正直な答え(「1 パス、しかも入力は極小」)は
**このモジュールが速さではなくエラーメッセージの網羅性にコストを払える理由**そのもの。

## 6. Test plan / テスト方針

| Test                                                 | Kind        | Checks / 何を保証するか                                 |
| ---------------------------------------------------- | ----------- | ------------------------------------------------------- |
| `test_parses_the_subject_example`                  | unit        | the six keys from §IV.3 produce the expected `Config` |
| `test_comments_and_blank_lines_are_ignored`        | unit        | E6, E9                                                  |
| `test_whitespace_around_key_and_value_is_stripped` | unit        | E11, E23                                                |
| `test_missing_mandatory_key_names_it`              | edge        | E5 — and that the message contains the key name        |
| `test_bad_integer_raises_config_value_error`       | edge        | E17–E20                                                |
| `test_coordinate_shapes_rejected`                  | edge        | E21, E22, E24                                           |
| `test_entry_and_exit_must_be_inside_and_distinct`  | edge        | E25–E27                                                |
| `test_duplicate_key_rejected`                      | edge        | E12                                                     |
| `test_unknown_key_ignored`                         | unit        | E13                                                     |
| `test_error_message_carries_the_line_number`       | property    | every raised message contains `source:line`            |
| `test_load_config_missing_file`                    | edge        | E1 — the only test that touches the filesystem         |
| `test_load_config_reads_the_committed_config`      | integration | the repository's own default config parses (§IV.3)     |

**EN** — The last one is worth more than it looks: it is the only test that fails if we change a key name and
forget the file the evaluator will actually run.

**JA** — 最後の 1 つは見た目以上に価値がある。**キー名を変えたのに、評価者が実際に実行するファイルを直し忘れたとき、
落ちる唯一のテスト。**

- Verified with `maze_analyzer.py`? No — the analyzer reads the output file, not the config. This module is
  validated by its own tests and, indirectly, by the fact that a bad config never reaches the generator.

## 7. Decisions to make / 決めること

**EN** — Five of these are open. Each is written as options plus consequences, the same form as
`01_kickoff.md`, because each one is cheap to decide now and expensive to change once javi's W17 is written
against it.

**JA** — 5 つが未決。それぞれを選択肢と帰結の形で書いてある(`01_kickoff.md` と同じ形)。
どれも今なら安く決まり、**javi の W17 がこれ前提で書かれたあとでは高くつく。**

### D1. How the configuration is represented / 設定をどう表現するか

|             | Option / 選択肢                                                                                                  | Consequences / 帰結                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ----------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** | A frozen dataclass `Config` with typed fields (**recommended**) / 型付きフィールドを持つ frozen dataclass | Field names are checked by mypy, so `cfg.wdith` fails at lint time rather than at runtime; the type of each field is documented in one place; it cannot be mutated downstream. **Cost:** adding a key means editing the class, which is a change both of us see. / フィールド名を mypy が検査するので `cfg.wdith` は実行時ではなく lint 時に落ちる。各フィールドの型が 1 か所に書かれる。下流から変更できない。**コスト:** キーの追加はクラスの編集になり、二人に見える変更になる。 |
| **B** | `dict[str, str]` returned raw, callers convert / 生の `dict[str, str]` を返し、変換は呼ぶ側                  | Nothing to define.**Cost:** every caller repeats `int(cfg["WIDTH"])`, so §IV.2's "never crash" has to be satisfied in every one of them — the exact failure mode §0.3 describes. / 定義するものが無い。**コスト:** 呼ぶ側が毎回 `int(cfg["WIDTH"])` を書き、§IV.2 の「落ちない」を全員が守る羽目になる。§0.3 が説明した失敗そのもの。                                                                                                                                         |
| **C** | `dict[str, int \| str \| bool \| Coord]` with converted values / 変換済みの値を持つ dict                          | Conversion happens once.**Cost:** mypy cannot tell which key holds which type, so every use needs a cast or an assertion, and typos in key strings are invisible until runtime. / 変換は 1 回で済む。**コスト:** mypy はどのキーがどの型かを知らないので、使うたびにキャストか assert が要り、キー名の打ち間違いは実行時まで見えない。                                                                                                                                                 |

> Decision: **A** — a frozen `Config` dataclass. §III.1 has mypy checking this project with
> `--disallow-untyped-defs`, so typed fields are checked for free, and a misspelled field name fails at lint time
> rather than at runtime. Immutability says the same thing about the configuration that `open_passage` says about
> the walls: **there is no second place that gets to change it.**
> / **A** — frozen な `Config` dataclass。§III.1 で mypy が走るので型付きフィールドの検査は無料で付いてくる。
> フィールド名の打ち間違いは実行時ではなく lint 時に落ちる。
> 不変であることは、`open_passage` が壁について言っているのと同じことを設定について言う。
> **後から変える場所が存在しない。**

### D2. Where entry / exit are validated / 入口・出口の検証をどこでやるか

**EN** — Two different questions hide under "validate the entry": *is it inside the grid the config asked for?*
(answerable from the file alone) and *is it usable in the maze we generated?* (needs the maze — is it on the outer
wall, does it collide with the reserved "42" cells, is it reachable). The first is D2; the second is W11 either way.

**JA** — 「入口を検証する」には別々の問いが 2 つ隠れている。
*設定が要求したグリッドの内側か*(ファイルだけで答えられる)と、
*生成した迷路で実際に使えるか*(迷路が要る — 外周にあるか、「42」の確保セルと衝突しないか、到達可能か)。
前者が D2 の論点で、**後者はどちらにせよ W11。**

|             | Option / 選択肢                                                                                                                                               | Consequences / 帰結                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** | The parser checks everything knowable from the file: inside the grid, and `entry != exit` (**recommended**) / ファイルだけで分かることは全部ここで見る | An impossible config fails**before** a maze is built, so the error names the config line instead of appearing halfway through generation. §IV.2 lists "実現不可能な迷路パラメータ" as a config-time error, which is this. **Cost:** the parser needs `width` and `height` before it can check `entry`, so the checks are ordered — a second pass after all keys are read. / 実現不可能な設定が、迷路を作る**前**に落ちる。エラーは生成の途中ではなく設定の行を指す。§IV.2 が「実現不可能な迷路パラメータ」を設定時のエラーとして挙げているのはこれ。**コスト:** `entry` の検査に `width`/`height` が要るので順序が生じ、全キーを読んだあとの 2 周目になる。 |
| **B** | The parser only converts types; W11 does every semantic check / パーサは型変換だけ、意味の検査は全部 W11                                                      | One place owns "is this entry valid", so there is no line to draw.**Cost:** we generate a whole maze before discovering `ENTRY=99,99`, and the message comes from a module that no longer knows which config line said it. / 「入口が妥当か」の担当が 1 か所になり、線引きが要らない。**コスト:** `ENTRY=99,99` に気づく前に迷路を丸ごと生成する。しかもメッセージを出すのは、どの設定行が原因かをもう知らないモジュール。                                                                                                                                                                                                                                                         |

> Decision: **A** — the parser checks everything answerable from the file alone. The dividing line is stated once
> and is easy to apply: **if answering the question needs the maze, it is W11's; otherwise it is W01's.** So
> "inside the grid" and "entry ≠ exit" are checked here, while "on the outer wall", "not inside the reserved 42"
> and "reachable" wait for W11. This is also what makes the error message able to say `config.txt:4:` at all.
> / **A** — ファイルだけで答えられることはすべてパーサで見る。線引きは一度書けば適用が容易:
> **その問いに答えるのに迷路が要るなら W11、要らないなら W01。**
> したがって「グリッドの内側か」「entry ≠ exit」はここで、「外周にあるか」「確保した 42 と衝突しないか」
> 「到達可能か」は W11 に回る。**エラーメッセージが `config.txt:4:` と言えるのも、この選択の結果。**

### D3. Are `#` comments whole-line only? / `#` コメントは行頭だけか

**EN** — §IV.3 says "`#` で始まる行はコメント" — *lines that begin with `#`*. It does not mention `#` after a value.

**JA** — §IV.3 は「`#` で**始まる行**はコメント」と書いており、値のあとの `#` については何も言っていない。

|             | Option / 選択肢                                                                            | Consequences / 帰結                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** | Whole-line only, exactly as written (**recommended**) / 書かれているとおり行単位のみ | Matches the subject literally, and a filename containing `#` survives (E10). **Cost:** `WIDTH=20  # the width` silently makes the value `20  # the width`, which then fails as a bad integer — the message must be good enough that the user sees why. / subject の字面どおり。`#` を含むファイル名も壊れない(E10)。**コスト:** `WIDTH=20  # the width` は値が `20  # the width` になり、不正な整数として落ちる。メッセージが理由を示せる品質である必要がある。 |
| **B** | Also strip anything after an unquoted `#` / 値の途中の `#` 以降も落とす                 | Trailing comments work, which people expect from `.ini`-like files. **Cost:** `OUTPUT_FILE=maze#1.txt` becomes `maze`, silently writing to the wrong file — a wrong result rather than an error. / 行末コメントが書けて、`.ini` 風のファイルから来た人の期待に合う。**コスト:** `OUTPUT_FILE=maze#1.txt` が `maze` になり、黙って別のファイルに書く。**エラーではなく誤った結果。**                                                                       |

> Decision:

### D4. A key that appears twice / 同じキーが 2 回現れたとき

|             | Option / 選択肢                                                                                      | Consequences / 帰結                                                                                                                                                                                                                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **A** | Reject with `ConfigValueError` naming both lines (**recommended**) / 両方の行番号を挙げて拒否 | A duplicate is almost always an edit the user forgot to delete, and telling them is free.**Cost:** a user who deliberately keeps two `WIDTH` lines to switch between must comment one out. / 重複はほぼ常に「消し忘れた編集」で、指摘するコストはゼロ。**コスト:** 意図的に 2 行持って切り替えたい人はコメントアウトが必要になる。 |
| **B** | Last one wins / 最後の行を採用                                                                       | Matches shell-style config habits.**Cost:** the value that takes effect is the one you have to scroll to find, and a typo'd duplicate is silently obeyed. / シェル系の設定の習慣に合う。**コスト:** 実際に効く値はスクロールしないと分からない位置にあり、打ち間違いの重複が黙って通る。                                             |

> Decision:

### D5. Accepted spellings for `PERFECT` / `PERFECT` に許す綴り

**EN** — The subject writes `PERFECT=True`, Python's capitalisation. Note also that §IV.3 lists `PERFECT` as
**mandatory** while §IV.4 calls the disabled mode "the default" — those are consistent: the key must be present,
and "default" describes which mode the maze is graded as when the flag is off.

**JA** — subject の表記は `PERFECT=True`(Python の綴り)。
なお §IV.3 は `PERFECT` を**必須キー**としつつ、§IV.4 は無効側を「デフォルト」と呼んでいる。
矛盾ではない。**キーは必ず書かれていなければならず、「デフォルト」はフラグが無効のときどちらのモードで採点されるかの話。**

|             | Option / 選択肢                                                                                                                                           | Consequences / 帰結                                                                                                                                                                                                                                                                                                                                |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** | `True` / `False` only, exactly as the subject writes them / subject の綴りのみ                                                                        | Nothing to explain, and it matches every example the evaluator has.**Cost:** `PERFECT=true` is an error, which will surprise someone at least once. / 説明が要らず、評価者が持つ例と一致する。**コスト:** `PERFECT=true` がエラーになり、少なくとも一度は誰かが驚く。                                                              |
| **B** | Case-insensitive `true`/`false`, plus `1`/`0`, `yes`/`no` (**recommended**) / 大文字小文字を無視し、`1`/`0`、`yes`/`no` も受ける | Forgiving where forgiveness costs nothing, and the rejected message can list what is accepted.**Cost:** one more table to keep, and one more thing to state in the README. / 寛容にしてもコストが増えない箇所で寛容にする。拒否時のメッセージに受け付ける綴りを列挙できる。**コスト:** 表が 1 つ増え、README に書くことが 1 つ増える。 |
| **C** | Anything Python's `bool()` accepts / Python の `bool()` に任せる                                                                                       | Shortest.**Cost:** `bool("False")` is `True` — the single most famous way to get this wrong. / 最短。**コスト:** `bool("False")` は `True`。この種の間違いで最も有名なもの。                                                                                                                                                  |

> Decision: **A** — `True` and `False` only, exactly as §IV.3 writes them. The subject gives one spelling and the
> evaluator's examples use it, so accepting more would be generosity nobody asked for — paid for with a table to
> keep, a README line, and a question at the defense. The rejection message lists the two accepted spellings, which
> costs one line and turns the surprise into an instruction.
> / **A** — §IV.3 の表記どおり `True` と `False` のみ。subject が示す綴りは 1 つで、評価者の例もそれを使う。
> それ以上を受け付けるのは誰も求めていない寛容さであり、代償として表を 1 つ抱え、README に 1 行増え、
> ディフェンスで質問の対象になる。**拒否時のメッセージに受け付ける 2 つの綴りを列挙する。**
> 1 行のコストで、驚きを指示に変えられる。

### D6. Extra keys — settled by decision 3.9 / 追加キー — 決定 3.9 で合意済みの論点

**EN** — 3.9 asked for the **spelling** to be agreed before the two halves meet. Proposal, kept deliberately small:

**JA** — 3.9 が求めていたのは、両半分が出会う前に**綴りを**合わせること。提案は意図的に小さく:

| Key              | Type              | Meaning                                                                                                                                                                                                | Status          |
| ---------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| `SEED`         | `int`, optional | reproducibility (§IV.4); absent means W05 decides — decision 3.10                                                                                                                                    | proposed / 提案 |
| `ALGORITHM`    | —                | not added: we have one algorithm (3.5 = A). Adding a key we ignore is worse than no key. / 追加しない。アルゴリズムは 1 つ(3.5 = A)。無視するキーを足すのは、足さないより悪い。                        | rejected        |
| `DISPLAY_MODE` | —                | not added: 4.1 = A settled on the terminal renderer. javi to confirm he needs nothing from the config. / 追加しない。4.1 = A で端末描画に決まっている。javi に「設定から要るものは無いか」を確認する。 | javi to confirm |

## 8. Open questions / 未解決

- [ ] **Q1 — for javi.** `MazeWriter.write(maze, entry, exit, shortest_path, filepath)` already takes `entry`,
  `exit` and `filepath` as parameters, which answers Q1 of `maze-data-structure.md`: **entry and exit come from
  the config, not from `Maze`.** Confirm, and this plan becomes the place that supplies all three. /
  javi の `MazeWriter.write` が既に `entry` / `exit` / `filepath` を引数で取っており、
  `maze-data-structure.md` の Q1 に答えている。**入口・出口は `Maze` ではなく設定から来る。** 確認したい。
- [x] **Q2 — answered by javi, 2026-09-12: one `except ConfigError`.** W17 catches the base class and prints the
  message as it stands. That is what makes every message in this module user-facing by construction: there is no
  layer left to reword it, so anything unclear here is unclear on the user's screen.
  / **2026-09-12、javi の回答:`except ConfigError` 1 つ。** W17 は基底クラスを捕まえ、メッセージをそのまま表示する。
  **このモジュールのメッセージは、書き換える層がもう存在しない。** ここで不明瞭なものは、画面でも不明瞭になる。
- [ ] **Q2b — for javi.** `a_maze_ing.py` also checks for a missing file itself. `load_config` reports that case
  and three more (a directory, an unreadable file, invalid UTF-8) as `ConfigFileError`, in the `source: problem`
  format. Keeping both gives one failure two paths and two wordings. Asked on 2026-09-12, not yet answered.
  / `a_maze_ing.py` 側にもファイル存在チェックがある。`load_config` は同じ場合と他 3 種を `ConfigFileError` で
  報告する。両方残すと 1 つの失敗に 2 経路 2 書式。2026-09-12 に質問、未回答。
- [ ] **Q3.** Decision 3.10 (seed) is still blank, and `SEED=` absent is its problem, not this module's. This plan
  only promises `seed: int | None`. / 決定 3.10 が空欄。`SEED` 未指定時の扱いは W05 の問題で、
  ここは `int | None` を渡すことしか約束しない。
- [ ] **Q4.** Is there a **minimum** size below which we refuse outright? §IV.4 says the "42" may be dropped on a
  maze too small, with an error printed — so a small maze is legal and that check belongs to W09, not here. This
  plan only enforces `>= 1`. / 「42」が入らない小さな迷路は許容され、コンソールにエラーを出す(§IV.4)。
  つまり小さい迷路自体は合法で、その判定は W09。ここは `>= 1` しか見ない。

## 9. Notes / 補足

### 9.1 No coordinate conversion happens here / ここで座標変換はしない

**EN** — `01_kickoff.md` 3.2 used to say the config's `(x, y)` is "converted once at parse time in W01". That line
predated the decision to wrap the grid in a `Maze` class, and **3.2 has now been corrected** (see its
"Updated 2026-09-02" note). As built, **`Maze` speaks `(x, y)` too** — `Coord` is
`(x, y)` and the transposition to `_grid[y][x]` happens inside `Maze`, hidden from every caller. So the parser
produces `(x, y)` and hands it over unchanged; there is nothing to convert.

**JA** — `01_kickoff.md` 3.2 には、設定の `(x, y)` は「W01 のパース時に一度だけ変換する」と書いてある。
この一文は、グリッドを `Maze` クラスで包むと決める前のもの。実際に作られたものでは、
**`Maze` も `(x, y)` で話す。** `Coord` は `(x, y)` で、`_grid[y][x]` への転置は `Maze` の内側で起き、
呼ぶ側からは見えない。したがってパーサは `(x, y)` を作ってそのまま渡す。**変換すべきものは存在しない。**

**EN** — Worth stating out loud, because the kickoff line reads like an instruction to swap the order, and doing so
would break every coordinate in the program in a way that only shows up on non-square mazes.

**JA** — 明記しておく価値がある。あの一文は「順序を入れ替えろ」という指示に読め、
実際に入れ替えると**プログラム中の全座標が壊れ、しかも正方形でない迷路でしか症状が出ない。**

### 9.2 The repository's `config.txt` — resolved / リポジトリの `config.txt` — 解消済み

**EN** — §IV.3 requires a default config file in the repository, and `make run` points at `config.txt`, which was
empty until step 6. It now holds the subject's own example (20x15, `0,0` to `19,14`), so the evaluator sees numbers
they already have and the "42" has room on the default run. Its comments explain the one thing users get wrong —
the far corner is `19,14`, not `20,15` — and a commented-out `#SEED=42` documents the optional key while showing
that comment lines are ignored. `test_load_config_reads_the_committed_config` keeps it loadable. It checks only
that the file parses, so the demo values stay free to change.

**JA** — §IV.3 は既定の設定ファイルを要求し、`make run` は `config.txt` を指している。ステップ 6 までは空だった。
現在は subject 自身の例(20x15、`0,0` から `19,14`)を持つので、評価者の手元の数字と一致し、既定の実行でも「42」が
収まる。コメントは利用者が間違える唯一の点(遠い角は `20,15` ではなく `19,14`)を説明し、コメントアウトした
`#SEED=42` が任意キーを文書化しつつ、コメント行が無視されることを示す。
`test_load_config_reads_the_committed_config` が読み込める状態を保つ。検査するのは「読めること」だけなので、
デモ用の値は自由に変えられる。

## 10. Rejected alternatives / 却下した案

| Option                                                       | Why rejected / 却下理由                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `configparser` from the standard library                   | It requires section headers (`[section]`), which §IV.3's format does not have. Working around that means feeding it a fake `[DEFAULT]` header, at which point we are still writing a parser — one whose behaviour on malformed input we do not control, and §IV.2 makes that behaviour our responsibility. / セクション見出し `[section]` を要求するが、§IV.3 の形式には無い。偽の `[DEFAULT]` を足す回避策を取っても結局パーサを書くことになり、しかも不正入力時の挙動を自分たちで制御できない。§IV.2 はその挙動を我々の責任にしている。 |
| JSON or TOML                                                 | The format is fixed by §IV.3. Not an option. / 形式は §IV.3 で固定されている。選択肢ではない。                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `eval()` on the value                                      | Turns a config file into executable code. Never. / 設定ファイルを実行可能コードに変える。論外。                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Returning a list of errors instead of raising (3.9 option C) | Rejected in the kickoff: every caller would have to check the result, and §IV.2 is satisfied by one handler either way. / kickoff で却下済み。呼ぶ側が毎回結果を検査することになり、§IV.2 はどちらにせよハンドラ 1 つで満たせる。                                                                                                                                                                                                                                                                                                                    |

## 11. Changelog / 変更履歴

| Date       | Change / 変更                                                                            | Reason / 理由                                                                                                                                                                                             |
| ---------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-09-02 | initial draft                                                                            | W01/W02 is the last unwritten module javi's W17 depends on, and §IV.2's error handling lives mostly here / javi の W17 が依存する最後の未着手モジュールであり、§IV.2 のエラー処理はその大半がここにある |
| 2026-09-02 | D1 = A (frozen `Config`), D2 = A (the parser checks what the file alone can answer)     | the two decisions the implementation cannot start without; D3–D5 are message-level and can follow / 実装を始めるのに必須の 2 件。D3〜D5 はメッセージの水準の話なので後追いでよい                         |
| 2026-09-02 | corrected `01_kickoff.md` 3.2, which still described a parse-time coordinate conversion | the implemented `Maze` hides the swap, so following the old wording would transpose every coordinate / 実装された `Maze` が入れ替えを隠しているため、古い記述に従うと全座標が転置される                |
| 2026-09-03 | step 2 implemented as a private `_read_pairs` helper, with 14 tests | the syntax layer can be tested before the value and key layers exist / 値とキーの工程が無くても構文の工程だけをテストできる |
| 2026-09-03 | D5 = A (`True` / `False` only) | one spelling in the subject, so a wider table would be generosity nobody asked for / subject の綴りは 1 つ。表を広げるのは誰も求めていない寛容さになる |
| 2026-09-03 | step 3 shaped as one converter per **type**, not one branch per key | `WIDTH`/`HEIGHT` share a conversion and so do `ENTRY`/`EXIT`, so six keys need four functions and each rule is written once / `WIDTH`/`HEIGHT` と `ENTRY`/`EXIT` はそれぞれ同じ変換なので、6 キーが 4 関数に収まり、規則が 1 か所にだけ書かれる |
| 2026-09-12 | Q2 answered by javi: one `except ConfigError` in `a_maze_ing.py` | the messages are already user-facing, so there is nothing for the handler to reword / メッセージは既に利用者向けなので、ハンドラが書き換えるものがない |
| 2026-09-13 | step 4: `parse_config`, reading each value through `_take` and bounding coordinates with `_require_inside` | writing each key twice let a message name the key next to the one it read, and that passed lint, mypy and every test until the code was run / キーを 2 回書く形で、隣のキーを名乗るメッセージが lint・mypy・テストを通過し、実行するまで見つからなかった |
| 2026-09-13 | step 5: `load_config` catches `OSError` as a whole rather than by subclass | opening a directory raises `IsADirectoryError` on Linux and `PermissionError` on Windows, and the pair works on both / ディレクトリを開くと Linux と Windows で違う例外になり、二人は両方の環境で作業している |
| 2026-09-13 | step 6: `config.txt` filled with the §IV.3 example; status set to implemented | IV.3 requires a default config and `make run` already pointed at the empty file / §IV.3 が既定の設定を要求し、`make run` は空のファイルを指していた |
