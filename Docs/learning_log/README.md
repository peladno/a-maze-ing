# learning_log/

---

## English

### Purpose

**One concept, one file.** A note where you rebuild a concept **in your own words**, from your own understanding.

> **The core rule: do not paste references.**
> Copying a Stack Overflow answer or a documentation page into a file feels like learning and is not. If you can
> only reproduce the source, you have stored it, not learned it. Read the source, close the tab, then write.
> What you can still write with the tab closed is what you actually know — and the gap you discover while writing
> is exactly the thing the evaluator will ask about.

Links to sources still belong in the file — in the **Sources** section at the bottom, as pointers, never as the body.

### Why we write it

- **Review** — a concept written once in your own words is re-readable in 2 minutes six months later.
  The original article is not; you would have to read all of it again.
- **Continuity** — you will meet these concepts again (graphs in `push_swap`-adjacent projects, bitmasks in C
  projects, packaging in every Python project after this one). This is the note your future self greps.
- **Defense material** — this is the single most direct one. At the peer evaluation you must explain the concepts
  behind the code, out loud, in your own words. This folder is literally rehearsal for that.
- **Early sharing** — the English summary at the top lets Javier check your understanding, which is the cheapest
  possible way to catch a misunderstanding before it becomes an implementation.

### Naming

`topic-name.md`, kebab-case, one concept — e.g. `perfect-maze-and-spanning-tree.md`.

If the file needs the word "and" twice, it is two concepts. Split it.

### Language

Unlike the other folders, the detailed explanation here is written **in Japanese**: this is So's own thinking, and
forcing it into a second language costs precision. To keep the file readable for Javier, every file starts with a
**short English summary (3–6 lines)**. The template enforces this.

### How to use

1. Copy `TEMPLATE.md`, name it after the concept.
2. Read your sources. **Close them.** Then write the explanation.
3. Include a **concrete example with real values** — a trace beats a definition every time.
4. Fill "What I still do not understand". Being explicit about the edge of your knowledge is a skill, not a weakness.
5. Commit: `docs(learn): note on <topic>`.

### Relation to `implementation_plans/`

`learning_log/` is **investigation and comparison** — what exists, how it works, what the trade-offs are.
`implementation_plans/` is the **contract for the design we adopted**. See the comparison table in
[`../implementation_plans/README.md`](../implementation_plans/README.md).

### Good first topics for this project

1. `bitmask-wall-encoding.md` — bit 0=N, 1=E, 2=S, 3=W (subject IV.5); `&`, `|`, `^`, `<<`, and why a bitmask
   instead of four booleans.
2. `perfect-maze-and-spanning-tree.md` — why "exactly one path between any two cells" is the definition of a tree,
   and what that implies for `PERFECT=True`.
3. `dfs-vs-bfs.md` — why DFS carves a maze while BFS finds the shortest path; queue vs stack; when each terminates.
4. `random-seed-and-reproducibility.md` — `random.Random(seed)` vs the global `random`, and why reproducibility is
   a testability requirement, not a feature.
5. `type-hints-and-mypy.md` — what `mypy --disallow-untyped-defs` actually checks, and what type hints do **not**
   do at runtime.
6. `python-packaging-wheel-vs-sdist.md` — `.whl` vs `.tar.gz`, what `pip install` does with each, needed for the
   `mazegen-*` deliverable.

---

## 日本語

### 目的

**1 概念 1 ファイル。** その概念を、**自分の言葉で・自分の理解から**組み立て直すノート。

> **中核ルール:参考資料を貼らない。**
> Stack Overflow の回答や公式ドキュメントをファイルに貼り付ける行為は、学んだ気分になるだけで学習ではない。
> 出典を再現できるだけなら、それは「保存した」のであって「学んだ」のではない。
> 資料を読む → **タブを閉じる** → 書く。タブを閉じたまま書けた分だけが本当に知っていること。
> そして書きながら見つかる穴こそ、評価者が突いてくる場所。

出典へのリンクはファイルに残してよい。ただし末尾の **Sources** 欄にポインタとして置く。本文にはしない。

### なぜ書くのか

- **振り返り** — 自分の言葉で一度書いた概念は、半年後に 2 分で読み直せる。元記事はそうはいかない(全部読み直しになる)。
- **継続性** — これらの概念には必ず再会する(グラフ、ビット演算は C 課題で、パッケージングは今後の Python 全部で)。
  将来の自分が grep するのはこのノート。
- **ディフェンス材料** — 最も直接的。ピア評価では、コードの背後にある概念を**声に出して自分の言葉で**説明する。
  このフォルダは文字どおりその予行演習。
- **早期共有** — 冒頭の英語サマリーがあれば Javier が理解をチェックできる。
  誤解が実装になる前に潰す、最も安い方法。

### 命名

`topic-name.md`、kebab-case、1 概念 — 例:`perfect-maze-and-spanning-tree.md`。

「and」が 2 回必要になったら、それは 2 概念。分割する。

### 言語について

他のフォルダと違い、ここの詳細説明は**日本語で書く**。So 自身の思考の記録であり、
第二言語に押し込めると精度が落ちるため。ただし Javier も読めるよう、
各ファイルの冒頭に**短い英語サマリー(3〜6 行)**を必ず置く。テンプレートがそれを強制する。

### 使い方

1. `TEMPLATE.md` をコピーし、概念名を付ける。
2. 資料を読む。**閉じる。** それから説明を書く。
3. **実際の値を使った具体例**を必ず入れる。定義より 1 回のトレース。
4. 「まだ分かっていないこと」欄を埋める。知識の境界を明示できるのは弱点ではなく技能。
5. コミット:`docs(learn): note on <topic>`。

### `implementation_plans/` との関係

`learning_log/` は**調査と比較**(何が存在し、どう動き、トレードオフは何か)。
`implementation_plans/` は**採用した設計の契約**。対比表は
[`../implementation_plans/README.md`](../implementation_plans/README.md) にある。

### この課題で最初に書くと良いトピック

1. `bitmask-wall-encoding.md` — bit 0=N, 1=E, 2=S, 3=W(subject IV.5)。`&` `|` `^` `<<` と、
   なぜ bool 4 個ではなくビットマスクなのか。
2. `perfect-maze-and-spanning-tree.md` — 「任意の 2 セル間の経路がちょうど 1 本」が木の定義そのものである理由と、
   それが `PERFECT=True` に何を意味するか。
3. `dfs-vs-bfs.md` — なぜ DFS は迷路を掘り、BFS は最短経路を出すのか。スタックとキュー。それぞれの停止条件。
4. `random-seed-and-reproducibility.md` — `random.Random(seed)` とグローバル `random` の違い。
   再現性が「機能」ではなく「テスト可能性の要件」である理由。
5. `type-hints-and-mypy.md` — `mypy --disallow-untyped-defs` が実際に何を検査するか。
   そして型ヒントが実行時には**何もしない**こと。
6. `python-packaging-wheel-vs-sdist.md` — `.whl` と `.tar.gz` の違い、`pip install` がそれぞれに何をするか。
   `mazegen-*` 提出物に直結する。
