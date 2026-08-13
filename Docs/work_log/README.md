# work_log/

---

## English

### Purpose

**One person, one day, one file.** A short daily record of what I did, what I will do next, where I got stuck,
and how long it took.

This is not a diary and not a status report for a manager. It is a tool with four concrete uses.

### Why we write it

- **Review** — at the end of the project you can see where the time actually went, which is the only honest input
  for the subject's README question *"your anticipated planning and how it evolved"*.
- **Continuity** — tomorrow-you has forgotten today's context. The "Next" section is a handover note to yourself;
  it removes the 20 minutes of "where was I?" at the start of every session.
- **Defense material** — "what worked well and what could be improved" is a graded README item. The answer is in
  these files, especially in the **Stuck** section.
- **Early sharing** — Javier can read what you did without asking. A blocker written down today is a blocker
  the other person can unblock tomorrow morning.

### Naming

`YYYY-MM-DD_<author>.md` where `<author>` is `so` or `javi` — e.g. `2026-08-13_so.md`.

Both of us write our own file. Never edit the other person's log; comment in the pair meeting instead.

### How to use

1. Copy `TEMPLATE.md` at the **start** of a work session, not at the end.
2. Fill "Done" as you go — reconstructing a day from memory produces a fiction.
3. Always fill **Next**, even one line. That line is what you read first tomorrow.
4. Be honest in **Stuck**. A log that only records successes is useless for the defense.
5. Commit at the end of the session: `docs(log): work log 2026-08-13 so`.

### Rules

- Keep it under ~10 minutes of writing. A log that costs 30 minutes stops being written by day 3.
- Record **time spent**, even approximately. Estimation only improves if you measure.
- Link to the real artifacts: commit hashes, branch names, `Docs/learning_log/*.md`, `Docs/implementation_plans/*.md`.
- Write the body in English so the other one can read it.

### Good first entries for this project

1. `2026-08-13_so.md` — read the subject, listed the mandatory requirements, set up the repo and `Docs/`.
2. `YYYY-MM-DD_so.md` — set up the virtual environment, `flake8` and `mypy` with the subject's exact flags.
3. `YYYY-MM-DD_so.md` — ran `maze_analyzer.py --help` and understood what it verifies (it defines "done" for us).
4. `YYYY-MM-DD_so.md` — studied the hexadecimal wall encoding and reproduced the example output by hand on paper.
5. `YYYY-MM-DD_so.md` — first design session for the config parser, written up in `implementation_plans/`.
6. `YYYY-MM-DD_so.md` — installed the provided MLX wheel and rendered one window to check the environment works.

---

## 日本語

### 目的

**1 人・1 日・1 ファイル。** その日にやったこと、次にやること、詰まったこと、かかった時間の短い記録。

日記でもなければ上司向けの進捗報告でもない。次の 4 つの具体的な用途を持つ道具。

### なぜ書くのか

- **振り返り** — プロジェクト終了時に「実際に時間がどこへ消えたか」が見える。
  subject の README 要件「当初の計画とその変化」に対して、正直に答えられる唯一の材料になる。
- **継続性** — 明日の自分は今日の文脈を忘れている。「Next」欄は自分宛ての引き継ぎメモで、
  毎回のセッション冒頭に発生する「どこまでやったっけ」の 20 分を消す。
- **ディフェンス材料** — 「うまくいったこと / 改善できること」は README の採点項目。
  その答えはこのファイル群、特に **Stuck** 欄にある。
- **早期共有** — Javier は聞かなくても状況を読める。今日書いた詰まりは、明日の朝に相方が解ける詰まりになる。

### 命名

`YYYY-MM-DD_<author>.md`(`<author>` は `so` または `javi`)— 例:`2026-08-13_so.md`。

各自が自分のファイルを書く。相方のログは編集しない(意見はペアミーティングで言う)。

### 使い方

1. `TEMPLATE.md` をコピーするのは作業の**終わり**ではなく**開始時**。
2. 「Done」は進めながら書く。1 日を後から思い出して書くと創作になる。
3. **Next** は必ず埋める。1 行でいい。明日いちばん最初に読む行になる。
4. **Stuck** は正直に書く。成功しか記録しないログはディフェンスで役に立たない。
5. セッション終わりにコミット:`docs(log): work log 2026-08-13 so`。

### ルール

- 書くのは 10 分以内に収める。30 分かかるログは 3 日目で書かれなくなる。
- **作業時間**を必ず残す(概算でよい)。見積もりは計測しない限り上達しない。
- 実体にリンクする:コミットハッシュ、ブランチ名、`Docs/learning_log/*.md`、`Docs/implementation_plans/*.md`。
- 本文は英語で書く(相方が読めるように)。

### この課題で最初に書くと良い記録

1. `2026-08-13_so.md` — subject を読む、必須要件を洗い出す、リポジトリと `Docs/` を用意する。
2. `YYYY-MM-DD_so.md` — 仮想環境の構築、subject 指定のフラグどおりの `flake8` / `mypy` 設定。
3. `YYYY-MM-DD_so.md` — `maze_analyzer.py --help` を実行し、何を検証するツールか理解する(これが「完成」の定義になる)。
4. `YYYY-MM-DD_so.md` — 16 進のウォールエンコーディングを学び、subject の出力例を紙の上で手で再現する。
5. `YYYY-MM-DD_so.md` — 設定ファイルパーサの最初の設計セッション。結果は `implementation_plans/` に書く。
6. `YYYY-MM-DD_so.md` — 配布された MLX の wheel を入れ、ウィンドウを 1 枚出して環境を確認する。
