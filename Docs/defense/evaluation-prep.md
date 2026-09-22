# Evaluation preparation / 評価の準備

| | |
| --- | --- |
| **Source / 元の資料** | the peer-evaluation sheet, copied in `Docs/reviewmaze` / ピア評価シート(`Docs/reviewmaze` に写したもの) |
| **Checked on / 確認日** | 2026-09-22, on `main` at `2b70702` |
| **How it was checked / 確認方法** | every item below was run for real; the outputs quoted are copied from those runs / 下の各項目は実際に実行し、載せた出力はその結果の写し |

> **EN** — How to use this file. Each section follows one block of the evaluation sheet, in its order. For each item it gives what the evaluator checks, what our program does (with the real output), how to show it in the defense, and the questions likely to follow. §0 is a one-page summary; §10 lists the risks to deal with before the defense.
>
> **JA** — このファイルの使い方。各節は評価シートの 1 ブロックに対応し、同じ順番で並んでいる。項目ごとに、評価者が確かめること、私たちのプログラムがどう動くか(実際の出力つき)、評価でどう見せるか、続いて聞かれそうな質問を書いた。§0 は 1 ページの要約、§10 は評価の前に片付けるべきリスクの一覧。

---

## 0. Summary / 要約

| Sheet block / シートの項目 | Status / 状態 | Where / 詳細 |
| --- | --- | --- |
| Submitted files and Norm / 提出ファイルと Norm | OK | §1 |
| README | OK | §2 |
| Display and interactive menu / 表示と対話メニュー | OK | §3 |
| Configuration file format / 設定ファイルの形式 | OK — answer ready for lower-case keys / 小文字のキーへの説明を用意 | §4 |
| Error management / エラー処理 | OK — no case crashes / どのケースもクラッシュしない | §5 |
| Output file / 出力ファイル | OK | §6 |
| Maze generation / 迷路の生成 | OK | §7 |
| Reusable module / 再利用モジュール | OK, with an explanation ready / 説明を用意すれば OK | §8 |
| Bonus: no dead end / ボーナス:行き止まり 0 | OK | §9 |

### Demo commands in order / 評価で使うコマンド(順番どおり)

```bash
make install                                   # once / 最初に 1 回
make lint                                      # §1  flake8 + mypy
make test                                      # 135 tests
python3 a_maze_ing.py config.txt               # §3  t / c / r / q
python3 maze_analyzer.py maze.txt              # §6  mode check / モードの確認
python3 maze_analyzer.py maze.txt --max-dead-ends 0   # §9  bonus / ボーナス
make build                                     # §8  rebuild the package / パッケージを作り直す
```

---

## 1. Submitted files and Norm / 提出ファイルと Norm

**EN** — The sheet requires README.md, LICENSE.md, a_maze_ing.py, a mazegen-* `.tar.gz` or `.whl`, a configuration file, and everything needed to rebuild the package; flake8 and mypy must pass. A missing element means a grade of 0.

**JA** — シートは README.md、LICENSE.md、a_maze_ing.py、mazegen-* の `.tar.gz` か `.whl`、設定ファイル、パッケージを作り直すのに必要なもの一式を求め、flake8 と mypy が通ることを求めている。1 つでも欠けると 0 点。

| Required / 必要なもの | Our file / 私たちのファイル |
| --- | --- |
| README.md | `README.md` (first line italic / 1 行目は斜体) |
| LICENSE.md | `LICENSE.md` — MIT, skusakab and jperez-u |
| a_maze_ing.py | `a_maze_ing.py` |
| mazegen-* package / パッケージ | `mazegen-0.1.0-py3-none-any.whl` and `mazegen-0.1.0.tar.gz` |
| a configuration file / 設定ファイル | `config.txt` (+ 3 examples in `config_file_examples/`) |
| what the rebuild needs / 作り直しに必要なもの | `pyproject.toml`, `poetry.lock`, `Makefile` (`make build`), `maze/`, `mazegen/` |

