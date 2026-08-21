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

| # | Item | Owner | Ref | Status (2026-08-20) |
| --- | --- | --- | --- | --- |
| F1 | Fix `Makefile`: recipe lines use spaces, so `make` fails with `missing separator`. Add the missing `debug` rule (§III.2). Point `run` at `python3 a_maze_ing.py config.txt` (§IV.2), not `python -m mazegen`. | javi | W20 | **accepted** — javi: unfinished, fixing today. He could not test it because his machine cannot run `make` (see F8). |
| F2 | Produce `mazegen-*` at the repository root, not `a_maze_ing-*` in `dist/`. | javi | W19, §VI | **accepted** |
| F3 | Move `mypy`, `flake8` (and `pytest`) out of `[project] dependencies` into a dev group. | javi | W20 | open |
| F4 | Decide whether `python-dotenv` is needed at all — config parsing is W01 and its error policy was settled in 3.9. | so + javi | W01, 3.9 | open |
| F5 | Correct `poetry_proposal.md` § 6 and its conclusion (see §2 above). | javi | §VII | **acknowledged** — "I will check it" |
| F6 | `license = "LICENCE.md"` in `pyproject.toml` — the file is `LICENSE.md`; and the copyright line still names only javi. | javi | 5.3 | **partly accepted** — javi will add so's name (the file was generated by GitHub and never reviewed). The `LICENCE.md` spelling in `pyproject.toml` was not mentioned and is still open. |
| F7 | Update the README setup section once F1–F3 land: it must state that Poetry is required and how to install it. | javi | W23, §VII | pending F1–F3 |
| F8 | Add `.gitattributes` with `* text=auto eol=lf`, and `eol=lf` on `Makefile` explicitly. | javi | W20 | **new** — see §6 |

## 5. Unchanged by this decision / この決定で変わらないこと

**EN** — Everything else in 2.1 stands: Python 3.10+, and the two of us on the same minor version. The lock file
now makes the dependency half of that automatic, but **the interpreter version is still an agreement** — Poetry
records a constraint, it does not install a Python for us.

**JA** — 2.1 の他の部分は有効:Python 3.10 以降で、二人が同じマイナーバージョンを使う。
依存関係については lock が自動化してくれるが、**インタプリタのバージョンは依然として口約束**。
Poetry は制約を記録するだけで、Python 本体を入れてくれるわけではない。


## 6. Environment finding: javi works on a company Windows PC / 環境に関する判明事項

**EN** — javi reported (2026-08-20) that he is working from a company Windows machine, which is why he could not
test the `Makefile`. This is not a one-off inconvenience — three consequences follow, and they are recorded here
because they affect decisions we have already taken.

1. **He cannot run `make lint`.** flake8 and mypy are graded (§III.1), and 2.2 — how strict we go — is still open.
   Code arriving unchecked is a slow leak, not a single event.
2. **W15 is the work most exposed to this.** 4.1 chose terminal rendering, and ANSI escapes, box-drawing
   characters, encoding and terminal width all behave differently on a Windows console than on the machines the
   evaluation runs on. Something that looks correct on his screen can break on the evaluator's.
3. **Line endings.** There is no `.gitattributes` and `core.autocrlf` is unset, so a Windows edit can convert
   files to CRLF — and a CRLF `Makefile` breaks `make` again, in a different way from the TAB problem. That is F8.

**JA** — javi から、会社の Windows PC で作業していると連絡があった(2026-08-20)。
`Makefile` を検証できなかったのはこのため。単発の不便ではなく、既に下した決定に影響する帰結が 3 つあるので記録する。

1. **`make lint` を回せない。** flake8 と mypy は採点対象(§III.1)で、2.2(どこまで strict にするか)は未決のまま。
   検査されないコードが入り続けるのは、一度きりの事故ではなくじわじわ漏れる問題。
2. **最も影響を受けるのは W15。** 4.1 でターミナル描画に決めた以上、ANSI エスケープ・罫線文字・文字コード・
   端末幅の扱いが Windows コンソールと評価環境で異なる。彼の画面で正しく見えるものが評価者の画面で崩れうる。
3. **改行コード。** `.gitattributes` がなく `core.autocrlf` も未設定なので、Windows での編集で CRLF になりうる。
   CRLF の `Makefile` は、TAB の件とは別の形で再び `make` を壊す。これが F8。

**Open / 未解決** — which machine will javi use on evaluation day? §IX requires both of us to modify code in front
of the evaluator, and the company PC cannot be brought there. How much time he has on a 42 machine changes how
defensively W15 has to be written. Tracked as Q5 in `01_kickoff.md`.
