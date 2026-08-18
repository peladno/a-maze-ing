# implementation_plans/

---

## English

### Purpose

**One design, one file.** The plan for something we are about to build: its scope, its interface, the steps, the
edge cases, the complexity and why it is acceptable, and how we will test it.

A plan is written **before** the code, and it is a **design-level** document:

> **Signatures, not bodies.** The Interface section contains Python signatures with type hints, class definitions
> and the exceptions raised — never a function body. If a plan contains an implementation, the plan has stopped
> being a plan and the review has become a code review of code nobody has run.

### Why we write it

- **Review** — the subject's README must state the algorithm we chose **and why**. That justification is written
  here, at the moment we still remember the alternatives.
- **Continuity** — a plan is what lets the other person implement, or take over, without a meeting.
- **Defense material** — the evaluator asks "why this data structure?", "what is the complexity?",
  "what happens if the entry equals the exit?". Those are literally the sections of this template.
- **Early sharing** — reviewing a one-page interface costs ten minutes; reviewing 300 lines of finished code costs
  an afternoon and ends in an argument. Agree on the signature before either of us writes the body.

### `learning_log/` vs `implementation_plans/`

The two folders are easy to confuse. The difference is **investigation vs contract**:

| | `learning_log/` | `implementation_plans/` |
| --- | --- | --- |
| **Question it answers** | "How does this work? What are my options?" | "What exactly are we building, and how?" |
| **Nature** | Investigation, comparison, understanding | The contract for the design we **adopted** |
| **Audience** | Both of us — each has to understand the other's work area | Both of us — the other side depends on it |
| **Timing** | Whenever you meet a concept | Before writing the code it describes |
| **Contains alternatives?** | Yes — comparing them is the point | Only as "rejected, because …" |
| **Binding?** | No. It is a note; being wrong is allowed | Yes. Changing it means telling the pair |
| **Code inside?** | Snippets to illustrate a concept are fine | Signatures and types only, **never bodies** |
| **Language** | Fully bilingual, section by section | Body in English (shared contract) |
| **Example** | `dfs-vs-bfs.md` — how both traversals work | `shortest-path-solver.md` — we use BFS, here is the API |
| **When it is wrong** | Fix the note, no one else affected | Update it **and** tell the other person: they may already be coding against it |

Rule of thumb: **`learning_log/` answers "why is this true?", `implementation_plans/` answers "what did we commit to?"**
A concept study that ends with "so we should do X" is a signal to open a plan file — it is not the plan itself.

### Naming

`topic-name.md`, kebab-case — e.g. `config-parser.md`, `hex-output-format.md`.

The two existing files (`A-Maze-ing_Project_Structure_and_Team_Division.md` and its Japanese version) predate this
convention; they are Javier's initial proposal for the project structure and the split, kept as-is for reference.

### How to use

1. Copy `TEMPLATE.md` **before** writing the code it covers.
2. Fill Scope and Interface first, then have the other person review it. Only then implement.
3. If the design changes during implementation, **update the plan in the same commit as the code**. A plan that
   disagrees with the code is worse than no plan — it will be quoted at you during the defense.
4. Commit: `docs(plan): design for <topic>`.

### Good first plans for this project

1. `config-parser.md` — `KEY=VALUE` per line, `#` comments, the six mandatory keys, and every invalid-input case
   (subject IV.3, and IV.2 "must never crash unexpectedly").
2. `maze-data-structure.md` — the in-memory representation both sides depend on. Write this one **first**, together.
3. `wall-encoding-and-output-format.md` — the hex digit per cell, N/E/S/W bit order, neighbour coherence, the entry/
   exit/path block, `\n` on every line (subject IV.5).
4. `generation-algorithm.md` — the algorithm, `PERFECT=True` vs the playable board, the corridor-width ≤ 2 rule,
   the no-3x3-open-area rule, and the seed.
5. `shortest-path-solver.md` — BFS or otherwise, the `N`/`E`/`S`/`W` output string, and the no-path case.
6. `mazegen-package-api.md` — the public surface of the reusable `MazeGenerator` class and how the `mazegen-*`
   artifact is built (subject VI).

---

## 日本語

### 目的

**1 設計 1 ファイル。** これから作るものの計画:Scope、Interface、実装手順、エッジケース、
計算量とそれが許容できる根拠、テスト方針。

計画はコードの**前**に書き、あくまで**設計レベル**の文書:

> **書くのはシグネチャであって本体ではない。** Interface セクションには型ヒント付きの Python シグネチャ、
> クラス定義、送出する例外を書く。**関数の本体は書かない**。
> 計画に実装が入った時点で、それは計画ではなくなり、レビューは「誰も動かしていないコードのコードレビュー」になる。

### なぜ書くのか

- **振り返り** — subject の README には、選んだアルゴリズムと**その理由**を書く義務がある。
  その理由は、まだ他の選択肢を覚えているこの瞬間にしか正確に書けない。
- **継続性** — 計画があれば、相方はミーティングなしで実装を進められる/引き継げる。
- **ディフェンス材料** — 評価者は「なぜこのデータ構造か」「計算量は」「entry と exit が同じだったら」を聞く。
  それはこのテンプレートのセクションそのもの。
- **早期共有** — 1 ページのインターフェースをレビューするのは 10 分。完成した 300 行をレビューするのは半日、
  しかも揉める。本体を書く前にシグネチャで合意する。

### `learning_log/` と `implementation_plans/` の違い

この 2 つは混同しやすい。違いは**調査 vs 契約**:

| | `learning_log/` | `implementation_plans/` |
| --- | --- | --- |
| **答える問い** | 「これはどう動く? どんな選択肢がある?」 | 「結局、何をどう作るのか?」 |
| **性質** | 調査・比較・理解 | **採用した**設計の契約 |
| **読者** | 二人。お互いの担当範囲を理解する必要がある | 二人。相方がこれに依存して実装する |
| **書く時期** | 概念に出会ったとき | それが記述するコードを書く前 |
| **選択肢を書くか** | 書く。比較こそが目的 | 「却下、理由は〜」としてのみ |
| **拘束力** | なし。ノートなので間違っていてよい | あり。変更したら相方に伝える義務がある |
| **コードを含むか** | 概念説明のための断片なら可 | シグネチャと型のみ。**本体は書かない** |
| **言語** | 章ごとに完全バイリンガル | 本文は英語(共有の契約なので) |
| **例** | `dfs-vs-bfs.md` — 2 つの探索がどう動くか | `shortest-path-solver.md` — BFS を採用、API はこれ |
| **間違っていたとき** | ノートを直すだけ。他に影響なし | 直した上で**相方に伝える**。既にそれ前提で書いているかもしれない |

目安:**`learning_log/` は「なぜそれが正しいのか」に答え、`implementation_plans/` は「何に合意したか」に答える。**
概念の調査が「だから X にすべき」で終わったら、それは計画ファイルを開く合図。調査ノート自体は計画ではない。

### 命名

`topic-name.md`、kebab-case — 例:`config-parser.md`、`hex-output-format.md`。

既存の 2 ファイル(`A-Maze-ing_Project_Structure_and_Team_Division.md` とその日本語版)はこの規約より前のもの。
Javier によるプロジェクト構成と分担の初期提案として、そのまま参照用に残してある。

### 使い方

1. 対象のコードを書く**前**に `TEMPLATE.md` をコピーする。
2. まず Scope と Interface を埋め、相方にレビューしてもらう。実装はその後。
3. 実装中に設計が変わったら、**コードと同じコミットで計画も更新する**。
   コードと食い違った計画は、計画がないより悪い(ディフェンスでそこを引用される)。
4. コミット:`docs(plan): design for <topic>`。

### この課題で最初に書くと良い計画

1. `config-parser.md` — 1 行 1 つの `KEY=VALUE`、`#` コメント、必須 6 キー、そして不正入力の全ケース
   (subject IV.3 と、IV.2 の「予期せぬクラッシュは絶対にしない」)。
2. `maze-data-structure.md` — 両側が依存するメモリ上の表現。これを**最初に、二人で**書く。
3. `wall-encoding-and-output-format.md` — 1 セル 1 桁の 16 進、N/E/S/W のビット順、隣接整合、
   entry/exit/path ブロック、全行末の `\n`(subject IV.5)。
4. `generation-algorithm.md` — アルゴリズム本体、`PERFECT=True` と遊べる盤面の違い、通路幅 ≤ 2 の制約、
   3x3 の開放領域禁止、シード。
5. `shortest-path-solver.md` — BFS などの選択、`N`/`E`/`S`/`W` 出力文字列、経路なしの場合。
6. `mazegen-package-api.md` — 再利用可能な `MazeGenerator` クラスの公開 API と、`mazegen-*` 成果物のビルド方法
   (subject VI)。