**Show / 見せ方:** `ls` the root, then `make lint` → `Success: no issues found in 23 source files`.

**Likely questions / 想定質問**

- *Why MIT? / なぜ MIT?* — **EN** It explicitly allows reuse, modification and redistribution, which §VI requires of the licence, and it is short enough to read in full. **JA** §VI がライセンスに求める「再利用・改変・再配布」を明示的に許しており、全文を読める短さだから。
- *What are the mypy flags? / mypy のフラグは?* — `--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs` (§III.2). `make lint-strict` also passes `--strict`. / `make lint-strict` は `--strict` も通る。

---

## 2. README

**EN** — Every element the sheet lists is a section of `README.md`. The Japanese part mirrors the English one.

**JA** — シートが挙げる要素は、すべて `README.md` の節になっている。日本語の部分は英語の部分と同じ内容。

| Sheet element / シートの要素 | README section / README の節 |
| --- | --- |
| Italic first line / 斜体の 1 行目 | line 1: `_This project has been created as part of the 42 curriculum by skusakab, jperez-u._` |
| Description | `## Description` |
| Instructions | `## Instructions` (Setup, Run, **Controls**, Test) |
| Resources + AI use / 参考資料と AI の使い方 | `## Resources` → References, AI Usage |
| Configuration file, complete / 設定ファイルの完全な説明 | `## Configuration file` (keys, coordinates, error policy) |
| Chosen algorithm / 選んだアルゴリズム | `## Maze generation algorithm` → Execution Pipeline |
| Why / 選んだ理由 | `### Why this algorithm` |
| Reusable module / 再利用モジュール | `## Reusable module — mazegen` |
| Roles / 役割 | `## Work assignments` → Team Member Roles |
| Planning and evolution / 計画と変化 | Planning and Evolution (10 items) |
| What worked / what to improve / うまくいったこと・改善点 | What Worked Well & What Could Be Improved |
| Tools / 使った道具 | Tools Used |

**Likely questions / 想定質問**

- *How did you use AI? / AI をどう使った?* — **EN** Concept explanations, reviews with hints (not fixes), docstrings, error messages, design documents and part of the tests, all checked by mutation testing; so wrote the generator and solver code. **JA** 概念の解説、ヒントによるレビュー(修正そのものではない)、docstring、エラーメッセージ、設計文書、テストの一部。テストはミューテーションテストで検証した。生成器とソルバーのコードは so が書いた。

---

## 3. Display and interactive menu / 表示と対話メニュー

**EN** — `python3 a_maze_ing.py config.txt` prints the seed, draws the maze in the terminal and opens a menu. The sheet's three mandatory interactions are all present, plus quitting.

**JA** — `python3 a_maze_ing.py config.txt` はシードを表示し、端末に迷路を描いてメニューを開く。シートが必須とする 3 つの操作がすべてあり、終了もある。

| Key / キー | Sheet item / シートの項目 | What happens / 動作 |
| --- | --- | --- |
| `r` | Re-generate / 作り直す | new random seed (printed as `New seed: N`), new maze, output file rewritten / 新しいシードで作り直し、出力ファイルも書き直す |
| `t` | Show/hide the shortest path / 最短経路の表示切り替え | green `o` on the path / 経路に緑の `o` |
| `c` | Change wall colours / 壁の色の変更 | none → cyan → yellow → blue |
| `q` | extra: quit / 追加:終了 | `Exiting application. Goodbye!` |

Entry `E` on blue, exit `X` on red, the "42" in magenta `███`. / 入口は青背景の `E`、出口は赤背景の `X`、「42」はマゼンタの `███`。

**Show / 見せ方:** press `t`, `c` three times, `r`, `t`, `q`.

**Likely questions / 想定質問**

