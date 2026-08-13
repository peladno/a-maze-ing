# pair_communication/

---

## English

### Purpose

**One meeting = one file.** Whatever we agreed on verbally stops existing the moment we forget it, and two people
remembering a decision differently is the most expensive kind of bug in a pair project — it is discovered at
integration time, after both sides are already written.

A file here records: what we discussed, **what we decided**, what is still open, and who does what next.

### Why we write it

- **Review** — "why did we pick a bitmask instead of four booleans?" has an answer with a date on it.
- **Continuity** — if one of us misses a session, reading one file replaces the meeting.
- **Defense material** — the subject's README requirements ask for our roles, our planning, **how the planning
  evolved**, and what worked or did not. That history cannot be reconstructed at the end; it has to be logged now.
- **Early sharing** — an interface agreed in writing before either side codes it is the cheapest integration
  we will ever get.

### Naming

`YYYY-MM-DD_short-topic.md` — e.g. `2026-08-13_kickoff.md`, `2026-08-20_wall-encoding-contract.md`.

If two meetings happen on the same day, the topic slug keeps them distinct. Do not append to an existing file.

### How to use

1. Copy `TEMPLATE.md` to the new filename **before** the meeting and fill in the agenda.
2. Fill the decisions during or immediately after the meeting — not the next day.
3. Every TODO gets an **owner** (`so` / `javi` / `both`) and a **due date**. A TODO without an owner is a wish.
4. Commit it: `docs(pair): log <topic> meeting`.

### Rules that keep this useful

- Record **decisions**, not transcripts. "We discussed algorithms for a while" is worthless;
  "We chose X because Y, rejected Z because W" is the whole point.
- Always record the **rejected** option and why. At the defense you will be asked "why not the other one?".
- If a decision is later reversed, write a **new** file that links back to the old one. Never rewrite history.
- Write the body in English so both of us can read it.

### Good first topics for this project

1. `2026-08-13_kickoff.md` — subject reading, deadline, meeting rhythm, tooling (Python version, venv, flake8/mypy).
2. `YYYY-MM-DD_role-division.md` — turning Javier's proposal in `implementation_plans/` into an agreed split.
3. `YYYY-MM-DD_maze-data-structure.md` — the shared in-memory representation both sides will depend on.
4. `YYYY-MM-DD_wall-encoding-contract.md` — bit order N/E/S/W and the coherence rule between neighbours (subject IV.5).
5. `YYYY-MM-DD_algorithm-choice.md` — which generation algorithm, and how `PERFECT=True` / `False` are handled.
6. `YYYY-MM-DD_renderer-choice.md` — terminal ASCII vs MLX, and who owns the interaction loop (subject V).

---

## 日本語

### 目的

**1 ミーティング = 1 ファイル。** 口頭で合意したことは、忘れた瞬間に存在しなくなる。
そして「二人が別々の内容を覚えている」状態は、ペア課題で最も高くつくバグ — 両側を書き終えた統合時に発覚するため。

ここに置くファイルが記録するのは、話したこと・**決めたこと**・未解決のこと・次に誰が何をするか。

### なぜ書くのか

- **振り返り** — 「なぜ bool 4 個ではなくビットマスクにしたのか」に、日付付きの答えが残る。
- **継続性** — 片方が参加できなくても、1 ファイル読めばミーティングの代わりになる。
- **ディフェンス材料** — subject の README 要件は、役割分担・計画・**計画がどう変化したか**・
  うまくいったこと/改善点を要求している。これは最後に思い出して書けるものではない。今記録するしかない。
- **早期共有** — どちらもコードを書く前に文章でインターフェースを合意しておくのが、最も安上がりな統合。

### 命名

`YYYY-MM-DD_short-topic.md` — 例:`2026-08-13_kickoff.md`、`2026-08-20_wall-encoding-contract.md`。

同じ日に 2 回話したときはトピック名で区別する。既存ファイルへの追記はしない。

### 使い方

1. ミーティング**前**に `TEMPLATE.md` をコピーし、議題を埋めておく。
2. 決定事項はミーティング中か直後に書く。翌日にしない。
3. TODO には必ず**担当者**(`so` / `javi` / `both`)と**期日**を付ける。担当者のない TODO はただの願望。
4. コミットする:`docs(pair): log <topic> meeting`。

### 有用に保つためのルール

- **議事録ではなく決定を書く**。「アルゴリズムについてしばらく話した」は無価値。
  「Y の理由で X を採用、W の理由で Z を却下」が本体。
- **却下した案とその理由**も必ず書く。ディフェンスでは「なぜもう一方にしなかったのか」を必ず聞かれる。
- 後で決定を覆すときは、**新しいファイル**を作って古いファイルにリンクする。履歴は書き換えない。
- 本文は英語で書く(二人とも読めるように)。

### この課題で最初に書くと良いトピック

1. `2026-08-13_kickoff.md` — subject 読み合わせ、締切、ミーティングの頻度、ツール(Python バージョン、venv、flake8/mypy)。
2. `YYYY-MM-DD_role-division.md` — `implementation_plans/` にある Javier の分担案を、合意済みの分担に落とす。
3. `YYYY-MM-DD_maze-data-structure.md` — 両側が依存する、メモリ上の共有表現。
4. `YYYY-MM-DD_wall-encoding-contract.md` — N/E/S/W のビット順と、隣接セル間の整合ルール(subject IV.5)。
5. `YYYY-MM-DD_algorithm-choice.md` — どの生成アルゴリズムにするか、`PERFECT=True` / `False` をどう扱うか。
6. `YYYY-MM-DD_renderer-choice.md` — ターミナル ASCII か MLX か、操作ループを誰が持つか(subject V)。
