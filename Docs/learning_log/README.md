# learning_log/

---

## English

### Purpose

**One concept, one file.** A **reference manual written for your future self**: a document you can come back to at
any time and rebuild your understanding from in a few minutes, **without re-reading the original sources**.

That last clause is the whole design goal. The test of a file in this folder is not "did I write it myself" but:

> **Six months from now, does reading this for five minutes put the concept back in my head?**

If yes, the file works. If it only makes sense while you still remember the topic, it does not.

### What that implies

Being revisitable is a property you have to build in deliberately:

1. **Enter from the top.** One sentence saying what the thing is, before any detail. That sentence is what you
   read first every time you come back.
2. **A worked example with real values.** A trace you can follow by hand reloads a concept faster than any
   definition. This is the single highest-value section.
3. **A diagram wherever the shape matters.** ASCII when the layout must be exact (grids, mazes, tables of bits);
   mermaid when it is a flow or a relationship.
4. **The traps you already hit.** A "common misconceptions" section is the part that saves future-you from
   repeating a debugging session.
5. **Where it is used in *this* project**, with the subject's section number. That is what makes the file ours
   rather than a generic tutorial.
6. **Self-check questions.** They are how you find out whether the document actually worked on you.

### The one rule that stays: sources are pointers, not bodies

Do not paste articles or documentation into the file. Not for moral reasons — for a practical one:
**a pasted article is exactly the thing you were trying to avoid re-reading.** If the file becomes as long as its
sources, it has stopped being a reference and gone back to being the source. Links belong in the **Sources**
section at the bottom.

### Writing it with AI is fine

These are explanatory documents, so drafting one with Claude is a normal way to produce it. Two conditions:

- **Log it.** §VII requires us to state which tasks and which parts of the project used AI. A file drafted with
  AI records that at the top.
- **Answer the self-check before you rely on it.** A document you cannot yet explain out loud is a document you
  have read, not one you have understood — and §IX asks for the second one.

### Why this folder exists

- **Review** — a concept written once, structured for re-entry, is re-loadable in minutes. The original article
  is not; you would have to read all of it again.
- **Continuity** — these concepts recur (graphs and bit operations in later projects, packaging in every Python
  project after this one). This is the note future-you greps.
- **Defense material** — at the peer evaluation you explain the concepts behind the code out loud. This folder is
  the study material for that, and the self-check questions are the rehearsal.
- **Early sharing** — because the file is fully bilingual, either of us can check the other's understanding of
  their own work area, which is the cheapest way to catch a misunderstanding before it becomes an implementation.

### Naming

`topic-name.md`, kebab-case — e.g. `maze-generation-algorithms.md`.

One concept per file, or one tight family of concepts that are only understandable together (three algorithms
solving the same problem belong in one file; three unrelated topics do not).

### Language: fully bilingual, one file

Both of us have to understand **each other's** work area — so takes W01–W12, javi takes W13–W17 and W20–W24, and
§IX asks each of us to explain and modify any part of it. A document only one of us can read cannot do that job.

So a file here is **fully bilingual in a single file**, not "English summary plus Japanese detail":

- **Section by section, English first, then Japanese** (`**EN** —` / `**JA** —`), the same rhythm as
  `pair_communication/01_kickoff.md`.
- **Figures, traces, ASCII diagrams and tables appear once**, shared between the two languages, with their labels
  in English. Duplicating a diagram means one copy eventually drifts from the other.
- Table headers are bilingual (`Choice / 選択`).

Two languages in one file, rather than two files, for the same reason: two files drift apart the first time only
one of them is corrected.

### Relation to `implementation_plans/`

`learning_log/` is **investigation and comparison** — what exists, how it works, what the trade-offs are.
`implementation_plans/` is the **contract for the design we adopted**. See the comparison table in
[`../implementation_plans/README.md`](../implementation_plans/README.md).

### Topics for this project

1. `maze-generation-algorithms.md` — **written**: grid graph and spanning tree, recursive backtracker, Prim,
   Kruskal, and how each scores against our constraints. Feeds decision 3.5.
2. `bitmask-wall-encoding.md` — bit 0=N, 1=E, 2=S, 3=W (§IV.5); `&`, `|`, `^`, `<<`, and why a bitmask instead of
   four booleans.
3. `bfs-and-shortest-path.md` — why breadth-first search is *provably* shortest and depth-first is not; needed for
   the `NESW` path in §IV.5.
4. `union-find.md` — only if we adopt Kruskal, or if we use it to count independent loops for `PERFECT=False`.
5. `random-seed-and-reproducibility.md` — `random.Random(seed)` vs the global `random`, and why reproducibility is
   a testability requirement rather than a feature.
6. `python-packaging-wheel-vs-sdist.md` — `.whl` vs `.tar.gz` and what `pip install` does with each, needed for
   the `mazegen-*` deliverable (§VI).

---

## 日本語

### 目的

**1 概念 1 ファイル。** **将来の自分のために書く解説書**。いつでも戻ってきて、
**出典を読み直さずに**数分で理解を組み直せる文書。

この「出典を読み直さずに」が設計目標のすべて。このフォルダのファイルの合否は
「自分で書いたかどうか」ではなく:

> **半年後、これを 5 分読んだら概念が頭に戻るか。**