- *Why does `r` ignore `SEED`? / なぜ `r` は `SEED` を使わない?* — **EN** The configured seed exists to reproduce the first maze; `r` exists to see a different one. With the same seed, `r` would draw the same maze again. The file is rewritten so it always matches the screen. **JA** 設定のシードは最初の 1 枚を再現するためのもので、`r` は別の迷路を見るためのもの。同じシードでは同じ迷路しか出ない。ファイルも書き直すので、常に画面と一致する。
- *How is a row drawn? / 1 行はどう描く?* — **EN** Each row of cells becomes two text lines: the cell contents with their west walls, then the south walls. **JA** セル 1 行が文字 2 行になる:西の壁と中身の行、南の壁の行。(→ `Docs/code_guide/06_display.md`)

**Careful / 注意:** Ctrl-D or Ctrl-C at the prompt ends in a traceback (not caught). Quit with `q`. / メニューで Ctrl-D・Ctrl-C を押すと traceback になる(捕まえていない)。終了は `q` で。

---

## 4. Configuration file format / 設定ファイルの形式

**EN** — Comment lines start with `#`, each line is `KEY=VALUE`, and the six mandatory keys are WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT; SEED is optional. Blank lines are ignored, spaces around keys and values are stripped, and a value may contain `=`.

**JA** — コメント行は `#` で始まり、各行は `KEY=VALUE`。必須キーは WIDTH、HEIGHT、ENTRY、EXIT、OUTPUT_FILE、PERFECT の 6 つで、SEED は任意。空行は無視し、キーと値の前後の空白は取り除き、値に `=` が入ってもよい。

### Lower-case keys / 小文字のキー

**EN** — The sheet says "each line is in the 'KEY=VALUE' format (lower case is also OK)". The subject says nothing about case: §IV.3 of the original PDF asks for "one `KEY=VALUE` pair per line" and lists every key in capitals (`WIDTH=20` … `PERFECT=True`); the words lower case, upper case and case-insensitive appear nowhere in it. The sheet's item is "Control that the configuration files follow the requirements", so its note tells the evaluator that a team's own file may use lower case and still pass. Our files — `config.txt` and the three examples — are all in capitals, as the subject writes them.

**JA** — シートには「各行は 'KEY=VALUE' の形(小文字でもよい)」とある。subject は大文字小文字について何も言っていない。原文の PDF の §IV.3 は「1 行に 1 つの `KEY=VALUE`」を求め、キーをすべて大文字で示している(`WIDTH=20` … `PERFECT=True`)。lower case・upper case・case-insensitive といった語は PDF のどこにも無い。シートのこの項目は「設定ファイルが要件に沿っているか確かめる」ものなので、この注記は「チームの設定ファイルが小文字で書かれていても合格にしてよい」という評価者への指示と読める。私たちのファイル(`config.txt` と見本 3 つ)は、subject の書き方どおりすべて大文字。

**Decision (2026-09-22) / 決定:** keys stay case-sensitive; no change to the parser. / キーは大文字小文字を区別したまま。パーサは変えない。

**EN** — If the evaluator still tries lower-case keys, the program does not crash: it names the keys it could not find and exits with status 1.

**JA** — それでも評価者が小文字のキーで試した場合、プログラムはクラッシュしない。見つからなかったキーを示して、終了コード 1 で終わる。

```text
width=20 ... perfect=false          (every key in lower case / すべて小文字)
Error: lowercase_keys.txt: missing required keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT
exit status 1
```

**Answer to give / 答え方**

- **EN** "The subject writes every key in capitals in §IV.3, so we read the keys exactly as written there. A lower-case file is refused with a message listing the keys it lacks, and the program exits with status 1 — it never crashes."
- **JA** 「subject §IV.3 はキーをすべて大文字で書いているので、その綴りどおりに読んでいます。小文字で書かれたファイルは、足りないキーを示すメッセージで拒否し、終了コード 1 で終わります。クラッシュはしません。」

