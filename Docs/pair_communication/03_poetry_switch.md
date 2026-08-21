# 03 — Switching from venv + pip to Poetry

| | |
| --- | --- |
| **Date / 日付** | 2026-08-20 |
| **Participants / 参加者** | javi (proposed and implemented), so (reviewed and accepted) |
| **Supersedes / 上書きする決定** | `01_kickoff.md` § 2.1 — option A (`venv` + `pip`) |
| **Related / 関連** | `Docs/implementation_plans/poetry_proposal.md`, `Docs/pair_communication/02_maze_file_structure_proposal.md`, subject §III.2, §VI |

**EN** — A reversal of a recorded decision gets its own file rather than an edit in place: §VII asks for our
planning **and how it evolved**, and that history is only readable if the original decision and its replacement
both survive. `01_kickoff.md` § 2.1 now points here.
**JA** — 決定の覆しは、その場で書き換えず新しいファイルに残す。
§VII は計画**とその変化**を求めており、その履歴は「元の決定」と「置き換えた決定」の両方が残って初めて読める。
`01_kickoff.md` § 2.1 からここにリンクしてある。

---

## 1. What changed / 何が変わったか

**EN** — 2.1 was decided as `python3 -m venv` + `pip install -r requirements.txt`. javi proposed Poetry in
`poetry_proposal.md`, implemented it (`pyproject.toml`, `poetry.lock`, a Poetry-based `Makefile`) and removed
`requirements.txt`. so reviewed it and accepted.

**JA** — 2.1 は `python3 -m venv` + `pip install -r requirements.txt` で決定していた。
javi が `poetry_proposal.md` で Poetry を提案し、実装まで行い(`pyproject.toml`、`poetry.lock`、
Poetry ベースの `Makefile`)、`requirements.txt` を削除した。so がレビューのうえ受け入れた。

## 2. Decision / 決定

**EN** — **Adopt Poetry** for dependency management, the virtual environment, and the build backend.

**JA** — 依存管理・仮想環境・ビルドバックエンドとして **Poetry を採用する**。

### Reasons / 理由

**EN** —
1. **The lock file.** `poetry.lock` pins exact versions, so both machines and the evaluator's resolve to the same
   environment. Under 2.1's original answer this was only an agreement between us, with nothing enforcing it.
2. **Runtime and dev dependencies are separated.** `pytest`, `flake8` and `mypy` are tools, not things a user of
   `mazegen` should be made to install.
3. **We need a build backend anyway.** §VI requires a distributable package built from source in a clean
   virtualenv during the evaluation. Poetry provides that without configuring a separate tool.
4. **It was already built.** javi had it working before the review, so adopting it costs nothing more.

**JA** —
1. **lock ファイル。** `poetry.lock` が正確なバージョンを固定するので、二人と評価者の環境が同じ解決結果になる。
   当初の 2.1 では、これは口約束でしかなく、強制する仕組みがなかった。
2. **runtime と dev の依存が分離できる。** `pytest` / `flake8` / `mypy` はツールであって、
   `mazegen` の利用者に入れさせるものではない。
3. **どのみちビルド機構が要る。** §VI は評価中にクリーンな virtualenv でソースからビルドし直すことを要求している。
   Poetry は別ツールを設定せずにそれを提供する。
4. **すでに動いている。** javi がレビュー前に構築済みなので、採用の追加コストがない。

### What this decision does *not* rest on / この決定が根拠に**していない**こと

**EN** — `poetry_proposal.md` § 6 states that the subject lists Poetry as the expected workflow. **It does not.**
§III.2 names `pip`, `uv` and `pipx`, and never mentions Poetry. The proposal's conclusion — that pip "would not
meet the project's stated requirements" — is likewise too strong: pip is explicitly permitted.

This matters because §VII is graded and an evaluator can open the subject. The defensible claim is the accurate
one: **the subject allows any package manager, and we chose Poetry for the reasons above.** `poetry_proposal.md`
should be corrected before it feeds the README.

**JA** — `poetry_proposal.md` の § 6 は「subject が期待するワークフローとして Poetry が記載されている」と書いているが、
**そのような記載はない。** §III.2 が挙げているのは `pip` / `uv` / `pipx` で、Poetry は一度も登場しない。
同じく結論部の「pip では要件を満たせない」も過大で、pip は明示的に許可されている。

§VII は採点対象であり、評価者は subject を開ける。したがって主張すべきは正確な方:
**subject は任意のパッケージマネージャを許容しており、その中で上の理由から Poetry を選んだ。**
README の材料になる前に `poetry_proposal.md` を修正すること。

## 3. Cost we accept / 受け入れるコスト

| | EN | JA |
| --- | --- | --- |
| **1** | Poetry itself must be installed before `make install` works, so the README needs an explicit setup line — the evaluator's machine may not have it. | `make install` の前に Poetry 自体のインストールが必要。評価者のマシンにあるとは限らないので README に手順を明記する。 |
| **2** | The build is driven by `pyproject.toml`, which currently names the project `a-maze-ing` and therefore does **not** produce `mazegen-*`. §VI also requires that file **at the repository root**, not in `dist/`. | ビルドは `pyproject.toml` に従うが、現状 `name = "a-maze-ing"` なので **`mazegen-*` を生成しない**。§VI はそのファイルを **`dist/` ではなくリポジトリのルート**に置くことも要求している。 |

## 4. Follow-ups / 残作業

| # | Item | Owner | Ref |
| --- | --- | --- | --- |
| F1 | Fix `Makefile`: recipe lines use spaces, so `make` fails with `missing separator`. Add the missing `debug` rule (§III.2). Point `run` at `python3 a_maze_ing.py config.txt` (§IV.2), not `python -m mazegen`. | javi | W20 |
| F2 | Produce `mazegen-*` at the repository root, not `a_maze_ing-*` in `dist/`. | javi | W19, §VI |
| F3 | Move `mypy`, `flake8` (and `pytest`) out of `[project] dependencies` into a dev group. | javi | W20 |
| F4 | Decide whether `python-dotenv` is needed at all — config parsing is W01 and its error policy was settled in 3.9. | so + javi | W01, 3.9 |
| F5 | Correct `poetry_proposal.md` § 6 and its conclusion (see §2 above). | javi | §VII |
| F6 | `license = "LICENCE.md"` in `pyproject.toml` — the file is `LICENSE.md`; and the copyright line still names only javi. | javi | 5.3 |
| F7 | Update the README setup section once F1–F3 land: it must state that Poetry is required and how to install it. | javi | W23, §VII |

## 5. Unchanged by this decision / この決定で変わらないこと

**EN** — Everything else in 2.1 stands: Python 3.10+, and the two of us on the same minor version. The lock file
now makes the dependency half of that automatic, but **the interpreter version is still an agreement** — Poetry
records a constraint, it does not install a Python for us.

**JA** — 2.1 の他の部分は有効:Python 3.10 以降で、二人が同じマイナーバージョンを使う。
依存関係については lock が自動化してくれるが、**インタプリタのバージョンは依然として口約束**。
Poetry は制約を記録するだけで、Python 本体を入れてくれるわけではない。
