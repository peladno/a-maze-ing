# A-Maze-ing — working notes for Claude

A 42 pair project (so / skusakab and javi / jperez-u). A Python maze generator that reads a
config file, generates a maze, writes it as hexadecimal wall masks, and displays it.

> **This file is loaded into every session. Keep it short.** Details belong in `Docs/`; this
> file only says where to look and how to behave.

---

## 1. How to work with so — learning-support mode

**so is the author of every line of assignment code.** The point of this project is that so
can explain and modify any part of it at the defense (§IX), so:

- **Do not write implementation code.** Give hints, concepts, and reviews instead.
- **Review in three parts:** where the problem is / why it is a problem / a hint for fixing
  it. Say what is right, too.
- **Explain Python fundamentals as they come up.** so is partway through 42's Python module,
  so a language feature met here is usually being met for the first time.
- **Claude may write:** docstrings (on request), documents under `Docs/`, and mechanical
  edits so asks for by name.
- **Never commit or push without being asked.** Never create a virtualenv or install
  packages — show the command instead.
- Reply in Japanese.

**Exception:** javi's own work areas (below) are not covered by this mode.

**JA** — so が課題コードを全部書く。Claude はヒント・概念解説・レビューに徹する。
実装コードは書かない。docstring と `Docs/` 配下は依頼があれば書いてよい。
commit / push / 仮想環境の作成は、必ず確認を取ってから。日本語で応答する。

## 2. Where things are

| Path | What it holds |
| --- | --- |
| `Docs/subject/ja.subject.md` | the subject, translated. **Section numbers (§IV.2 etc.) are quoted everywhere** |
| `Docs/implementation_plans/` | the contract for each module, written **before** the code |
| `Docs/implementation_plans/architecture-overview.md` | **start here** — the pipeline and who owns what |
| `Docs/learning_log/` | one concept per file, fully bilingual, written for future-so |
| `Docs/work_log/` | per session: done / next / stuck / learned / for the pair |
| `Docs/pair_communication/01_kickoff.md` | **every design decision, numbered.** Quote decision numbers (3.2, 3.9 …) |

**Read the relevant plan before touching a module.** If the design changes while
implementing, update the plan **in the same commit** as the code.

## 3. Commands

```bash
make install    # poetry install    (needed on a fresh clone)
make test       # poetry run pytest -q
make lint       # flake8 + mypy with the §III.2 flags
make run        # python3 a_maze_ing.py config.txt
```

Python >= 3.10, Poetry (decision 2.1 = D). Run `make lint` before every commit: §III.2 makes
it a graded rule, and `F`-codes from pyflakes are usually real bugs.

## 4. Conventions

- **Docstrings:** NumPy sections, in English. They ship with the code and the evaluator reads
  them, so **never name internal task numbers** (`W12`) in them. Subject sections (§IV.5) are
  fine and useful.
- **Error messages:** `source:line: KEY must be …, got '…'`. Built from `_where` so the format
  lives in one place. User vocabulary only — no parameter or type names.
- **Commits:** `type(scope): imperative summary`, then a body explaining **why**, wrapped at
  72 columns. Reference subject sections as `IV.2`, not `§IV.2`.
- **Branches:** docs may go straight to `main`; code goes on `feature/<topic>`.
- **Tests** are not submitted or graded (§III.3), but a test that has never failed proves
  nothing — check what would break it.

## 5. Work split

- **so:** W01–W12 — config, `Maze`, the generator, validation, the solver.
- **javi:** W13–W17, W20–W24 — hex output, the writer, the terminal renderer,
  `a_maze_ing.py`, packaging.

§IX requires both of them to explain and modify any part, which is why `learning_log/` files
are bilingual in one file.

## 6. Where the work is right now

Read the newest file in `Docs/work_log/` first — its §2 *Next* is the to-do list, and §5 is
what the pair still owes each other.

Two things outstanding across the whole repo:

- **`a_maze_ing.py` does not exist**, though §IV.2 fixes that filename and `make run` calls it
  (javi, W17).
- **`config.txt` at the repo root is empty**, though §IV.3 requires a default config.