---

## 5. Error management / エラー処理

**EN** — The sheet edits the configuration to break it, and reminds that an unexpected end of the program means a grade of 0. Every case below prints one line on standard error and exits with status 1 — no traceback.

**JA** — シートは設定ファイルを壊して試し、予期せぬ終了は 0 点だと念を押している。下のどのケースも、標準エラーに 1 行を出して終了コード 1 で終わる。traceback は出ない。

| Sheet case / シートのケース | Change / 変更 | Real output / 実際の出力 |
| --- | --- | --- |
| Remove a mandatory key / 必須キーを消す | no `PERFECT` line | `Error: missing_key.txt: missing required keys: PERFECT` |
| Line without `=` / `=` の無い行 | `HEIGHT 15` | `Error: no_equals.txt:2: expected KEY=VALUE, got 'HEIGHT 15'` |
| Letters for numbers / 数の代わりに文字 | `WIDTH=twenty` | `Error: letters.txt:1: WIDTH must be a whole number, got 'twenty'` |
| Wrong boolean / 間違った真偽値 | `PERFECT=maybe` | `Error: bad_bool.txt:6: PERFECT must be True or False, got 'maybe'` |
| Wrong tuple / 間違った座標 | `ENTRY=0;0` | `Error: bad_tuple1.txt:3: ENTRY must be 'x,y', got '0;0'` |
| | `ENTRY=(0,0)` | `Error: bad_tuple2.txt:3: ENTRY x must be a whole number, got '(0'` |
| | `EXIT=19,14,3` | `Error: bad_tuple3.txt:4: EXIT must be 'x,y', got '19,14,3'` |
| extra: outside the maze / 追加:盤面の外 | `EXIT=20,14` | `Error: exit_outside.txt:4: EXIT x must be less than 20, got 20` |
| extra: negative size / 追加:負の大きさ | `WIDTH=-5` | `Error: neg_width.txt:1: WIDTH must be a positive integer, got '-5'` |
| extra: entry on the "42" / 追加:入口が「42」の上 | `ENTRY=8,7` | `Error: the entry 8,7 is part of the "42", whose cells are closed on every side` |
| extra: too small for loops / 追加:ループの余地が無い | 2x2, `PERFECT=False` | `Error: a maze that is not perfect needs room for two loops: at least 3x2 or 2x3, got 2x2` |
| extra: missing file / 追加:ファイルが無い | `nope.txt` | `Error: Configuration file 'nope.txt' not found.` |

**How it works / 仕組み**

**EN** — `maze/config.py` raises a `ConfigError` subclass with the file name and line; the generator raises `GenerationError` and the solver `SolveError`, both `MazeError`s. `a_maze_ing.py` catches `(ConfigError, MazeError)`, prints `Error: …` to stderr and returns 1. The two families are separate, which is why both are named.

**JA** — `maze/config.py` はファイル名と行番号つきの `ConfigError` の仲間を投げる。生成器は `GenerationError`、ソルバーは `SolveError` を投げ、どちらも `MazeError` の仲間。`a_maze_ing.py` は `(ConfigError, MazeError)` を捕まえ、`Error: …` を標準エラーに出して 1 を返す。2 つの系統は別なので、両方を書いている。

**Careful / 注意**

- **EN** Never set `OUTPUT_FILE` to the configuration file's own name: the first run overwrites the configuration with the maze. **JA** `OUTPUT_FILE` に設定ファイル自身の名前を書かないこと。1 回目の実行で、設定ファイルが迷路の出力で上書きされる。
- **EN** An `OUTPUT_FILE` in a directory that does not exist raises an uncaught `OSError` (traceback). Avoid it in the demo; see §10. **JA** 存在しないフォルダの中の `OUTPUT_FILE` は、捕まえていない `OSError`(traceback)になる。デモでは避ける。§10 参照。

---

## 6. Output file / 出力ファイル

