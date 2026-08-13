# Docs — A-Maze-ing

*Project: A-Maze-ing (42 Tokyo, Python 3.10+) — skusakab (So) & jperez-u (Javier) — started 2026-08-13*

---

## English

### Why this folder exists

The code shows **what** we built. This folder records **why** we built it that way, **when** we decided it,
and **what each of us understood**. It exists for four reasons:

1. **Review (振り返り)** — we can look back at a decision weeks later and remember the reasoning, not just the result.
2. **Continuity** — if one of us is away for three days, the other can read the logs and continue without a meeting.
3. **Defense material** — at peer-evaluation both of us must explain *any* part of the project, including parts we
   did not write ourselves. These documents are the study material for that.
4. **Early sharing with the pair** — a design written down before coding gets reviewed before the code exists,
   which is far cheaper than reviewing it afterwards.

> The subject states explicitly that a small modification may be requested during evaluation, and that **both**
> students must be able to understand and modify the implementation. Writing here is not overhead — it is part of
> passing the defense.

### Structure

| Path | What goes in it | File naming |
| --- | --- | --- |
| `Docs/README.md` | This file. Map of the documentation + conventions. | — |
| `Docs/commit_guide.md` | Git commit rules we both follow. | — |
| `Docs/subject/` | The subject PDF and its Japanese translation. | `en.subject.pdf`, `ja.subject.md` |
| `Docs/pair_communication/` | One file per meeting: agenda, decisions, open questions, TODOs with an owner. | `YYYY-MM-DD_short-topic.md` |
| `Docs/work_log/` | One file per person per day: what I did / what is next / where I got stuck / time spent. | `YYYY-MM-DD_<author>.md` |
| `Docs/learning_log/` | One file per concept, **rewritten in your own words** — not pasted references. | `topic-name.md` (kebab-case) |
| `Docs/implementation_plans/` | The design we actually adopted: scope, interface, steps, edge cases, complexity, test plan. | `topic-name.md` (kebab-case) |

`<author>` is `so` (skusakab) or `javi` (jperez-u).

### Naming conventions

- Dates are always **ISO 8601**: `2026-08-13`. It sorts correctly in `ls` and in the GitHub file list.
- Topic slugs are **kebab-case, lowercase, ASCII**: `hex-wall-encoding.md`, not `Hex Wall Encoding.md`.
  Spaces and non-ASCII characters make `git`, shell globbing, and links harder for both of us.
- One meeting = one file. One person-day = one file. One concept = one file.
  **Never** append today's log to yesterday's file — the diff becomes unreadable.
- Every document starts from the matching `TEMPLATE.md` in the same folder. Copy it, do not edit it in place.

### Language rule

Every document in `Docs/` is **bilingual**. Javier does not read Japanese and So is a Japanese speaker, so a
document that only one of us can read is not a shared document.

- README / guide files: an `## English` section and a `## 日本語` section.
- Templates and logs: bilingual headings (`## Decisions / 決定事項`). Write the **body in English** so both of us
  can read it; add Japanese notes underneath a heading when the nuance matters. The exception is
  `learning_log/`, where the deep explanation is written in Japanese on purpose (it is So's own understanding),
  with a short English summary on top so Javier can still follow.

### Commit convention (summary)

`type(scope): summary` — for example `docs(setup): scaffold bilingual Docs structure`.
Full rules, the list of types, and the scopes we use are in [commit_guide.md](commit_guide.md).

---

## 日本語

### このフォルダの目的

コードは「**何を**作ったか」を示す。このフォルダは「**なぜ**そう作ったか」「**いつ**そう決めたか」
「**各自が何を理解したか**」を残す場所。目的は 4 つ:

1. **振り返り** — 数週間後に決定の「理由」を思い出せる。結果だけ残っていても再現できない。
2. **継続性** — 片方が 3 日離れても、相方はログを読めばミーティングなしで続きを進められる。
3. **ディフェンス材料** — ピア評価では、**自分が書いていない部分も含めて**プロジェクトのどこでも説明を求められる。
   この文書群がそのための教材になる。
4. **相方への早期共有** — 設計を「コードを書く前」に文章にすると、コードが存在する前にレビューできる。
   後からレビューするより圧倒的に安い。

> subject には「評価中に小さな修正を求められることがあり、**両方の学生**が実装を理解し変更できる必要がある」と
> 明記されている。ここに書くことは余計な作業ではなく、ディフェンスに通るための作業。

### 構成

| パス | 何を置くか | ファイル命名 |
| --- | --- | --- |
| `Docs/README.md` | このファイル。ドキュメント全体の地図と規約。 | — |
| `Docs/commit_guide.md` | 二人で守る git コミット規約。 | — |
| `Docs/subject/` | subject PDF とその日本語訳。 | `en.subject.pdf`, `ja.subject.md` |
| `Docs/pair_communication/` | 1 ミーティング 1 ファイル。議題・決定事項・未解決事項・担当者付き TODO。 | `YYYY-MM-DD_short-topic.md` |
| `Docs/work_log/` | 1 人 1 日 1 ファイル。やったこと / 次にやること / 詰まったこと / 作業時間。 | `YYYY-MM-DD_<author>.md` |
| `Docs/learning_log/` | 1 概念 1 ファイル。**参考資料の貼り付けではなく自分の言葉で再構成する**。 | `topic-name.md`(kebab-case) |
| `Docs/implementation_plans/` | 実際に採用した設計。Scope / Interface / 手順 / エッジケース / 計算量 / テスト方針。 | `topic-name.md`(kebab-case) |

`<author>` は `so`(skusakab)または `javi`(jperez-u)。

### 命名規約

- 日付は必ず **ISO 8601**(`2026-08-13`)。`ls` でも GitHub のファイル一覧でも正しい順に並ぶため。
- トピック名は **kebab-case・小文字・ASCII**。`hex-wall-encoding.md` であって `Hex Wall Encoding.md` ではない。
  空白や非 ASCII は git・シェルの glob・リンクを扱いにくくする。
- 1 ミーティング = 1 ファイル、1 人日 = 1 ファイル、1 概念 = 1 ファイル。
  **昨日のファイルに今日のログを追記しない**(diff が読めなくなる)。
- 各ドキュメントは同じフォルダの `TEMPLATE.md` からコピーして作る。テンプレート自体を書き換えない。

### 言語ルール

`Docs/` 配下は**すべてバイリンガル**。Javier は日本語を読まないので、片方しか読めない文書は共有文書ではない。

- README・ガイド類:`## English` と `## 日本語` の 2 セクション。
- テンプレート・ログ類:見出しをバイリンガル(`## Decisions / 決定事項`)にし、**本文は英語**で書く。
  ニュアンスが重要な箇所は見出しの下に日本語メモを足す。
  例外は `learning_log/` で、ここは深い説明を意図的に日本語で書く(So 自身の理解の記録なので)。
  ただし Javier も追えるよう、冒頭に短い英語サマリーを必ず付ける。

### コミット規約(要約)

`type(scope): summary` 形式。例:`docs(setup): scaffold bilingual Docs structure`。
type の一覧・scope・詳細ルールは [commit_guide.md](commit_guide.md) を参照。