戻るなら成功。まだ覚えているうちしか意味が通らないなら失敗。

### そこから導かれること

「戻れること」は意識して作り込まないと手に入らない性質:

1. **上から入れるようにする。** 詳細の前に「これは何か」を一文で。
   戻ってくるたび、最初に読むのはその一文になる。
2. **実際の値で追える例を置く。** 手で追えるトレースは、どんな定義よりも速く概念を再ロードする。
   **最も価値の高いセクションはここ。**
3. **形が意味を持つところには図を置く。** レイアウトが正確でなければならないもの(格子、迷路、ビットの並び)は
   ASCII、流れや関係は mermaid。
4. **自分がハマった罠を残す。**「よくある誤解」の節は、将来の自分が同じデバッグを繰り返すのを防ぐ部分。
5. **この課題のどこで使うか**を、subject の節番号付きで書く。
   これがあるかどうかで、一般的なチュートリアルではなく「自分たちの文書」になる。
6. **確認問題を置く。** その文書が自分に効いたかどうかを知る手段はこれしかない。

### 唯一残すルール:出典はポインタであって本文ではない

記事やドキュメントをファイルに貼り付けない。道徳的な理由ではなく実務的な理由:
**貼り付けた記事は、まさに「読み直したくなかったもの」そのものだから。**
ファイルが出典と同じ長さになった時点で、それは解説書ではなく出典に戻っている。
リンクは末尾の **Sources** に置く。

### AI と一緒に書いてよい

これは解説文書なので、Claude と一緒に草稿を作るのは普通の作り方。条件は 2 つ:

- **記録する。** §VII は「どのタスクの、どの部分に AI を使ったか」の記述を要求している。
  AI と作ったファイルは冒頭にそれを書く。
- **頼る前に確認問題に答える。** 声に出して説明できない文書は「読んだ」文書であって「理解した」文書ではない。
  §IX が求めているのは後者。

### なぜこのフォルダがあるのか

- **振り返り** — 再入場を前提に構成された解説は、数分で再ロードできる。元記事はそうはいかない(全部読み直しになる)。
- **継続性** — これらの概念には再会する(グラフとビット演算は後の課題で、パッケージングは今後の Python 全部で)。
  将来の自分が grep するのはこのノート。
- **ディフェンス材料** — ピア評価では、コードの背後にある概念を声に出して説明する。
  このフォルダがその教材であり、確認問題がその予行演習。
- **早期共有** — 完全バイリンガルなので、お互いの担当範囲について相手の理解をチェックできる。
  誤解が実装になる前に潰す最も安い方法。

### 命名

`topic-name.md`、kebab-case — 例:`maze-generation-algorithms.md`。

1 ファイル 1 概念。ただし「一緒でないと理解できない概念の束」は 1 つとして数える
(同じ問題を解く 3 つのアルゴリズムは 1 ファイル、無関係な 3 トピックは別ファイル)。

### 言語:完全バイリンガル、1 ファイル

二人は**お互いの担当範囲**を理解する必要がある。so が W01〜W12、javi が W13〜W17 と W20〜W24 を持ち、
§IX はどちらにも「どの部分でも説明し修正できること」を要求している。
片方しか読めない文書では、この役目を果たせない。

したがってここのファイルは、「英語サマリー + 日本語詳細」ではなく **1 ファイル内で完全バイリンガル**にする:

- **章ごとに英語 → 日本語の順**(`**EN** —` / `**JA** —`)。
  `pair_communication/01_kickoff.md` と同じリズム。
- **図・トレース・ASCII・表は 1 回だけ置き**、両言語で共有する。ラベルは英語。
  図を二重に持つと、いずれ片方だけが直されてずれる。
- 表の見出しはバイリンガル(`Choice / 選択`)にする。

2 ファイルに分けず 1 ファイルにするのも同じ理由。分けると、片方だけ修正された瞬間にずれ始める。

### `implementation_plans/` との関係

`learning_log/` は**調査と比較**(何が存在し、どう動き、トレードオフは何か)。
`implementation_plans/` は**採用した設計の契約**。対比表は
[`../implementation_plans/README.md`](../implementation_plans/README.md) にある。

### この課題のトピック

1. `maze-generation-algorithms.md` — **作成済み**:格子グラフと全域木、再帰的バックトラッカー、Prim、Kruskal、
   および各案が制約に対してどうか。決定 3.5 の材料。
2. `bitmask-wall-encoding.md` — bit0=N, 1=E, 2=S, 3=W(§IV.5)。`&` `|` `^` `<<` と、
   なぜ bool 4 個ではなくビットマスクなのか。
3. `bfs-and-shortest-path.md` — 幅優先探索がなぜ*証明として*最短で、深さ優先はなぜ違うのか。
   §IV.5 の `NESW` 経路に必要。
4. `union-find.md` — Kruskal を採用する場合、または `PERFECT=False` の独立ループ数を数えるのに使う場合。
5. `random-seed-and-reproducibility.md` — `random.Random(seed)` とグローバル `random` の違い。
   再現性が「機能」ではなく「テスト可能性の要件」である理由。
6. `python-packaging-wheel-vs-sdist.md` — `.whl` と `.tar.gz`、`pip install` がそれぞれに何をするか。
   `mazegen-*` 提出物(§VI)に直結する。