**EN** — The first maze shown is the one stored in `OUTPUT_FILE`. The file is `HEIGHT` lines of `WIDTH` hex digits, an empty line, the entry, the exit and the path, every line ending with `\n`.

**JA** — 最初に表示された迷路が、そのまま `OUTPUT_FILE` に保存されている。ファイルは、`WIDTH` 桁の 16 進数が `HEIGHT` 行、空行、入口、出口、経路の順で、すべての行が `\n` で終わる。

Checked on a 20x15 file / 20x15 のファイルで確認: `grid rows: 15, widths: {20}, blank line: '', entry: 0,0, exit: 19,14, path length: 41, ends with newline: True`.

**Analyzer / analyzer の結果**(`SEED=42`)

```text
PERFECT=False → Wall coherence: OK
                Verdict: Pac-Man-USABLE: fully connected, corners and centre reachable,
                35 independent routes; no real dead-end -> bonus-grade (perfectly braided).
PERFECT=True  → Wall coherence: OK
                Verdict: PERFECT maze: a single path, no loop -> matches PERFECT=True
```

**Path matches the picture / 経路と画面の一致**

**EN** — The letters in the file are exactly `to_directions(shortest_path(...))`, and replaying them from the entry crosses only open walls and ends on the exit (checked). In the demo, press `t` and follow the green `o` marks with the letters: `S` is down, `E` is right.

**JA** — ファイルの文字は `to_directions(shortest_path(...))` そのもので、入口から文字どおりに進むと開いた壁だけを通って出口に着く(確認済み)。デモでは `t` を押し、緑の `o` を文字と見比べる。`S` は下、`E` は右。

**Likely questions / 想定質問**

- *What does one hex digit mean? / 16 進数 1 桁の意味は?* — **EN** Four bits, N=1, E=2, S=4, W=8; a set bit is a closed wall. `b` = 1011 = N, E, W closed. **JA** 4 ビットで N=1、E=2、S=4、W=8。ビットが 1 なら壁が閉じている。`b` = 1011 = 北・東・西が閉じている。
- *How are the two sides of a wall kept equal? / 壁の両側をどう一致させる?* — **EN** `Maze.open_passage` is the only code that opens a wall, and it clears the bit on both cells at once. **JA** 壁を開けるのは `Maze.open_passage` だけで、両方のセルのビットを同時に消す。

---

## 7. Maze generation / 迷路の生成

| Sheet expectation / シートの要求 | Our answer / 私たちの答え | Evidence / 根拠 |
| --- | --- | --- |
| Randomly generated, e.g. `random` / ランダムに生成 | `random.Random(seed)`; no seed → `random.randrange(2**32)` | `maze/generator.py` |
| Inconsistent parameters handled / 矛盾したパラメータへの対処 | entry/exit outside, negative or zero size, entry on the "42", too small for two loops — all refused with a message (§5) / すべてメッセージつきで拒否 | §5 |
| All cells reachable except the "42" / 「42」以外は全セルに到達可能 | spanning tree from `(0, 0)`; a split raises `GenerationError` / (0,0) からの全域木。分断されたら `GenerationError` | analyzer: `fully connected` |
| Walls all around / 外周は壁 | walls start closed and only `open_passage` between two cells in the grid opens one / 壁は閉じた状態から始まり、盤面の中の 2 セルの間しか開かない | **300 generated mazes: 0 border openings** |
| No 3x3 open zone / 3x3 の開けた場所なし | checked **before** each wall is opened (below) / 壁を開ける前に毎回確認 | **300 mazes: 0 open 3x3 areas**; tests |
| "42" present, message if too small / 「42」、小さければメッセージ | 7x5 block, centred, from 9x7 up; below: `Warning: The '42' pattern was omitted because the maze size is too small.` | analyzer counts 2 dead ends "enclosed by the '42'" |
| `PERFECT=True` → perfect / 完全迷路 | stop after the spanning tree / 全域木で止める | analyzer: `PERFECT maze` |
| `PERFECT=False` → Pac-Man board / 遊べる盤面 | braiding + loop top-up; corners and centre open / braiding とループの補充。四隅と中央は空く | analyzer: `Pac-Man-USABLE` |
| Same seed → same maze / 同じシードで同じ迷路 | set `SEED=42`, run twice / 2 回実行 | **output files identical** / 出力ファイルが一致 |

