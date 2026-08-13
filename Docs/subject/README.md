# subject/

---

## English

### What goes here

| File | Content |
| --- | --- |
| `en.subject.pdf` | The original subject PDF, exactly as distributed. **Never edit it.** |
| `ja.subject.md` | Full Japanese translation of the subject, for So. Chapter numbering matches the PDF. Its appendix holds a requirements checklist (every "must" as a checkbox) we tick off before the defense. Translator's notes are marked 訳注. |

### Why keep the subject inside the repository

- The subject is the **contract**. Every design decision in `implementation_plans/` must be traceable back to a
  line of it. Having it one directory away makes "where does this requirement come from?" a 10-second question.
- The subject is versioned (this one is **v2.2**). If a new version is published mid-project, a diff against the
  copy stored here tells us exactly what changed.
- At the defense, both of us must be able to point at the requirement behind a feature. Reading it together is
  part of the work, not a formality.

### How to read it (recommended order)

1. **IV. Mandatory part** — usage, config format, maze requirements, output format. This is what is graded first.
2. **V. Visual representation** — the display and the required user interactions.
3. **VI. Code reusability** — the `MazeGenerator` class and the `mazegen-*` package.
4. **III. Common Instructions** — Python 3.10+, flake8, mypy flags, docstrings, Makefile rules.
5. **VII. Readme Requirements** — read this **early**, not at the end: it dictates what we must record about our
   planning and our AI usage as we go. If we only read it on the last day, the information is already lost.

### Rules

- Do not commit any modification of `en.subject.pdf`.
- When the notes and the PDF disagree, **the PDF wins**. Fix the notes.
- Quote the subject with its section number when you cite it elsewhere, e.g. "IV.5 says every line ends with `\n`".

---

## 日本語

### ここに置くもの

| ファイル | 内容 |
| --- | --- |
| `en.subject.pdf` | 配布された subject PDF の原本。**絶対に編集しない**。 |
| `ja.subject.md` | subject の日本語全訳。章番号は PDF と一致。巻末に要件チェックリスト(「must」を全部チェックボックス化)を持ち、ディフェンス前の抜け漏れ確認に使う。訳者の補足は「訳注」と明示。 |

### なぜ subject をリポジトリに置くのか

- subject は**契約書**。`implementation_plans/` の設計判断はすべて subject の記述に遡れなければならない。
  隣のディレクトリにあれば「この要件はどこ由来?」が 10 秒で終わる。
- subject にはバージョンがある(これは **v2.2**)。途中で新版が出た場合、ここのコピーとの diff で
  何が変わったか正確に分かる。
- ディフェンスでは、機能の裏にある要件を二人とも指し示せる必要がある。一緒に読むこと自体が作業の一部。

### 読む順番(推奨)

1. **IV. Mandatory part** — 実行方法・設定ファイル形式・迷路の要件・出力形式。最初に採点される部分。
2. **V. Visual representation** — 表示と、必須のユーザー操作。
3. **VI. Code reusability** — `MazeGenerator` クラスと `mazegen-*` パッケージ。
4. **III. Common Instructions** — Python 3.10+、flake8、mypy のフラグ、docstring、Makefile のルール。
5. **VII. Readme Requirements** — **最後ではなく早い段階で読む**。計画の推移や AI の使い方など、
   「進めながら記録しておかないと失われる情報」を要求しているため。最終日に読んでも手遅れになる。

### ルール

- `en.subject.pdf` の変更をコミットしない。
- メモと PDF が食い違ったら、**PDF が正**。メモの方を直す。
- 他の文書から引用するときは節番号を添える。例:「IV.5 に全行が `\n` で終わると書いてある」。
