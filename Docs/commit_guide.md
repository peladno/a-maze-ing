# Commit Guide / コミット規約

---

## English

### Why we bother

A commit history is a document that writes itself — if the messages are good. When we prepare for the defense,
`git log --oneline` should read like a table of contents of the project. When something breaks,
`git log -S "some_symbol"` should point at the commit that introduced it, and the message should explain why it
was introduced. Neither works if every message says `update` or `fix`.

### Format

```text
type(scope): summary

optional body: WHY this change, not WHAT (the diff already shows what)

optional footer: refs, co-author
```

Rules for the first line:

- **≤ 50 characters** if possible, hard limit 72. `git log --oneline` truncates the rest.
- **Imperative mood**: `add`, not `added` / `adds`. Read it as *"if applied, this commit will …"*.
- **Lowercase** summary, **no trailing period**.
- One logical change per commit. If the summary needs "and", it is probably two commits.

### Types

| Type | Use for |
| --- | --- |
| `feat` | New behaviour visible to the user of the program or of the module. |
| `fix` | A bug fix. |
| `docs` | Documentation only, including everything under `Docs/` and `README.md`. |
| `test` | Adding or changing tests only. |
| `refactor` | Behaviour unchanged, structure changed. |
| `style` | Formatting / flake8 / type-hint-only changes, no behaviour change. |
| `chore` | Repo plumbing: `.gitignore`, `requirements.txt`, `Makefile`, packaging config. |
| `build` | Anything about producing the `mazegen-*` package artifacts. |

### Scopes for this project

`config`, `maze`, `generator`, `solver`, `validator`, `output`, `render`, `pattern42`, `mazegen`, `cli`,
`docs`, `setup`, `make`.

Scope is optional but strongly preferred — it is what makes the log skimmable.

### Examples

```text
feat(config): parse KEY=VALUE pairs and ignore comment lines
fix(output): terminate the last line with a newline
docs(setup): scaffold bilingual Docs structure
test(solver): cover the unreachable-exit case
refactor(maze): extract wall lookup into a helper
chore(setup): ignore python caches and virtualenvs
```

Bad examples and why:

| Message | Problem |
| --- | --- |
| `update` | Says nothing. Useless in `git log`. |
| `fixed bug in generator and added tests` | Past tense, two changes in one commit, no scope. |
| `feat: WIP` | A commit is not a save button. Squash or amend before pushing. |

### Pair workflow

- One branch per responsibility: `feature/<scope>-<short-topic>` (e.g. `feature/config-parser`).
- Small commits, pushed often. A branch that lives a week creates a conflict festival.
- Open a Pull Request for anything the other person will have to explain at the defense — which is almost
  everything. The reviewer's job is **not** "does it work", it is **"can I explain this to the evaluator"**.
- Merge only after both of us understand the change. Write the outcome of the review in
  `Docs/pair_communication/` if a real decision came out of it.
- Pull/rebase from `main` before starting a new piece of work.

### Useful commands

| Command | What it does |
| --- | --- |
| `git log --oneline --graph --decorate` | The readable history. Use this before every defense rehearsal. |
| `git log --oneline -- maze/generator.py` | Every commit that touched one file. |
| `git log -p -S "MazeGenerator"` | Commits that added or removed that string — how a symbol was born. |
| `git commit --amend` | Fix the message of the commit you have not pushed yet. |
| `git diff --staged` | Read your own change before committing. Do this every time. |

---

## 日本語

### なぜ規約を決めるのか

コミット履歴は「メッセージが良ければ」勝手に出来上がるドキュメント。ディフェンス準備のとき
`git log --oneline` がプロジェクトの目次のように読めるのが理想。
不具合が出たときは `git log -S "シンボル名"` でそれを入れたコミットに辿り着き、メッセージから理由が分かるのが理想。
全部 `update` や `fix` だと、このどちらも成立しない。

### 形式

```text
type(scope): summary

任意の本文:「なぜ」変えたかを書く(「何を」変えたかは diff が語る)

任意のフッター:参照、Co-authored-by
```

1 行目のルール:

- 可能なら **50 文字以内**、上限 72 文字。`git log --oneline` は途中で切られる。
- **命令形**(`add` であって `added` / `adds` ではない)。「このコミットを適用すると〜する」と読む。
- summary は**小文字始まり**、**末尾にピリオドを付けない**。
- 1 コミット = 1 論理変更。summary に「and」が必要なら、たぶん 2 コミットに分けるべき。

### type 一覧

| type | 用途 |
| --- | --- |
| `feat` | プログラム/モジュールの利用者から見える新しい振る舞い。 |
| `fix` | バグ修正。 |
| `docs` | ドキュメントのみ(`Docs/` 配下と `README.md` を含む)。 |
| `test` | テストの追加・変更のみ。 |
| `refactor` | 振る舞いは変えず構造だけ変える。 |
| `style` | 整形・flake8 対応・型ヒントのみの変更。振る舞いは変わらない。 |
| `chore` | リポジトリの配管:`.gitignore`、`requirements.txt`、`Makefile`、パッケージ設定。 |
| `build` | `mazegen-*` パッケージ成果物の生成に関わるもの。 |

### この課題で使う scope

`config`, `maze`, `generator`, `solver`, `validator`, `output`, `render`, `pattern42`, `mazegen`, `cli`,
`docs`, `setup`, `make`。

scope は任意だが強く推奨。ログを流し読みできるかどうかは scope で決まる。

### 例

```text
feat(config): parse KEY=VALUE pairs and ignore comment lines
fix(output): terminate the last line with a newline
docs(setup): scaffold bilingual Docs structure
test(solver): cover the unreachable-exit case
refactor(maze): extract wall lookup into a helper
chore(setup): ignore python caches and virtualenvs
```

悪い例とその理由:

| メッセージ | 問題 |
| --- | --- |
| `update` | 何も言っていない。`git log` で無価値。 |
| `fixed bug in generator and added tests` | 過去形・2 つの変更が同居・scope なし。 |
| `feat: WIP` | コミットは保存ボタンではない。push 前に squash か amend する。 |

### ペアでの進め方

- 責務ごとにブランチを切る:`feature/<scope>-<short-topic>`(例:`feature/config-parser`)。
- 小さくコミットし、こまめに push。1 週間生き続けるブランチはコンフリクト祭りを生む。
- **相方がディフェンスで説明することになる変更**は必ず Pull Request にする(= ほぼ全部)。
  レビュアーの仕事は「動くか」ではなく「**これを評価者に説明できるか**」。
- 二人が理解してからマージする。レビューから本物の決定が出たら `Docs/pair_communication/` に残す。
- 新しい作業を始める前に `main` を pull / rebase する。

### 使えるコマンド

| コマンド | 何をするか |
| --- | --- |
| `git log --oneline --graph --decorate` | 読める履歴。ディフェンス練習の前に必ず眺める。 |
| `git log --oneline -- maze/generator.py` | 特定ファイルを触った全コミット。 |
| `git log -p -S "MazeGenerator"` | その文字列を追加・削除したコミット。シンボルの誕生を追える。 |
| `git commit --amend` | まだ push していないコミットのメッセージを直す。 |
| `git diff --staged` | コミット前に自分の変更を読む。毎回やる。 |