### How the 3x3 rule is implemented / 3x3 の規則の実装(シートが「聞け」と指示している)

**EN** — A spanning tree cannot contain even a 2x2 open block (four cells joined in a ring would be a loop), so only braiding can create a 3x3 area. Before braiding opens the wall between `a` and `b`, `_completes_open_3x3` looks at the only 3x3 blocks that change — the ones containing both cells, six of them whichever way the wall runs. The wall is closed and inside each of them, so a block completes exactly when it has one closed internal wall left; `_closed_walls_in` counts the twelve internal walls. If any block would complete, that wall is not a candidate. The cost is fixed (6 blocks × 12 walls) on any maze size. Tests check the last wall, horizontal and vertical, two closed walls, and a generated maze with no open 3x3.

**JA** — 全域木には 2x2 の開けた場所すら無い(4 セルが輪になるとループになるから)。なので 3x3 を作りうるのは braiding だけ。braiding が `a` と `b` の間の壁を開ける前に、`_completes_open_3x3` が、変わりうる 3x3 ブロックだけを見る。両方のセルを含むブロックで、壁の向きに関係なく 6 つ。その壁はどのブロックでも内側にあって閉じているので、閉じた内側の壁が 1 枚だけ残っているブロックがあれば、開けると完成する。`_closed_walls_in` が内側の壁 12 枚を数える。完成するなら、その壁は候補から外す。手間は迷路の大きさに関係なく一定(6 ブロック × 12 枚)。テストは、最後の 1 枚(横・縦)、閉じた壁 2 枚、生成した迷路に 3x3 が無いことを確かめている。

### Show / 見せ方

```bash
# PERFECT=True and PERFECT=False with SEED=42, then / 両モードで生成してから
python3 maze_analyzer.py maze.txt
# reproducibility: run twice with SEED=42 and compare / 再現性:2 回実行して比べる
cp maze.txt first.txt && python3 a_maze_ing.py config.txt   # then q
cmp maze.txt first.txt && echo same
```

**Likely questions / 想定質問**

- *Which algorithm and why? / どのアルゴリズムで、なぜ?* — **EN** The recursive backtracker, written with an explicit stack. It starts with the fewest dead ends (long corridors), so braiding has least to undo; the stack removes the recursion limit (about 1000 calls). **JA** 再帰的バックトラッカーを明示的なスタックで書いた。通路が長く、行き止まりが最も少ない状態から始まるので、braiding の手間が少ない。スタックで書けば再帰の上限(約 1000)が無い。
- *How do you count loops? / ループをどう数える?* — **EN** Independent loops = E − V + 1. A tree has V − 1 passages, so every wall braiding opens adds exactly one loop, and the number of walls opened is the loop count. **JA** 独立なループの数は E − V + 1。木の通路は V − 1 本なので、braiding が壁を 1 枚開けるたびにループがちょうど 1 本増え、開けた枚数がループの数になる。
- *Why can braiding stop after one pass? / なぜ 1 周で足りる?* — **EN** Opening a wall only adds passages, so it never creates a dead end; each cell is recounted on its turn because one wall can fix two neighbouring dead ends. **JA** 壁を開けても通路が増えるだけなので、行き止まりは生まれない。隣り合う 2 つの行き止まりが 1 枚で直ることがあるので、各セルで通路を数え直す。
- *What if braiding leaves one loop? / braiding でループが 1 本しかできなかったら?* — **EN** On 3x2 or 2x3 it can; `_add_loops` opens the missing walls one at a time. **JA** 3x2 や 2x3 では起きうる。`_add_loops` が足りない壁を 1 枚ずつ開ける。
- *Why is the "42" always safe? / 「42」が安全な理由は?* — **EN** Its open column lands on `width // 2` and its third row on `height // 2`, so a centre cell stays free; from 9x7 a margin of one cell keeps the corners free and every open cell connected (checked on every size up to 60x60). **JA** 空き列が `width // 2`、3 行目が `height // 2` に重なるので中央のセルが空く。9x7 以上なら 1 セルの余白で四隅が空き、空いたセルはすべてつながる(60x60 まで全サイズで確認)。

---

## 8. Reusable module / 再利用モジュール

**EN** — The evaluator rebuilds the package in one virtual environment, installs it in another, and tests it with `a_maze_ing.py`. `make build` (`poetry build --output .`) recreates both files; a build into a scratch directory on 2026-09-22 produced `mazegen-0.1.0-py3-none-any.whl` and `mazegen-0.1.0.tar.gz`.

**JA** — 評価者は、ある仮想環境でパッケージを作り直し、別の仮想環境にインストールして、`a_maze_ing.py` で試す。`make build`(`poetry build --output .`)で両方のファイルが作り直される。2026-09-22 に作業用フォルダへビルドし、2 つのファイルができることを確かめた。

### Commands / コマンド(so runs them — Claude does not create environments / 実行するのは so)

```bash
# 1. rebuild in a fresh environment / 新しい環境で作り直す
python3 -m venv /tmp/build-env && . /tmp/build-env/bin/activate
pip install poetry
poetry build --output .
deactivate

# 2. install in another environment and test / 別の環境にインストールして試す
python3 -m venv /tmp/test-env && . /tmp/test-env/bin/activate
pip install ./mazegen-0.1.0-py3-none-any.whl
python3 -c "from mazegen import MazeGenerator, shortest_path, to_directions; \
m = MazeGenerator(20, 15, seed=42).generate(); \
print(to_directions(shortest_path(m, (0, 0), (19, 14))))"
python3 a_maze_ing.py config.txt          # from the repository root / リポジトリの直下で
```

### What to say about `a_maze_ing.py` / `a_maze_ing.py` について説明すること

**EN** — The wheel contains the reusable part only: `mazegen` (the entry point of the package) and `maze` (generator, solver, maze structure, config parser). The display and the output writer are part of the application, not of the reusable module §VI asks for, so they stay in the repository. `a_maze_ing.py` therefore runs from the repository root, where `display/` and `output/` are next to it. Tested: with only the wheel on the path and outside the repository, `mazegen` works (41 steps on 20x15, seed 42) and `a_maze_ing.py` stops with `ModuleNotFoundError: No module named 'display'`.

**JA** — wheel に入っているのは再利用される部分だけ:`mazegen`(パッケージの入口)と `maze`(生成器、ソルバー、迷路の構造、設定パーサ)。表示と出力はアプリの一部で、§VI が求める再利用モジュールではないので、リポジトリに残している。そのため `a_maze_ing.py` は、`display/` と `output/` が隣にあるリポジトリの直下で実行する。確認済み:wheel だけを置いてリポジトリの外で動かすと、`mazegen` は動く(20x15、シード 42 で 41 歩)が、`a_maze_ing.py` は `ModuleNotFoundError: No module named 'display'` で止まる。

**Likely questions / 想定質問**

- *What is a wheel? / wheel とは?* — **EN** A zip file in a form pip can install directly; the name says package, version, Python 3, no C code, any platform. **JA** pip がそのままインストールできる形の zip ファイル。名前はパッケージ名・版・Python 3・C の部品なし・どの OS でも、を表す。
- *Why is `MazeGenerator` in `maze/` and not `mazegen/`? / なぜ `maze/` にある?* — **EN** It sits next to the `Maze` it builds; `mazegen/__init__.py` re-exports it, and `pyproject.toml` packages both. **JA** 自分が作る `Maze` の隣に置いた。`mazegen/__init__.py` が再公開し、`pyproject.toml` が両方を入れる。
- *How do I access a solution? / 解へのアクセスは?* — `shortest_path(maze, entry, exit)` → cells; `to_directions(cells)` → `N/E/S/W`.

---

## 9. Bonuses / ボーナス

| Idea on the sheet / シートの案 | Status / 状態 | Evidence / 根拠 |
| --- | --- | --- |
| No dead end at all / 行き止まり 0 | **Done / 達成** | `python3 maze_analyzer.py maze.txt --max-dead-ends 0` → `Pac-Man-USABLE … no real dead-end -> bonus-grade (perfectly braided)` |
| Several algorithms / 複数のアルゴリズム | not done / 未実装 | — |
| Animation / アニメーション | not done / 未実装 | — |

**EN** — The two dead ends the analyzer lists as "enclosed by the '42'" are the notches of the "2": three sides are the pattern, so no wall can open them, and the analyzer does not count them.

**JA** — analyzer が「enclosed by the '42'」と示す 2 つは、「2」の 2 つのくぼみ。3 方向が「42」なので開けられる壁が無く、analyzer は数えない。

---

## 10. Risks before the defense / 評価前のリスク

| # | Risk / リスク | Owner / 担当 | Options / 選択肢 |
| --- | --- | --- | --- |
| R1 | ~~Lower-case keys~~ — **settled 2026-09-22**: the subject writes keys in capitals and the sheet's note is a tolerance for the team's own file; keys stay case-sensitive, answer in §4 / **決定済み**:subject はキーを大文字で書き、シートの注記はチームの設定ファイルへの許容。区別したままにし、答えは §4 | so | — |
| R2 | ~~"positive integer" for WIDTH/HEIGHT~~ — **done 2026-09-22**: `_as_int` says `must be a positive integer` when the minimum is 1 / **対応済み**:最小値 1 のとき `must be a positive integer` と表示 | so | — |
| R3 | Unwritable `OUTPUT_FILE` → uncaught `OSError` / 書けない `OUTPUT_FILE` で traceback | javi (`a_maze_ing.py`) | catch `OSError` around the write / 書き出しの周りで `OSError` を捕まえる |
| R4 | Ctrl-D / Ctrl-C at the menu → traceback / メニューで Ctrl-D・Ctrl-C | javi (`display/input_handler.py`) | catch `EOFError` / `KeyboardInterrupt` and quit cleanly / 捕まえて静かに終わる |
| R5 | The committed wheel's `mazegen/__init__.py` lacks the final newline of the source / コミット済み wheel が 1 文字古い | javi | `make build` after any change, before the defense / 変更後・評価前に作り直す |
| R6 | 3 local commits not pushed yet / 未 push の 3 コミット | so | `git push origin main` |

**EN** — None of the open risks fails a mandatory item as long as the demo avoids them. R3 and R4 matter most, because "unexpected end of the program" means 0: avoid an unwritable output path and Ctrl-D / Ctrl-C at the menu, even if they stay unfixed.

**JA** — デモで避ければ、残っているリスクで必須項目が不合格になるものは無い。最も大事なのは R3 と R4。「予期せぬ終了は 0 点」に関わるので、直さない場合でも、書けない出力先と、メニューでの Ctrl-D・Ctrl-C はデモで避ける。

---

## Related / 関連

- `Docs/code_guide/` — the Japanese guide to every module / 全モジュールの解説(日本語)
- `Docs/implementation_plans/generation-algorithm.md`, `shortest-path-solver.md`, `config-parser.md`
- `Docs/pair_communication/01_kickoff.md` — numbered decisions / 番号付きの決定
