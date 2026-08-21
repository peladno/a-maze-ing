# 01 — Kickoff: roles, conventions and technical decisions

|                                 |                                                                                                                 |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Date / 日付**           |                                                                                                                 |
| **Participants / 参加者** | so (skusakab), javi (jperez-u)                                                                                  |
| **Duration / 所要時間**   |                                                                                                                 |
| **Related / 関連**        | `Docs/subject/ja.subject.md`, `Docs/implementation_plans/A-Maze-ing_Project_Structure_and_Team_Division.md` |

**EN** — This file is the agenda **and** the record. Each item gives the question, a short note on how such a
choice is usually approached, and the realistic options. Fill the `> Decision:` line during the meeting.
An item left empty is an item we will argue about again at integration time.
**JA** — このファイルは議題であると同時に記録。各項目は「問い」「一般にどう考えるか」「現実的な選択肢」で構成されている。
ミーティング中に `> Decision:` の行を埋めること。空のまま残った項目は、統合時にもう一度揉める項目になる。

**Priority legend / 優先度**

| Mark | EN                           | JA                                     |
| ---- | ---------------------------- | -------------------------------------- |
| 🔴   | Blocks coding. Decide today. | コードを書き始められない。今日決める。 |
| 🟡   | Decide this week.            | 今週中に決める。                       |
| ⚪   | Can wait, but do not forget. | 後回し可。ただし忘れない。             |

**Contents / 目次**

| Part | EN                                             | JA                                   |
| ---- | ---------------------------------------------- | ------------------------------------ |
| 1    | Ways of working                                | 進め方                               |
| 2    | Environment and tooling                        | 環境とツール                         |
| 3    | Core technical decisions                       | 中核の技術判断                       |
| 4    | Display                                        | 表示                                 |
| 5    | Reusable package and licence                   | 再利用パッケージとライセンス         |
| 6    | Testing                                        | テスト                               |
| 7    | **Role division — summary table**       | **役割分担 — 一覧表**         |
| 8    | Schedule                                       | スケジュール                         |
| 9    | **All other decisions — summary table** | **その他の決定事項 — 一覧表** |

---

## Part 1 — Ways of working / 進め方

### 1.1 🔴 Deadline and rhythm / 締切とリズム

**EN** — When is the deadline, how many days do we really have, and how often do we meet? Does either of us have
other 42 projects or exams running in parallel?
**JA** — 締切はいつで、実際に使える日数は何日か。ミーティングは何回やるか。
どちらかが並行して別の 42 課題や試験を抱えていないか。

**How to think about it / 考え方**

**EN** — Two rhythms are usually combined: a short **sync** (10–15 min, frequent, "what are you on, what is
blocking you") and a longer **design/review session** (60–90 min, weekly, decisions and code reading). Pair
projects fail far more often from drifting apart than from lack of skill, so the frequent short one matters most.
**JA** — 通常は 2 つのリズムを組み合わせる。短い**同期**(10〜15 分、頻繁、「今どこ・何で詰まっているか」)と、
長い**設計/レビュー会**(60〜90 分、週 1、決定とコード読み)。
ペア課題は技術不足より「二人がズレていくこと」で失敗する方がずっと多いので、短い方の頻度が効く。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Drift is caught within a day and blockers rarely survive overnight.  **Cost:** a fixed daily slot in a one-month project, and a short sync degenerates into status theatre when nothing is actually blocking. | ズレが 1 日で捕まり、ブロッカーが翌日まで残らない。**コスト:** 1 か月のプロジェクトに毎日の固定枠。詰まっていない日は、短い同期が形式的な報告会に堕ちる。 |
| **B** | Enough time in one sitting to actually read code together.  **Cost:** up to three days of drift between sessions — in a one-month project that is 10% of the schedule. | 1 回の枠が長く、実際に一緒にコードを読める。**コスト:** 会の間隔が最大 3 日空く。1 か月のプロジェクトでは日程の 10%。 |
| **C** | Zero scheduling overhead.  **Cost:** all coordination then rests on the logs actually being written — if 1.3 lands on the minimal option, nothing is coordinating us at all. | 日程調整の負荷がゼロ。**コスト:** 調整のすべてが「ログが実際に書かれていること」に依存する。1.3 が最小構成になると、調整する仕組みが 1 つも残らない。 |

**EN** — Note: the decision below fixes the **deadline** (9/17) but not the **rhythm** — the options above are still open.
**JA** — 注:下の決定は**締切**(9/17)を決めたが、**リズム**は未回答。上の選択肢はまだ開いている。

**Options / 選択肢**

|             | EN                                                                   | JA                                                        |
| ----------- | -------------------------------------------------------------------- | --------------------------------------------------------- |
| **A** | Daily short sync + one weekly long session.                          | 毎日の短い同期 + 週 1 の長い会。                          |
| **B** | Two fixed long sessions per week, no daily sync (rely on work logs). | 週 2 回の長い会のみ。日次同期なし(作業ログで代替)。       |
| **C** | Async by default on Discord; meet only at milestone boundaries.      | 基本 Discord で非同期。マイルストーンの区切りだけ集まる。 |

> Decision: ¹ヶ月（9/17）

### 1.2 🔴 Git workflow / git の運用

**EN** — How do changes reach `main`? Branch per person or per feature? Pull Requests or direct merges?
Is `main` allowed to be broken?
**JA** — 変更はどうやって `main` に入るか。ブランチは人ごとか機能ごとか。PR か直マージか。
`main` が壊れている状態を許すか。

**So's current proposal / So の現案**

**EN** — No Pull Requests. Each of us cuts our own branch and merges into `main` when the work is ready.
Documentation may be pushed directly to `main`.
**JA** — PR はなし。各自がブランチを切り、作業がまとまった時点で `main` にマージする。
ドキュメントは `main` への直 push を許す。

**How to think about it / 考え方**

**EN** — A PR is not paperwork; it is the moment the other person is forced to read your code. Since §IX requires
**both** of us to explain and modify any part of the project, the reading has to happen somewhere. If we drop PRs,
we must replace them with another mechanism — see 7.3 — otherwise each of us will only know half the project on
defense day. Note that `Docs/commit_guide.md` currently describes a PR-based flow; if we adopt this proposal, that
file must be updated in the same decision.
**JA** — PR は事務手続きではなく、「相方が自分のコードを読まざるを得なくなる瞬間」。
§IX は**二人とも**どの部分も説明・修正できることを要求しているので、読む行為はどこかで起きなければならない。
PR をなくすなら、別の仕組みで置き換える必要がある(7.3 参照)。さもないとディフェンス当日、各自がプロジェクトの半分しか知らない。
なお `Docs/commit_guide.md` は現状 PR 前提で書かれている。この案を採るなら、そのファイルも同じ決定の中で更新する。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Fastest path: no waiting on review, and docs never queue behind code.  **Cost:** nothing in the workflow forces either of us to read the other's code, so all of §IX preparation rests on 7.3; and `main` can break without anyone noticing. | 最速。レビュー待ちがなく、ドキュメントがコードの後ろに並ばない。**コスト:** 運用の中に「相手のコードを読む」強制力が一切なくなり、§IX への備えが 7.3 だけに乗る。さらに `main` が壊れても誰も気づかない。 |
| **B** | Same speed, but the diff is at least announced.  **Cost:** an announcement is not a read — it works only if we actually open the link. | 速度は同じで、少なくとも diff が告知される。**コスト:** 告知は「読むこと」ではない。実際にリンクを開く習慣がなければ機能しない。 |
| **C** | The shared-contract areas (W03, W04, W18) get reviewed — exactly the ones both of us depend on.  **Cost:** slower on the areas that change most in the first week. | 共有契約の領域(W03・W04・W18)にレビューが入る。二人が依存するのはまさにそこ。**コスト:** 最初の 1 週間に最も変化する領域が遅くなる。 |

**Options / 選択肢**

|             | EN                                                                                                             | JA                                                                             |
| ----------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **A** | So's proposal as written: branch per person, direct merge to`main`, docs pushed straight to `main`.        | So の現案どおり:人ごとのブランチ、`main` へ直マージ、ドキュメントは直 push。 |
| **B** | Same, but the merge is announced on Discord with a one-line summary so the other reads the diff.               | 同じだが、マージ時に Discord で 1 行要約を流し、相方が diff を読む。           |
| **C** | PR required only for the shared contract areas (data structure, encoding, public API); direct merge elsewhere. | 共有契約の領域(データ構造・符号化・公開 API)だけ PR 必須。それ以外は直マージ。 |

> Decision: A

### 1.3 🟡 Documentation habit / ドキュメントの運用

**EN** — Do we both use `Docs/work_log/` daily, `Docs/pair_communication/` per meeting, and
`Docs/implementation_plans/` before coding?
**JA** — `Docs/work_log/`(毎日)、`Docs/pair_communication/`(ミーティングごと)、
`Docs/implementation_plans/`(コードを書く前)を二人とも使うか。

**How to think about it / 考え方**

**EN** — This is not bureaucracy. Subject §VII requires the README to describe our planning, **how it evolved**,
and what worked or did not. That is history: it can be recorded but not reconstructed. The realistic risk is not
"we write too little" but "we write nothing after week one", so the rule should be small enough to survive a bad day.
**JA** — 形式主義ではない。subject §VII は README に、計画・**その変化**・うまくいったこと/改善点を求めている。
これは履歴であり、記録はできても後から復元はできない。
現実的なリスクは「書く量が足りない」ではなく「1 週目以降まったく書かなくなる」こと。
だからルールは、調子の悪い日でも守れる程度に小さくする。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Everything §VII asks for is already recorded when we need it; the planning history writes itself.  **Cost:** a daily writing habit that has to survive bad days, and a lapse is invisible until the README is due. | §VII が求めるものが、必要な時点ですでに揃っている。計画の履歴が勝手に出来上がる。**コスト:** 調子の悪い日も続ける必要があり、途切れても README を書く日まで気づけない。 |
| **B** | Effort follows the work, and the modules that matter most still get a written contract.  **Cost:** on days we only read or debug, nothing is recorded — and those days hold the best material for "what could be improved". | 労力が作業量に比例し、重要なモジュールには契約が残る。**コスト:** 読むだけ・デバッグだけの日は何も残らない。そういう日こそ「改善点」の材料が眠っている。 |
| **C** | Almost no overhead, and the shared contracts still exist.  **Cost:** §VII's "how the planning evolved" has to be reconstructed from git log and memory, which usually produces one vague paragraph. | ほぼ無負荷で、共有契約だけは残る。**コスト:** §VII の「計画がどう変化したか」を git log と記憶から復元することになり、たいてい曖昧な一段落になる。 |

**Options / 選択肢**

|             | EN                                                                                  | JA                                                                    |
| ----------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **A** | Full use of all three folders as designed.                                          | 3 フォルダすべてを設計どおり使う。                                    |
| **B** | Work log only on days we actually code; plans only for the shared-contract modules. | 作業ログはコードを書いた日だけ。計画は共有契約のモジュールだけ。      |
| **C** | Minimum: meeting records + one plan file per module, no daily log.                  | 最小構成:ミーティング記録 + モジュールごとに計画 1 枚。日次ログなし。 |

> Decision:

### 1.4 🟡 AI usage and README ownership / AI の使い方と README の担当

**EN** — Subject §II and §VII: we must state **which tasks and which parts** of the project used AI. What do we
allow ourselves, and where do we log it as we go?
**JA** — subject §II と §VII は「**どのタスクの、どの部分に** AI を使ったか」の記述を要求している。
自分たちに何を許し、進めながらどこに記録するか。

**So's current proposal / So の現案**

**EN** — Assign the **entire README** to one of us, rather than splitting it by section.
**JA** — README は節ごとに分けず、**全体をどちらか一方**に割り振る。

**How to think about it / 考え方**

**EN** — One owner gives the README a single voice and removes the "I thought you were writing that part" failure
mode; the cost is that the owner must interview the other about their half. That interview is not a downside —
it is exactly the §IX rehearsal of explaining code you did not write. The other person then reviews.
Whoever owns it needs the AI-usage log to exist from day one, so agree now where it is recorded.
**JA** — 一人が持つと README の文体が統一され、「そこは君が書くと思っていた」という失敗が消える。
代償は、担当者が相方に「あなたの担当部分」を取材しなければならないこと。
これは欠点ではなく、まさに §IX で要求される「自分が書いていないコードを説明する」練習そのもの。
その後もう一方がレビューする。
担当者が困らないよう、AI 使用ログは初日から存在している必要がある。記録場所を今決めること。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | So writes it and javi reviews; so must interview javi about W13–W17, W20 and W22–W24, which is §IX rehearsal in disguise.  **Cost:** the README is graded and so already owns 14 of 25 work areas, so this loads the heavier side further. | so が書き javi がレビュー。so は W13〜W17・W20・W22〜W24 について javi に取材せざるを得ず、これは実質 §IX の予行演習。**コスト:** README は採点対象で、so は既に 25 領域中 14 を持っている。重い側をさらに重くする。 |
| **B** | Javi owns it and so reviews; W23 is on javi's side in both of Javier's splits, so it balances the load.  **Cost:** so must still be able to defend the README's technical claims, so the interview has to run in the other direction. | javi が持ち so がレビュー。W23 は Javier の両案とも B 側なので、負荷が釣り合う。**コスト:** so も README の技術的主張を説明できる必要があるので、取材は逆向きに行われなければならない。 |
| **C** | Each person describes their own AI use accurately, which is literally what §VII asks for.  **Cost:** two voices in one document, and someone still has to merge them. | 各自が自分の AI 利用を正確に書く。§VII が求めているのは文字どおりこれ。**コスト:** 1 つの文書に 2 つの文体が混ざり、結局誰かが統合する。 |

**Consequences — AI log location / 帰結(AI ログの置き場)**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Recorded where the work is, no new file to remember.  **Cost:** scattered across the folder, so the README writer has to grep the whole log at the end. | 作業と同じ場所に残るので、新しいファイルを覚える必要がない。**コスト:** フォルダ全体に散るため、README を書く人が最後に全ログを grep することになる。 |
| **B** | One place to read when writing §VII.  **Cost:** a second file to remember to update — exactly the kind that goes stale after week one. | §VII を書くとき読む場所が 1 つ。**コスト:** 更新を忘れがちなファイルが 1 つ増える。1 週目以降に腐る典型。 |

**Options / 選択肢**

|             | EN                                                                                  | JA                                                            |
| ----------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **A** | So owns the whole README; javi reviews.                                             | README 全体を So が持ち、javi がレビュー。                    |
| **B** | Javi owns the whole README; so reviews.                                             | README 全体を javi が持ち、so がレビュー。                    |
| **C** | One owner, but the AI-usage section is written by each person about their own work. | 一人が持つが、AI 使用の節だけは各自が自分の作業について書く。 |

**AI log location / AI ログの置き場**

|             | EN                                                                | JA                                                           |
| ----------- | ----------------------------------------------------------------- | ------------------------------------------------------------ |
| **A** | A line in`Docs/work_log/` each time AI is used, tagged `AI:`. | AI を使うたび`Docs/work_log/` に `AI:` タグ付きで 1 行。 |
| **B** | A dedicated running file, e.g.`Docs/ai_usage.md`.               | 専用の通しファイル(例:`Docs/ai_usage.md`)。                |

> Decision:

---

## Part 2 — Environment and tooling / 環境とツール

### 2.1 🔴 Python version and virtual environment / Python のバージョンと仮想環境

**EN** — Subject §III.1 requires Python 3.10+. Which exact version do we both install? Which environment tool —
this choice becomes the `make install` rule (§III.2). Which OS is each of us on?
**JA** — subject §III.1 は Python 3.10 以降を要求。二人が入れる正確なバージョンは何か。
環境構築ツールは何か(この選択がそのまま `make install`(§III.2)になる)。各自の OS は何か。

**How to think about it / 考え方**

**EN** — Pin the **same** minor version on both machines. Different minor versions mean a bug can exist for one of
us and not the other, and that class of bug costs hours to even identify. `venv` is in the standard library and
needs no install, which is why it is the safe default for a graded project; `uv` is much faster but is one more
thing the evaluator's machine may not have. The OS answer also decides which MLX wheel is usable (see 4.2).
**JA** — 二人のマシンで**同じ**マイナーバージョンに固定する。マイナーが違うと、
片方にだけ再現するバグが生まれ、その種のバグは「特定するだけ」で何時間も溶ける。
`venv` は標準ライブラリでインストール不要なので、採点される課題では安全な既定。
`uv` は高速だが、評価者のマシンにない可能性のある依存が 1 つ増える。
OS の答えは、使える MLX wheel も決める(4.2 参照)。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Standard library, nothing extra to install, and `make install` is a line the evaluator's machine will certainly support.  **Cost:** slower installs than uv, and the same minor version has to be pinned by agreement — nothing enforces it. | 標準ライブラリで追加インストールが不要。`make install` は評価者のマシンでも確実に動く。**コスト:** uv より遅く、マイナーバージョンの一致は口約束に依存する(強制する仕組みがない)。 |
| **B** | Much faster installs and a modern workflow.  **Cost:** a tool the evaluator may not have, so the README needs a documented fallback. | インストールが大幅に速く、現代的な運用。**コスト:** 評価者が持っていない可能性があり、README に代替手順を明記する必要がある。 |
| **C** | Tools stay isolated from the project environment.  **Cost:** two mechanisms to explain and to keep working instead of one. | ツールがプロジェクト環境から隔離される。**コスト:** 説明し保守する仕組みが 1 つではなく 2 つになる。 |
| **D** | A lock file pins exact versions for both of us and the evaluator, dev and runtime dependencies are separated, and `poetry build` produces the wheel and sdist §VI asks for without extra tooling.  **Cost:** a tool that must be installed before `make install` works, so the README needs an explicit setup line; and `poetry build` is driven by `pyproject.toml`, which currently names the project `a-maze-ing` and therefore does **not** produce `mazegen-*`. | lock ファイルで二人と評価者のバージョンが正確に一致し、dev 依存と runtime 依存が分離でき、`poetry build` が §VI の要求する wheel と sdist を追加設定なしで生成する。**コスト:** `make install` の前にツール自体のインストールが必要になるので、README に手順を明記する必要がある。また `poetry build` は `pyproject.toml` に従うため、現状の `name = "a-maze-ing"` では **`mazegen-*` を生成しない**。 |

**Options / 選択肢**

|             | EN                                                                   | JA                                                          |
| ----------- | -------------------------------------------------------------------- | ----------------------------------------------------------- |
| **A** | `python3 -m venv` + `pip install -r requirements.txt`.           | `python3 -m venv` + `pip install -r requirements.txt`。 |
| **B** | `uv` for speed, with a `venv` fallback documented in the README. | 速度重視で`uv`。README に `venv` の代替手順を明記。     |
| **C** | `pipx` for tools, `venv` for the project.                        | ツールは`pipx`、プロジェクトは `venv`。                 |
| **D** | Poetry — dependency management, virtualenv and build backend in one tool. | Poetry — 依存管理・仮想環境・ビルドバックエンドを 1 つのツールで。 |

> Decision: ~~A~~ → **superseded by D (Poetry)** on 2026-08-20.
> The original decision was `venv` + `pip`. javi proposed Poetry, implemented it, and so accepted it after review.
> **The record of that re-decision, with its reasons and its follow-ups, is
> [`03_poetry_switch.md`](03_poetry_switch.md).**
> / 当初の決定は `venv` + `pip`。javi が Poetry を提案・実装し、so がレビューのうえ受け入れた。
> 再決定の記録・理由・残作業は [`03_poetry_switch.md`](03_poetry_switch.md) にある。

### 2.2 🟡 Lint configuration / lint の設定

**EN** — `make lint` must run `flake8 .` and `mypy` with the exact flags in §III.2. Do we add a config file for
flake8? Do we aim for `make lint-strict` (`mypy --strict`) from day one or only at the end?
**JA** — `make lint` は §III.2 指定のフラグどおり `flake8 .` と `mypy` を実行する必要がある。
flake8 用の設定ファイルを置くか。`make lint-strict`(`mypy --strict`)は初日から目指すか、最後にやるか。

**How to think about it / 考え方**

**EN** — Type errors are cheap to fix while you are writing the function and expensive to fix in bulk two weeks
later, because by then the fix often means changing a signature that the other person already depends on.
Running the strict check from the start also front-loads the design questions ("what can this actually return?"),
which is the part the evaluator asks about.
**JA** — 型エラーは「その関数を書いている最中」なら安く直せるが、2 週間後にまとめて直すと高くつく。
その頃には修正が「相方が既に依存しているシグネチャの変更」を意味することが多いため。
最初から strict で回すと、設計上の問い(「この関数は結局何を返しうるのか」)が前倒しで出てくる。
評価者が突くのはまさにそこ。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Type errors surface while the function is being written, and signature questions get settled before the other side depends on them.  **Cost:** slower at the start, and `--strict` demands annotations in places that feel unnecessary early on. | 型エラーが関数を書いている最中に出る。シグネチャの疑問が、相手が依存する前に片づく。**コスト:** 序盤が遅い。`--strict` は、まだ不要に感じる場所にも注釈を要求する。 |
| **B** | Fast start, and the strict pass becomes one focused task.  **Cost:** that task lands in the finalisation milestone, where a forced signature change can ripple into the other person's finished code. | 序盤が速く、strict 化が 1 つの集中作業になる。**コスト:** その作業が仕上げのマイルストーンに来る。そこでシグネチャ変更が必要になると、相方の完成済みコードに波及する。 |
| **C** | No strict work at all — §III.2 marks it optional.  **Cost:** we give up the cheapest available check on a graded requirement (§III.1 type hints), and "we did not try" is a weak answer if asked. | strict 化をやらない。§III.2 は任意としている。**コスト:** 採点要件(§III.1 の型ヒント)に対する最も安い検査を捨てることになる。聞かれたときに「やっていません」は弱い答え。 |

**Options / 選択肢**

|             | EN                                                                                        | JA                                                                               |
| ----------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **A** | `mypy --strict` from day one; `lint-strict` is the real gate.                         | 初日から`mypy --strict`。`lint-strict` を本当の関門にする。                  |
| **B** | Subject flags only during development; attempt`--strict` at the finalisation milestone. | 開発中は subject 指定のフラグのみ。仕上げのマイルストーンで`--strict` に挑戦。 |
| **C** | Subject flags only; skip`lint-strict` entirely (it is optional).                        | subject 指定のフラグのみ。`lint-strict` は任意なのでやらない。                 |

> Decision:

### 2.3 🟡 Makefile ownership / Makefile の担当

**EN** — Who writes the `Makefile` (`install` / `run` / `debug` / `clean` / `lint` / optional `lint-strict`),
and when?
**JA** — `Makefile`(`install` / `run` / `debug` / `clean` / `lint` /(任意)`lint-strict`)は誰がいつ書くか。

**How to think about it / 考え方**

**EN** — The `Makefile` is the shared definition of "how to run this project", so it is worth having before there
is much to run: it removes every "which command did you use?" message. It is also the first thing an evaluator
types, which makes a broken rule an unusually expensive bug.
**JA** — `Makefile` は「このプロジェクトをどう動かすか」の共有定義なので、
動かすものが揃う前に存在している価値がある(「どのコマンドで動かした?」というやり取りが全部消える)。
評価者が最初に叩くのもこれなので、壊れたルールは異常に高くつくバグになる。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | `make run` exists before there is anything to run, so both of us always use the same commands.  **Cost:** placeholder rules fail until the code lands, and a failing rule can be mistaken for real breakage. | 動かすものが揃う前から `make run` が存在し、二人が常に同じコマンドを使う。**コスト:** コードが揃うまでダミーのルールは失敗する。その失敗を本物の故障と誤認しうる。 |
| **B** | One owner, one style, and it matches W20 (javi).  **Cost:** so is blocked on javi for `make lint` while writing the core, unless so runs the tools by hand in the meantime. | 担当が 1 人で様式が統一され、W20(javi)と一致する。**コスト:** so はコアを書いている間 `make lint` を javi 待ちになる。手でツールを叩く運用にしない限り。 |
| **C** | Written once, when it can be written properly.  **Cost:** until then each of us invents commands, and the "works on my machine" gap grows quietly. | きちんと書ける時点で一度だけ書く。**コスト:** それまで各自が独自のコマンドを使い、「自分の環境では動く」の差が静かに広がる。 |

**Options / 選択肢**

|             | EN                                                                     | JA                                                     |
| ----------- | ---------------------------------------------------------------------- | ------------------------------------------------------ |
| **A** | Written today with placeholder targets, filled in as the code appears. | 今日ダミーのターゲットで作り、コードができ次第埋める。 |
| **B** | Owned by whoever takes the infrastructure side (see Part 7).           | インフラ側の担当者が持つ(Part 7 参照)。                |
| **C** | Written at the first integration checkpoint.                           | 最初の統合チェックポイントで書く。                     |

> Decision:

### 2.4 🟡 `maze_analyzer.py` as the acceptance gate / 受け入れ判定としての `maze_analyzer.py`

**EN** — The provided script checks wall coherence and reports whether the maze is perfect or playable (§IV.5).
Do we run `--help` together now? Do we wire it into the `Makefile` or the tests?
**JA** — 配布スクリプトはウォールの整合性を検査し、迷路が完全迷路か遊べる盤面かを報告する(§IV.5)。
今この場で `--help` を一緒に実行するか。`Makefile` かテストに組み込むか。

**How to think about it / 考え方**

**EN** — This script is the closest thing we have to the Moulinette, so its options define "done" more precisely
than the subject prose does — for example §VIII mentions `--max-dead-ends 0`. Reading it **before** designing the
generator is much cheaper than discovering its expectations after the generator exists.
**JA** — このスクリプトは手元にある Moulinette に最も近いものなので、
そのオプションは subject の散文より正確に「完成」を定義している(§VIII に `--max-dead-ends 0` の言及がある)。
生成器を設計する**前**に読む方が、生成器ができてから期待値を知るよりずっと安い。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | The acceptance criterion becomes one command anyone can run, including at the defense.  **Cost:** a rule outside §III.2's required list — harmless, but it must not be confused with or replace `lint`. | 受け入れ基準が「誰でも叩ける 1 コマンド」になる。ディフェンスでも使える。**コスト:** §III.2 の必須ルール一覧にないルールが増える。無害だが `lint` と混同したり置き換えたりしないこと。 |
| **B** | The property is checked on every test run, so a regression is caught the day it appears.  **Cost:** the suite now depends on an external script we do not control, and it gets slower. | テストを回すたびに検査されるので、退行が出た日に捕まる。**コスト:** 自分たちが管理していない外部スクリプトにテストが依存し、実行が遅くなる。 |
| **C** | Zero setup.  **Cost:** we find out at checkpoints, so a generator that has been subtly wrong for a week costs a week to unwind. | 準備ゼロ。**コスト:** 発覚がチェックポイントになる。1 週間微妙に間違っていた生成器は、巻き戻しに 1 週間かかる。 |

**Options / 選択肢**

|             | EN                                                                                   | JA                                                            |
| ----------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| **A** | Read it now together; add a`make check` rule that runs it on the generated output. | 今一緒に読む。生成結果に対して実行する`make check` を追加。 |
| **B** | Read it now; call it from the test suite instead of the Makefile.                    | 今読む。Makefile ではなくテストから呼ぶ。                     |
| **C** | Use it manually before each integration checkpoint.                                  | 統合チェックポイントの前に手動で使う。                        |

> Decision:

---

## Part 3 — Core technical decisions / 中核の技術判断

> **EN** — Everything in this part is a **shared contract**. Whatever we decide goes into
> `Docs/implementation_plans/` as a file with signatures, before either of us writes a function body.
> **JA** — この Part はすべて**共有の契約**。決めた内容は、どちらかが関数本体を書く前に
> `Docs/implementation_plans/` にシグネチャ付きのファイルとして残す。

### 3.1 🔴 Maze data structure / 迷路のデータ構造

**EN** — **Decide this first — both sides depend on it.** How is the maze held in memory? Is the in-memory form
the same as the hex output form, or does the output layer convert?
**JA** — **最初に決める。両側がこれに依存する。** 迷路はメモリ上でどう保持するか。
メモリ上の形式は 16 進出力と同じか、出力層で変換するか。

**How to think about it / 考え方**

**EN** — The question behind the question is *who is the audience of this structure*. §VI says the reusable module
may expose a structure **different** from the output file, so we are free to pick whatever is easiest to reason
about internally and convert at the edge. A general principle: the internal representation should make the
**invariants** easy to hold (see 3.3), and the output format should be a function applied at the end, not a
constraint on the whole program.
**JA** — この問いの本質は「その構造の読者は誰か」。§VI は、再利用モジュールが公開する構造は出力ファイルと
**異なっていてよい**と明記している。つまり内部は考えやすい形を選び、端で変換してよい。
一般原則として、内部表現は**不変条件**(3.3 参照)を保ちやすい形にし、
出力形式は最後に適用する関数として扱う。プログラム全体を縛る制約にしない。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | The output digit *is* the stored value, so §IV.5 carries almost no conversion risk, and every geometric rule reads straight off the grid.  **Cost:** the shared wall exists twice, so correctness depends entirely on 3.3's single mutator holding — if anything else writes a wall, nothing catches it. | 出力の桁が格納値そのものなので、§IV.5 に変換リスクがほぼない。幾何のルールも構造をそのまま読める。**コスト:** 共有する壁が 2 か所に存在するため、正しさが 3.3 の単一変更経路に全面的に依存する。他の何かが壁を書けば、誰も気づけない。 |
| **B** | Readable per-cell access and an obvious home for per-cell state.  **Cost:** the double-storage problem is unchanged, and the output conversion comes back. | セル単位のアクセスが読みやすく、セルごとの状態の置き場が自明。**コスト:** 二重保持の問題は変わらず、出力のための変換が復活する。 |
| **C** | The invariant cannot be broken and loop counting is direct.  **Cost:** every geometric requirement — 3x3, the "42", rendering — needs the grid reconstructed each time. | 不変条件を破れず、ループ数を直接数えられる。**コスト:** 幾何の要件(3x3・「42」・描画)のたびにグリッドを組み直す必要がある。 |
| **D** | The encoder makes the internal/output coincidence a deliberate choice rather than an accident, and §VI explicitly permits the two to differ.  **Cost:** one more function that must stay in sync whenever either side changes. | エンコーダを置くことで、内部と出力の一致が「偶然」ではなく「設計上の選択」になる。§VI も両者が異なってよいと明記している。**コスト:** どちらかが変わるたび同期が必要な関数が 1 つ増える。 |

**Options / 選択肢**

|             | EN                                                                             | JA                                                               |
| ----------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| **A** | `list[list[int]]` — one 4-bit mask per cell, identical to the output digit. | `list[list[int]]` — 1 セル 4 ビットのマスク。出力の桁と同一。 |
| **B** | A`Cell` class holding four wall flags plus its coordinates.                  | 4 つの壁フラグと座標を持つ`Cell` クラス。                      |
| **C** | A graph: cells as nodes, open passages as edges (closest to the theory).       | グラフ:セルをノード、開いた通路をエッジとする(理論に最も近い)。  |
| **D** | Internal form of our choice + an explicit encoder to the hex form.             | 好きな内部形式 + 16 進形式への明示的なエンコーダ。               |

> Decision: A + D. ただし`Maze` クラスで包む。

### 3.2 🔴 Coordinate convention / 座標の規約

**EN** — The config uses `ENTRY=0,0` and `EXIT=19,14` as `(x, y)` with `WIDTH=20`, `HEIGHT=15`. Where is the
origin? Is `x` the column and `y` the row? Do we index `grid[y][x]` or `grid[x][y]`?
**JA** — 設定は `WIDTH=20` / `HEIGHT=15` に対し `ENTRY=0,0`、`EXIT=19,14` を `(x, y)` として使う。
原点はどこか。`x` は列で `y` は行か。添字は `grid[y][x]` か `grid[x][y]` か。

**How to think about it / 考え方**

**EN** — There is no "correct" convention, only a **consistent** one. The classic trap is that the config speaks
`(x, y)` while nested lists naturally read `[row][column]` = `[y][x]`, so the two orders coexist in the same
program. The usual defence is to write the rule down once, convert at the boundary (config parsing), and never
mix the two vocabularies inside the core. A named type alias such as `Coord = tuple[int, int]` documents the order
in the signature, so `mypy` and the reader see the same thing.
**JA** — 「正しい」規約はなく、「一貫した」規約があるだけ。典型的な罠は、
設定ファイルが `(x, y)` で話すのに、ネストしたリストは自然に `[行][列]` = `[y][x]` と読める点。
同じプログラム内に 2 つの順序が同居してしまう。
定石は、ルールを一度だけ文書化し、境界(設定パース)で変換し、コアの中では 2 つの語彙を混ぜないこと。
`Coord = tuple[int, int]` のような型エイリアスを作るとシグネチャに順序が残り、`mypy` と読み手が同じものを見る。

**Consequences / 帰結**

|             | EN                                                                                                                                                                                                                                              | JA                                                                                                                                                                     |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A** | Outer list = rows. Output (§IV.5), rendering and the 3x3 area scan all iterate rows, so they read straight off the structure. **Cost:** the config's `(x, y)` order is swapped when indexing, so the conversion must happen at the boundary and be documented. | 外側 = 行。出力(§IV.5)・描画・3x3 領域走査はどれも行を回すので、構造をそのまま読める。**コスト:** 設定の `(x, y)` と添字順が入れ替わるため、境界で変換し、それを文書化する必要がある。 |
| **B** | Outer list = columns, so `len(grid) == WIDTH`. Indexing matches the config literally. **Cost:** every row-oriented operation (output, rendering, area scan) reads transposed, and dimension checks are easy to write backwards. | 外側 = 列なので `len(grid) == WIDTH`。添字が設定と一致する。**コスト:** 行単位の処理(出力・描画・領域走査)はすべて転置して読むことになり、寸法検証を逆に書きやすい。 |
| **C** | One index formula, no ambiguity anywhere. **Cost:** every access goes through a helper, so nothing is readable without it. | 添字の式が 1 つだけで、曖昧さがどこにも残らない。**コスト:** すべてのアクセスがヘルパー経由になり、ヘルパーなしでは何も読めない。 |

**EN** — Note how this interacts with 3.1: since we wrap the grid in a `Maze` class, the order can be hidden behind
row-iteration accessors, and no caller on the output or rendering side ever sees it. That design decides how much
the cost above actually matters — a raw grid handed across the boundary pays it on every use.
**JA** — 3.1 との関係に注意。グリッドを `Maze` クラスで包むと決めているので、
順序は「行を返すアクセサ」の背後に隠せ、出力側・描画側の呼び出し元は一切それを見ない。
上のコストがどれだけ効くかは、その設計で決まる。生の配列を境界越しに渡す形にすると、使うたびにコストを払う。

**Options / 選択肢**

|             | EN                                                                  | JA                                                          |
| ----------- | ------------------------------------------------------------------- | ----------------------------------------------------------- |
| **A** | Origin top-left,`x` = column, `y` = row, stored `grid[y][x]`. | 原点は左上、`x` = 列、`y` = 行、格納は `grid[y][x]`。 |
| **B** | Same, but stored`grid[x][y]` to match the config order literally. | 同じだが、設定の順序に合わせて`grid[x][y]` で格納。       |
| **C** | A flat`list` with an index helper, no nesting at all.             | ネストせず、添字ヘルパー付きのフラットな`list`。          |

> Decision: **A** — origin top-left, `x` = column, `y` = row, stored `grid[y][x]`. Agreed with javi after
> reviewing the Consequences table: the output encoder (W13) and the renderer (W15) are both row-oriented, so
> storing rows first keeps the cost off javi's side. The config's `(x, y)` order is converted **once**, at parse
> time in W01 (so), and the core never sees the other order. `Maze` still keeps the grid private and exposes row
> iteration, so no caller indexes the raw list either way.
> / **A** — 原点は左上、`x` = 列、`y` = 行、`grid[y][x]` で格納。Consequences 表を見たうえで javi と合意。
> 出力エンコーダ(W13)と描画(W15)がどちらも行単位なので、行を先にすればコストが javi 側に落ちない。
> 設定の `(x, y)` は W01(so)のパース時に**一度だけ**変換し、コアはもう一方の順序を一切見ない。
> なお `Maze` はどちらにせよグリッドを private に保ち行アクセサを公開するので、生のリストを添字で触る呼び出し元はない。

### 3.3 🔴 Wall encoding and its invariant / ウォール符号化と不変条件

**EN** — §IV.5 fixes it: bit 0 = North, 1 = East, 2 = South, 3 = West; **1 means closed**. Do we both read `3` as
"south and west open"? Where do we enforce that two neighbours encode their shared wall identically?
**JA** — §IV.5 で固定:bit0=北、1=東、2=南、3=西。**1 が「閉じている」**。
`3` を「南と西が開いている」と二人とも読めるか。隣接 2 セルが共有する壁を同一に符号化することを、どこで保証するか。

**How to think about it / 考え方**

**EN** — The encoding itself is imposed by the subject, so the real decision is about the invariant. There are two
families of answer: make the invalid state **unrepresentable** (a single "open a passage" operation that always
updates both neighbours, so nothing else may touch walls), or allow free edits and **detect** breakage with a
validator. The first prevents the bug; the second finds it. They are not exclusive, and saying which one we rely
on is exactly the kind of design answer an evaluator is looking for.
**JA** — 符号化そのものは subject が決めているので、実際の判断は不変条件の方。
答えの系統は 2 つ。不正な状態を**表現できなくする**(「通路を開ける」操作を 1 つだけ用意し、
常に両隣を同時に更新する。それ以外は壁に触れない)か、自由に編集させて**バリデータで検出**するか。
前者はバグを防ぎ、後者はバグを見つける。排他ではない。
そして「どちらに頼っているか」を言えることが、評価者の求める設計上の答えそのもの。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | The invalid state becomes unrepresentable, which is the strongest possible answer at the defense.  **Cost:** every wall change must go through that one operation — including the "42" pattern (3.6) and the braiding step (3.4), which both mutate walls in bulk and will need to fit that shape. | 不正な状態が表現不能になる。ディフェンスで最も強い答え。**コスト:** すべての壁の変更がその 1 操作を通る必要がある。「42」(3.6)と braiding(3.4)は壁をまとめて変更するので、その形に収める設計が要る。 |
| **B** | Free editing keeps the generation code simple to write.  **Cost:** the invariant is only checked at the end, so a bug is discovered far from its cause. | 自由に編集でき、生成コードが書きやすい。**コスト:** 不変条件の確認が最後だけになり、バグが原因から遠い場所で発覚する。 |
| **C** | Prevention during construction plus a safety net in the tests.  **Cost:** slightly more code, and the validator can lull us into relaxing the discipline it was meant to back up. | 構築時の予防に加え、テストで安全網を張れる。**コスト:** コードがやや増え、「バリデータがあるから」と本来の規律が緩みやすい。 |

**Options / 選択肢**

|             | EN                                                                                        | JA                                                                  |
| ----------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **A** | Single`open_passage(a, b)` operation owns all wall mutation; nothing else writes walls. | 壁の変更は`open_passage(a, b)` 1 つだけが担う。他は壁を書かない。 |
| **B** | Free mutation + a validator run before output.                                            | 自由に変更 + 出力前にバリデータを実行。                             |
| **C** | Both: the operation for construction, the validator as a safety net in tests.             | 両方:構築は操作経由、バリデータはテストの安全網。                   |

> Decision: A

### 3.4 🔴 `PERFECT=True` vs the default playable board / `PERFECT=True` と既定の遊べる盤面

**EN** — **Careful: the default is `PERFECT=False`** (§IV.4), and that mode has *more* constraints, not fewer:
full connectivity, the four corners and the centre open, **at least two independent loops**, dead ends rare.
A perfect maze with one wall removed is explicitly **not** acceptable. One algorithm plus post-processing, or two
distinct paths?
**JA** — **注意:既定は `PERFECT=False`**(§IV.4)で、そちらの方が制約が**多い**。
完全連結、四隅と中央が通路、**独立した経路が 2 本以上**、行き止まりは稀。
「完全迷路の壁を 1 枚壊しただけ」は明示的に**不可**。
1 アルゴリズム + 後処理でいくか、2 経路を別々に実装するか。

**How to think about it / 考え方**

**EN** — The standard technique here is called **braiding**: generate a perfect maze, then remove walls to
eliminate dead ends, which creates loops. The subject's wording matters — one removed wall is not enough, so the
question is not *whether* to braid but *how much*, and how we measure the result (this is where
`maze_analyzer.py` earns its place). The alternative is an algorithm that produces loops natively. Whichever we
choose, note that the two modes share almost everything except the final step, so keeping them in one pipeline
with a switch usually costs less than maintaining two.
**JA** — ここでの定石は **braiding(編み込み)**:まず完全迷路を作り、その後で壁を取り除いて行き止まりを潰し、
ループを作る。subject の書き方が重要で、「1 枚壊すだけ」では不十分。
つまり問いは「braid するか否か」ではなく「**どれだけ**するか」、そして「結果をどう測るか」。
`maze_analyzer.py` が効いてくるのはここ。
もう一方の道は、最初からループを生むアルゴリズムを使うこと。
どちらにせよ、2 モードは最終段以外ほぼ共通なので、
スイッチ付きの 1 本のパイプラインにする方が、2 本維持するより安く済むことが多い。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | One pipeline and one algorithm to explain; `PERFECT=True` is simply the pipeline stopping early.  **Cost:** the braiding step must remove enough dead ends for §IV.4 (two independent loops, dead ends rare) without violating corridor width (3.7) — that tuning is the real work, and `maze_analyzer.py` is the only objective measure of it. | パイプラインが 1 本、説明するアルゴリズムも 1 つ。`PERFECT=True` は途中で止めるだけ。**コスト:** braiding が §IV.4(独立ループ 2 本以上、行き止まりは稀)を満たすまで行き止まりを潰しつつ、通路幅(3.7)を壊してはいけない。この調整が本体の作業で、客観的に測れるのは `maze_analyzer.py` だけ。 |
| **B** | Each mode can be specialised optimally.  **Cost:** two code paths to write, test and explain — twice the surface for a bug, in a one-month project. | 各モードを最適に特化できる。**コスト:** 書く・テストする・説明する経路が 2 本。1 か月のプロジェクトでバグの面積が倍になる。 |
| **C** | One parameter covers both modes and is elegant to describe.  **Cost:** "loop density" has to be defined precisely enough to guarantee §IV.4's *at least two independent loops*, which a density number does not give you by itself. | 1 つのパラメータで両モードを覆え、説明も綺麗。**コスト:** 「ループ密度」を、§IV.4 の*独立ループ 2 本以上*を保証できる精度で定義する必要がある。密度という数値だけではそれを保証しない。 |

**Options / 選択肢**

|             | EN                                                                           | JA                                                                    |
| ----------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **A** | Perfect maze generator + a braiding step applied when`PERFECT=False`.      | 完全迷路の生成器 +`PERFECT=False` のとき braiding 段を適用。        |
| **B** | Two separate generation paths, each specialised.                             | 2 つの独立した生成経路。それぞれ専用。                                |
| **C** | One generator with a "loop density" parameter;`PERFECT=True` is density 0. | 「ループ密度」パラメータ付きの単一生成器。`PERFECT=True` は密度 0。 |

> Decision: A

### 3.5 🔴 Generation algorithm and its justification / 生成アルゴリズムと選定理由

**EN** — The foreword names recursive backtracker, Prim and Kruskal. Which do we choose, and **why**? §VII requires
the justification in the README, so we must be able to state it in one paragraph.
**JA** — まえがきは再帰的バックトラッカー・Prim・Kruskal を挙げている。どれを選び、**なぜか**。
§VII は README にその理由を求めるので、一段落で言える必要がある。

**How to think about it / 考え方**

**EN** — All three produce a perfect maze, because all three build a **spanning tree** over the grid — that is why
the foreword mentions the connection. So the choice is not about correctness but about the *character* of the
result and the *shape* of the code: how long and winding the corridors are, how many dead ends appear, whether
recursion depth is a concern at large sizes, and how naturally the algorithm lets us reserve the "42" region.
Before choosing, each of us should be able to describe how the candidates differ — if not, that is a
`learning_log/` entry first, not a coin flip.
**JA** — 3 つともグリッド上の**全域木**を作るため、いずれも完全迷路になる(まえがきが全域木に言及するのはこのため)。
つまり選択は正しさの問題ではなく、結果の*性格*とコードの*形*の問題。
通路がどれだけ長く曲がりくねるか、行き止まりがどれだけ出るか、
大きなサイズで再帰の深さが問題になるか、「42」の領域を確保しやすいか。
選ぶ前に、二人とも候補の違いを説明できること。できないなら、それはコイン投げではなく `learning_log/` の項目。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Long winding corridors — it looks the most like a maze — and the algorithm is short.  **Cost:** it produces many dead ends, so 3.4's braiding step has more to remove; and recursion depth grows with WIDTH×HEIGHT unless written iteratively with an explicit stack. | 通路が長く曲がりくねり、最も「迷路らしい」見た目になる。アルゴリズムも短い。**コスト:** 行き止まりが多く出るため、3.4 の braiding が潰す量が増える。また明示的スタックで反復的に書かない限り、再帰の深さが WIDTH×HEIGHT に比例する。 |
| **B** | More branching, shorter corridors, and no recursion at all.  **Cost:** it needs a frontier structure, and its texture still leaves dead ends for braiding to clean up. | 分岐が多く通路が短く、再帰を使わない。**コスト:** フロンティア構造が必要で、テクスチャ上やはり行き止まりが残り braiding の仕事になる。 |
| **C** | Very uniform texture, and the disjoint-set structure it needs is the same tool that makes "is this still a tree?" trivial to answer.  **Cost:** that extra data structure is one more concept **both** of us must be able to explain (§IX). | テクスチャが非常に均一。必要になる素集合データ構造は、「まだ木か?」を自明に答える道具でもある。**コスト:** そのデータ構造は、**二人とも**説明できなければならない概念が 1 つ増えることを意味する(§IX)。 |
| **D** | Bonus credit under §VIII with no cost until we choose to add it.  **Cost:** the second algorithm must satisfy every constraint too — the reserved "42" region (3.6), corridor width (3.7), and §IV.4 — so it is rarely as cheap as it looks. | §VIII のボーナスを、追加すると決めるまで無コストで狙える。**コスト:** 2 つ目のアルゴリズムも全制約(3.6 の「42」領域、3.7 の通路幅、§IV.4)を満たす必要があり、見た目ほど安くならない。 |

**EN** — Constraint from 3.6 = A: the generator must be able to treat the reserved "42" cells as out of bounds, i.e. work on a non-rectangular region. Check each candidate against that before deciding.
**JA** — 3.6 = A による制約:生成器は「42」の確保セルを範囲外として扱える必要がある(= 長方形でない領域で動く)。決める前に各候補をこの条件で確認すること。

**Options / 選択肢**

|             | EN                                                                                              | JA                                                                                   |
| ----------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **A** | Recursive backtracker (DFS) — long winding corridors, few junctions, recursion depth to watch. | 再帰的バックトラッカー(DFS)— 長く曲がりくねる通路、分岐は少なめ、再帰の深さに注意。 |
| **B** | Prim — grows from a frontier, more branching, shorter corridors.                               | Prim — フロンティアから成長。分岐が多く通路は短め。                                 |
| **C** | Kruskal — edges merged via a disjoint-set structure, very uniform texture.                     | Kruskal — 素集合データ構造で辺を併合。テクスチャが非常に均一。                      |
| **D** | One now, a second later as the §VIII bonus ("support multiple algorithms").                    | まず 1 つ。§VIII のボーナス(複数アルゴリズム対応)で後から追加。                     |

> Decision: **A — recursive backtracker, written iteratively with an explicit stack.**
> Since the default mode is `PERFECT=False`, braiding has to remove almost every dead end, so the algorithm that
> starts with the fewest of them leaves the least work. The recursion-depth caveat is not a reason against it:
> writing it iteratively removes the problem entirely, and the explicit stack is the same one the trace in
> `Docs/learning_log/maze-generation-algorithms.md` §2.2 shows.
> **This rests on a figure we have not measured yet** (~10% dead ends vs ~30%), so it is provisional in that one
> respect — §5.4 of the reference gives the procedure, and the measurement becomes the §VII justification.
> Cheap to revisit: 3.1 and 5.1 keep the algorithm inside `MazeGenerator`, so replacing it would not reach javi's
> side (W13 / W15). Kruskal is rejected as a *generator*, but **union-find stays under consideration as a tool for
> validation (W10)** — counting independent loops after braiding. See Q2.
> / **A — 再帰的バックトラッカー。ただし明示的スタックによる反復版で書く。**
> 既定モードが `PERFECT=False` である以上 braiding が行き止まりをほぼ全部潰す必要があり、
> 開始時の行き止まりが最も少ないものが残作業を最小にする。
> 再帰の深さは反対理由にならない。反復版にすれば完全に消え、そのスタックは
> `Docs/learning_log/maze-generation-algorithms.md` §2.2 のトレースが示すものと同じ。
> **この判断は未実測の数値(行き止まり 約 1 割 対 約 3 割)に乗っている**ので、その一点において暫定。
> 解説書 §5.4 に実測手順があり、その計測結果がそのまま §VII の選定理由になる。
> 覆っても差し替えは安い。3.1 と 5.1 によりアルゴリズムは `MazeGenerator` の内側にあり、
> javi 側(W13 / W15)には届かない。
> Kruskal は**生成器としては**却下するが、**union-find は検証(W10)の道具として引き続き検討する** —
> braiding 後の独立ループ数の計数。Q2 参照。

### 3.6 🔴 The "42" pattern / 「42」パターン

**EN** — The pattern must be visible, drawn by **fully closed cells** (§IV.4). Reserved before generation or
carved after? How does it coexist with connectivity, corridor width ≤ 2 and the dead-end rule? Below what size do
we skip it and print an error?
**JA** — パターンは**完全に閉じたセル**で描かれ、目に見えなければならない(§IV.4)。
生成前に確保するか、生成後に彫るか。連結性・通路幅 ≤ 2・行き止まりルールとどう両立するか。
どのサイズ未満で省略し、エラーを出すか。

**How to think about it / 考え方**

**EN** — Note what "fully closed cells" means: those cells are **removed from the walkable area**, so the pattern is
a hole in the graph, not a decoration. That is why it interacts with every other rule — connectivity must hold
*around* it, and the subject explicitly exempts the pattern from the isolation and dead-end rules. Generally,
reserving the region **before** generation is the more predictable approach, because the generator then simply
never carves there; carving afterwards means repairing whatever you just broke. Either way this belongs to
whoever owns generation — it is not a rendering feature.
**JA** — 「完全に閉じたセル」の意味に注意。それらのセルは**歩ける領域から取り除かれる**ので、
このパターンは装飾ではなくグラフに空いた穴。だから他のすべてのルールと干渉する。
連結性はその*周り*で保たれねばならず、subject はこのパターンを孤立・行き止まりのルールから明示的に除外している。
一般に、生成の**前**に領域を確保する方が予測可能。生成器がそこを掘らないだけで済むため。
後から彫る場合は、たった今壊したものを修復する作業になる。
いずれにせよこれは生成担当の仕事であり、描画の機能ではない。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | The generator never carves into the pattern, so nothing has to be repaired and connectivity holds around it by construction.  **Cost:** the generation algorithm must accept out-of-bounds cells, which constrains the choice in 3.5 — it has to work on a non-rectangular region. | 生成器がパターンを掘らないので修復が不要で、連結性はその周りで構造的に保たれる。**コスト:** 生成アルゴリズムが範囲外セルを扱える必要があり、3.5 の選択を制約する(長方形でない領域で動くこと)。 |
| **B** | Generation stays a plain rectangle, which keeps the algorithm textbook-shaped.  **Cost:** closing cells afterwards can disconnect the maze, and the repair may itself break corridor width or the dead-end rule. | 生成が単純な長方形のままで、アルゴリズムが教科書どおりの形を保てる。**コスト:** 後からセルを閉じると迷路が分断されうる。修復自体が通路幅や行き止まりのルールを壊すこともある。 |
| **C** | Prevention plus proof that the pattern survived generation.  **Cost:** a validator for something that cannot happen — cheap, but still one more thing to maintain and explain. | 予防に加え、パターンが生成後も残っていることを証明できる。**コスト:** 起きないはずのことを検査するバリデータ。安いが、保守し説明する対象が 1 つ増える。 |

**Options / 選択肢**

|             | EN                                                                               | JA                                                     |
| ----------- | -------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **A** | Reserve the cells before generation; the generator treats them as out of bounds. | 生成前にセルを確保。生成器はそこを範囲外として扱う。   |
| **B** | Generate first, then close the pattern cells and repair connectivity.            | 先に生成し、その後パターンのセルを閉じて連結性を修復。 |
| **C** | Reserve before generation, and validate afterwards that the pattern survived.    | 生成前に確保し、生成後にパターンが残っているか検証。   |

> Decision: A

### 3.7 🟡 Corridor width and open areas / 通路幅と開放領域

**EN** — No open area wider than 2 cells; 2x3 and 3x2 fine, **3x3 not** (§IV.4). Guaranteed by construction, or
rejected by a validator and retried? Same question for "four corners and centre open" in the default mode.
**JA** — 幅 2 セルを超える開放領域は禁止。2x3・3x2 は可、**3x3 は不可**(§IV.4)。
構造的に保証するか、バリデータが弾いて再試行するか。既定モードの「四隅と中央が通路」も同じ問い。

**How to think about it / 考え方**

**EN** — This is the classic **generate-and-test vs correct-by-construction** trade-off. Generate-and-test is
easy to write and easy to explain, but if the constraint is often violated the retry loop can become slow or, in
the worst case, never terminate — so it needs a bounded number of attempts and a clear failure message.
Correct-by-construction is faster and always terminates, but the constraint has to be threaded through the
generation logic, which makes that logic harder to read. Note that a validator is worth writing in either case,
because it is also the thing that proves the property in a test.
**JA** — これは典型的な **generate-and-test 対 correct-by-construction** のトレードオフ。
generate-and-test は書きやすく説明しやすいが、制約違反が頻発すると再試行ループが遅くなり、
最悪の場合終わらない。だから試行回数の上限と明確な失敗メッセージが要る。
correct-by-construction は速く必ず終わるが、制約を生成ロジックに織り込むことになり、そのロジックが読みにくくなる。
なお、どちらを選んでもバリデータは書く価値がある。テストでその性質を証明するのもバリデータだから。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Always terminates, wastes no work, and the constraint is provably held.  **Cost:** the rule is threaded through the generation logic, making the hardest part of the project harder to read and to explain at the defense. | 必ず終了し、無駄な計算がなく、制約が構造的に保証される。**コスト:** 制約が生成ロジックに織り込まれ、プロジェクト最難所の可読性と説明しやすさが落ちる。 |
| **B** | Simple to write and simple to explain, and the validator doubles as the test.  **Cost:** if violations are common the retry loop is slow or non-terminating, so it needs an attempt limit and a clear failure message (§IV.2). | 書きやすく説明しやすい。バリデータがそのままテストになる。**コスト:** 違反が頻発すると再試行ループが遅くなるか終わらない。試行上限と明確な失敗メッセージ(§IV.2)が必須になる。 |
| **C** | Generation stays simple and the fix is local.  **Cost:** closing a wall can break connectivity or create a dead end, so the repair must itself be re-validated — a fix that needs a fix. | 生成が単純なままで、修正が局所的。**コスト:** 壁を閉じると連結性を壊したり行き止まりを作ったりするので、修復自体を再検証する必要がある。修正のための修正が生まれる。 |

**Options / 選択肢**

|             | EN                                                                          | JA                                                               |
| ----------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **A** | Correct by construction: the generator can never create a 3x3 opening.      | 構造的保証:生成器が 3x3 の開放を作れないようにする。             |
| **B** | Generate and validate; retry up to N times, then fail with a clear message. | 生成して検証。N 回まで再試行し、超えたら明確なメッセージで失敗。 |
| **C** | Post-process: detect wide areas and close a wall to break them.             | 後処理:広い領域を検出し、壁を 1 枚閉じて崩す。                   |

> Decision:

### 3.8 🟡 Shortest path / 最短経路

**EN** — The output needs the shortest valid path as a string of `N`/`E`/`S`/`W` (§IV.5). Which algorithm, and why
is it the shortest? Does the solver belong to the engine or the output side — does `MazeGenerator` expose a
solution (§VI says it must expose at least one)? What if no path exists?
**JA** — 出力には最短の妥当な経路を `N`/`E`/`S`/`W` の文字列で書く(§IV.5)。
どのアルゴリズムで、なぜ最短と言えるか。ソルバはエンジン側か出力側か
(§VI は最低ひとつの解へのアクセスを要求している)。経路がない場合はどうするか。

**How to think about it / 考え方**

**EN** — Every passage costs the same, so this is an unweighted shortest-path problem — the standard answer is a
breadth-first search, and the reason it is *provably* shortest is that BFS visits cells in non-decreasing order of
distance from the start. A depth-first search finds *a* path, not the shortest one, which is a common and easily
caught mistake. Note the two modes differ here: with `PERFECT=True` there is only one path anyway, so the property
only really bites in the default mode. Ownership: §VI forces the reusable module to expose a solution, which
argues for the solver living on the engine side.
**JA** — どの通路もコストが同じなので、これは重みなし最短経路問題。標準的な答えは幅優先探索であり、
それが*証明として*最短である理由は、BFS が開始点からの距離の非減少順にセルを訪れるから。
深さ優先探索は「ある経路」を見つけるが最短ではない。よくある、そして見つけやすい間違い。
なお 2 モードで事情が違う:`PERFECT=True` ではそもそも経路が 1 本しかないので、
この性質が効くのは既定モードの方。
担当については、§VI が再利用モジュールに解の公開を義務づけている。ソルバをエンジン側に置く論拠になる。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | §VI's "expose at least one solution" is satisfied directly, and the future project gets the solver for free.  **Cost:** more algorithmic work on so's side, which 7.2 already flagged as the heavier one. | §VI の「最低ひとつの解を公開する」を直接満たし、将来のプロジェクトはソルバをそのまま得る。**コスト:** so 側のアルゴリズム作業が増える。7.2 で既に重い側と指摘した方。 |
| **B** | Balances the load — javi gets genuine algorithmic work rather than only glue.  **Cost:** the reusable module still has to expose a solution for §VI, so either the engine duplicates it or the package depends on the app side, which is backwards. | 負荷が釣り合い、javi が接着作業だけでなく本物のアルゴリズム作業を持てる。**コスト:** §VI のために再利用モジュールも解を公開しなければならず、エンジンが重複実装するか、パッケージがアプリ側に依存する(依存方向が逆)ことになる。 |
| **C** | Clean separation: the engine computes, the output layer formats the `NESW` string.  **Cost:** one more interface to agree on and keep in sync between the two of us. | 役割が綺麗に分かれる。エンジンが計算し、出力層が `NESW` 文字列に整形する。**コスト:** 二人で合意し同期し続けるインターフェースが 1 つ増える。 |

**Options / 選択肢**

|             | EN                                                                          | JA                                                  |
| ----------- | --------------------------------------------------------------------------- | --------------------------------------------------- |
| **A** | BFS in the engine;`MazeGenerator` exposes the path.                       | エンジン内で BFS。`MazeGenerator` が経路を公開。  |
| **B** | BFS in the output layer; the engine only exposes the structure.             | 出力層で BFS。エンジンは構造だけ公開。              |
| **C** | Engine exposes a generic "solve" hook; the output layer formats the string. | エンジンは汎用の solve を公開。文字列整形は出力層。 |

> Decision:

### 3.9 🔴 Config keys and error policy / 設定キーとエラー方針

**EN** — Six mandatory keys, `KEY=VALUE` per line, `#` comments (§IV.3). Which **extra** keys, with exactly what
names? And §IV.2: the program must **never crash unexpectedly** — which exceptions, who catches, what message,
what exit code?
**JA** — 必須 6 キー、1 行 1 つの `KEY=VALUE`、`#` コメント(§IV.3)。
**追加**キーは何を、正確にどんな名前で足すか。
そして §IV.2:**予期せずクラッシュしてはならない** — どの例外を、誰が捕まえ、どんなメッセージで、どの終了コードか。

**How to think about it / 考え方**

**EN** — Agree the spelling of extra keys **now**: `SEED` vs `RANDOM_SEED` is the kind of mismatch that only shows
up when the two halves meet. For errors, the usual shape is: low-level code raises a **specific** exception with a
precise message, and exactly **one** place near the entry point catches it and turns it into a user-facing line.
Catching everywhere produces messages nobody can trace; catching nowhere produces the traceback §IV.2 forbids.
Defining our own exception type is what lets the top-level handler distinguish "the user's config is wrong" from
"our code has a bug" — and those two deserve different messages.
**JA** — 追加キーの綴りは**今**合わせる。`SEED` と `RANDOM_SEED` の食い違いは、両半分が出会った瞬間にだけ表面化する類。
エラーについての定石は、低レベルのコードが**具体的な**例外を正確なメッセージ付きで送出し、
エントリポイント付近の**ただ 1 か所**がそれを捕まえてユーザー向けの 1 行に変換する形。
あちこちで捕まえると誰も追えないメッセージになり、どこでも捕まえないと §IV.2 が禁じるトレースバックが出る。
自前の例外型を定義しておくと、最上位のハンドラが「ユーザーの設定が不正」と「自分たちのコードのバグ」を区別できる。
この 2 つは違うメッセージに値する。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | The top-level handler can tell "the user's config is wrong" from "our code has a bug", and those deserve different messages — which is what §IV.2 is really asking for.  **Cost:** an exception module both of us import and must keep consistent; new error types have to be agreed rather than invented on the spot. | 最上位のハンドラが「ユーザーの設定が不正」と「自分たちのコードのバグ」を区別できる。この 2 つは違うメッセージに値し、§IV.2 が本当に求めているのはそこ。**コスト:** 二人が import し、一貫性を保つ例外モジュールが必要。新しい例外型はその場で作らず合意が要る。 |
| **B** | No new types to define, and the built-ins are familiar to any reader.  **Cost:** the handler cannot distinguish our errors from a genuine bug, so we either print a config message for a real crash or leak a traceback. | 新しい型を定義せずに済み、組み込み例外は誰にでも馴染みがある。**コスト:** ハンドラが自分たちのエラーと本物のバグを区別できず、本当のクラッシュに設定エラーの文言を出すか、トレースバックを漏らすかになる。 |
| **C** | All problems in a config are reported at once, which is friendlier when several are wrong.  **Cost:** every caller must check the result, and Python that returns errors instead of raising is unusual enough to need explaining at the defense. | 設定の問題を一度にまとめて報告でき、複数間違っているときに親切。**コスト:** 呼び出し側が毎回結果を検査する必要があり、送出せず返す Python は珍しいのでディフェンスで説明を求められる。 |

**Options / 選択肢**

|             | EN                                                                                          | JA                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **A** | Custom`ConfigError` / `MazeError` types; one handler in `a_maze_ing.py`; exit code 1. | 自前の`ConfigError` / `MazeError`。ハンドラは `a_maze_ing.py` に 1 つ。終了コード 1。 |
| **B** | Built-in`ValueError` / `OSError` only; same single handler.                             | 組み込みの`ValueError` / `OSError` のみ。ハンドラは同じく 1 つ。                        |
| **C** | Parser returns a result object with an error list instead of raising.                       | パーサは送出せず、エラー一覧を持つ結果オブジェクトを返す。                                  |

> Decision: A

### 3.10 🟡 Seed and reproducibility / シードと再現性

**EN** — Reproducibility via a seed is mandatory (§IV.4). A local `random.Random(seed)` instance or the global
`random` module? What when the config has no seed?
**JA** — シードによる再現性は必須(§IV.4)。`random.Random(seed)` のインスタンスか、グローバルの `random` か。
設定にシードがない場合はどうするか。

**How to think about it / 考え方**

**EN** — The global `random` module is shared state: anything else that touches it — including a test running
earlier in the same process — changes your results, which is exactly what "reproducible" is supposed to exclude.
A local instance keeps the randomness inside the object that owns it, which also makes the generator safe to
instantiate twice. When no seed is given, generating one and **printing it** costs one line and turns "I saw a
weird maze once" into a reproducible bug report — a habit that pays off during the defense.
**JA** — グローバルの `random` は共有状態。同じプロセス内で先に走ったテストを含め、
それに触れる何かが結果を変えてしまう。「再現可能」が排除したいのはまさにそれ。
ローカルなインスタンスなら乱数はそれを持つオブジェクトの中に閉じ、生成器を 2 個作っても安全になる。
シードが与えられていないとき、生成して**表示する**のは 1 行の手間で、
「変な迷路を一度見た」を再現可能なバグ報告に変える。ディフェンスで効いてくる習慣。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Every run is reproducible, including the surprising ones — a weird maze becomes a bug report.  **Cost:** output varies between runs, so any test comparing raw stdout has to account for the printed seed. | すべての実行が再現可能になる。「変な迷路」がバグ報告に変わる。**コスト:** 実行ごとに出力が変わるので、標準出力を比較するテストは表示されたシードを考慮する必要がある。 |
| **B** | Runs are identical by default, which makes demos and tests predictable.  **Cost:** we keep looking at the same maze, so a bug that only appears for other seeds stays hidden until late. | 既定で毎回同じ結果になり、デモとテストが予測可能。**コスト:** 同じ迷路ばかり見ることになり、他のシードでだけ出るバグが終盤まで隠れる。 |
| **C** | Shortest to write.  **Cost:** shared global state — any other code, or a test that ran earlier in the same process, changes our output, which is exactly what §IV.4's reproducibility is meant to rule out. | 書く量が最も少ない。**コスト:** 共有のグローバル状態になる。他のコードや同一プロセスで先に走ったテストが出力を変えてしまい、§IV.4 の再現性が排除したいものそのものになる。 |

**Options / 選択肢**

|             | EN                                                                                           | JA                                                                   |
| ----------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **A** | `random.Random(seed)` instance held by the generator; auto-generate and print when absent. | 生成器が`random.Random(seed)` を保持。未指定なら自動生成して表示。 |
| **B** | Same instance, but absent seed means a fixed default so runs are always identical.           | 同じくインスタンス保持。未指定時は固定値にして常に同一の結果。       |
| **C** | Global`random.seed()` for simplicity.                                                      | 簡潔さを取ってグローバルの`random.seed()`。                        |

> Decision:

---

## Part 4 — Display / 表示

### 4.1 🔴 Terminal ASCII or MLX / ターミナル ASCII か MLX か

**EN** — §V allows either. Whichever we pick, the required interactions are the same: regenerate, show/hide the
shortest path, change wall colours (optionally colour the "42").
**JA** — §V はどちらでもよいとしている。どちらを選んでも必須の操作は同じ:
再生成、最短経路の表示/非表示、壁の色変更(任意で「42」の着色)。

**How to think about it / 考え方**

**EN** — The trade is portability against impressiveness. A terminal renderer needs no installation, runs
identically on both our machines and on the evaluator's, and ANSI escape codes are enough for colours. MLX looks
much better in a demo but adds an install step, an event loop, and a class of bug ("nothing appears") that has
nothing to do with mazes. A common compromise is to build the terminal renderer first — it is also the fastest
way to *debug the generator*, since you can see the maze — and treat MLX as an upgrade if time allows.
**JA** — 天秤にかかるのは可搬性と見栄え。
ターミナル描画はインストール不要で、二人のマシンでも評価者のマシンでも同じように動き、色は ANSI エスケープで足りる。
MLX はデモでの見栄えが大きく上だが、インストール手順・イベントループ・
そして迷路とは無関係なバグの類(「何も表示されない」)が増える。
よくある折衷は、まずターミナル描画を作ること。迷路が目で見えるので**生成器のデバッグ**にも最速。
そのうえで、時間が許せば MLX を上積みとして扱う。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Runs identically on both our machines and the evaluator's, needs no install step, and it is the fastest way to debug the generator because the maze is visible.  **Cost:** a less impressive demo, §VIII's animation bonus is harder to reach, and the "42" has to be readable in characters alone (see 4.3). | 二人のマシンでも評価者のマシンでも同じように動き、インストール手順が不要。迷路が目で見えるので生成器のデバッグにも最速。**コスト:** デモの見栄えが落ち、§VIII のアニメーションボーナスが遠のく。「42」を文字だけで読ませる必要がある(4.3 参照)。 |
| **B** | Keeps the safe option while leaving the impressive one open.  **Cost:** two renderers to maintain if we finish, and the standing temptation to start MLX before the core is done. | 安全な選択肢を確保しつつ、見栄えの良い方も残せる。**コスト:** 完成すれば描画を 2 つ保守することになり、コアが終わる前に MLX に手を出す誘惑が常にある。 |
| **C** | The best-looking demo, and the subject shows it as a first-class option.  **Cost:** an install step on both machines, an event loop, and a class of bug that has nothing to do with mazes. | デモの見栄えが最良で、subject も正式な選択肢として示している。**コスト:** 両マシンでのインストール手順、イベントループ、そして迷路と無関係なバグの一群。 |

**Options / 選択肢**

|             | EN                                        | JA                                 |
| ----------- | ----------------------------------------- | ---------------------------------- |
| **A** | Terminal only.                            | ターミナルのみ。                   |
| **B** | Terminal first, MLX later if time allows. | まずターミナル、時間が許せば MLX。 |
| **C** | MLX only.                                 | MLX のみ。                         |

> Decision: A

### 4.2 🟡 MLX per OS / OS ごとの MLX

**EN** — If we choose MLX: `mlx-2.2.tgz` contains a `ubuntu/` and a `fedora/` wheel plus the source. Do both
machines have a matching wheel? What is the fallback if one of us cannot run it?
**JA** — MLX を選ぶ場合:`mlx-2.2.tgz` には `ubuntu/` と `fedora/` の wheel、それにソースが入っている。
二人のマシンに合う wheel はあるか。片方が動かせない場合の代替は何か。

**How to think about it / 考え方**

**EN** — A graphical dependency that only one of us can run quietly breaks the §IX requirement that **both** of us
can demo and modify the project. It also affects `requirements.txt` and `make install`: a wheel shipped inside the
repository is installed differently from a package fetched from PyPI, and the README must say which.
**JA** — 片方しか動かせないグラフィック依存は、
「**二人とも**デモし修正できること」という §IX の要求を静かに壊す。
`requirements.txt` と `make install` にも影響する。
リポジトリ同梱の wheel は PyPI から取るパッケージとインストール方法が違うので、README にどちらかを書く必要がある。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Both of us can demo either renderer, which satisfies §IX for both.  **Cost:** two renderers to keep working, plus MLX install steps in the README and in `make install`. | 二人ともどちらの描画でもデモできる。§IX を両者で満たせる。**コスト:** 描画を 2 つ保守することになり、README と `make install` に MLX の手順が加わる。 |
| **B** | Only one machine needs the graphical dependency.  **Cost:** the other cannot demo or debug that half — the §IX risk in a different shape. | グラフィック依存を入れるマシンが 1 台で済む。**コスト:** もう一方はその半分をデモもデバッグもできない。§IX のリスクが形を変えて残る。 |
| **C** | No graphical dependency at all, and `requirements.txt` stays minimal.  **Cost:** we forgo the more impressive demo, and §VIII's animation bonus becomes harder to reach. | グラフィック依存が一切なく、`requirements.txt` が最小のままになる。**コスト:** 見栄えの良いデモを諦めることになり、§VIII のアニメーションボーナスが遠のく。 |

**EN** — Note: 4.1 was decided as A (terminal only), which settles this item as **C** unless we revisit 4.1.
**JA** — 注:4.1 は A(ターミナルのみ)で決定済み。4.1 を再検討しない限り、この項目は **C** で確定する。

**Options / 選択肢**

|             | EN                                                                         | JA                                                            |
| ----------- | -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **A** | Both install MLX; terminal renderer kept as the guaranteed fallback.       | 二人とも MLX を入れる。ターミナル描画を確実な代替として残す。 |
| **B** | Only the display owner installs MLX; the other demos the terminal version. | 表示担当だけ MLX を入れる。もう一方はターミナル版でデモ。     |
| **C** | Skip MLX entirely (follows from 4.1 option A).                             | MLX を使わない(4.1 の A を選んだ場合はこれ)。                 |

> Decision:

### 4.3 🟡 Rendering and the "42" / 描画と「42」

**EN** — The "42" must be **visible in the rendering**. How many characters or pixels per cell, and how are walls
drawn between cells?
**JA** — 「42」は**描画上で見えなければならない**。1 セルを何文字/何ピクセルで描き、セル間の壁をどう描くか。

**How to think about it / 考え方**

**EN** — A grid of cells cannot be drawn one character per cell if walls also need to be visible, because the wall
lives *between* two cells and needs its own space — the usual answer is a cell plus its north and west walls,
giving a 2x2 or 3x3 character block per cell. The choice is not cosmetic: it decides whether a correct maze
*looks* correct, and whether the "42" reads as "42". Since the pattern is produced by the generator and judged by
eye in the renderer, both owners should agree on this together rather than in sequence.
**JA** — 壁も見せる必要がある以上、セルのグリッドを 1 セル 1 文字では描けない。
壁はセルとセルの*間*にあり、自分の場所を必要とするから。
定石は「セル + その北と西の壁」を 1 単位として、1 セルあたり 2x2 か 3x3 の文字ブロックにすること。
この選択は化粧ではない。正しい迷路が正しく*見える*かどうか、
そして「42」が「42」と読めるかどうかを決める。
パターンは生成器が作り、判定は描画側の目で行われるので、
両担当が順番にではなく一緒に合意すべき項目。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Compact, so a 20x15 maze fits comfortably in any terminal.  **Cost:** walls and cells share little space, so the "42" is only readable at larger sizes — worth testing early against §IV.4's minimum-size rule. | コンパクトで、20x15 の迷路がどの端末にも収まる。**コスト:** 壁とセルに割ける空間が少なく、「42」が読めるのは大きいサイズのみ。§IV.4 の下限サイズ規定と併せて早めに実験する価値がある。 |
| **B** | The clearest reading of walls, entry, exit and path.  **Cost:** a 20x15 maze becomes 60x45 characters, and §IV.3 lets the config ask for larger — at which point it stops fitting a terminal window. | 壁・入口・出口・経路が最も読みやすい。**コスト:** 20x15 が 60x45 文字になる。§IV.3 は設定でさらに大きくできるので、その時点で端末に収まらなくなる。 |
| **C** | Strongest contrast, so the "42" and the solution path stand out immediately.  **Cost:** block glyphs and colours depend on the terminal, so it may not look the same on the evaluator's machine as on ours. | コントラストが最も強く、「42」と解の経路が一目で分かる。**コスト:** ブロック文字と色は端末依存なので、評価者のマシンで自分たちと同じに見えるとは限らない。 |

**Options / 選択肢**

|             | EN                                                                                   | JA                                                                        |
| ----------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| **A** | 2 characters per cell (cell + its north/west walls).                                 | 1 セル 2 文字(セル + 北/西の壁)。                                         |
| **B** | 3x3 character block per cell — clearest, but large mazes stop fitting the terminal. | 1 セル 3x3 文字ブロック — 最も見やすいが、大きい迷路が端末に収まらない。 |
| **C** | Block characters / colour fills instead of line drawing.                             | 線ではなくブロック文字や色の塗りで表現。                                  |

> Decision:

---

## Part 5 — Reusable package and licence / 再利用パッケージとライセンス

### 5.1 🟡 `MazeGenerator` public API / `MazeGenerator` の公開 API

**EN** — §VI: generation must live in **one class inside a standalone module**, importable by a future project.
What is its public surface? What stays private?
**JA** — §VI:生成処理は**スタンドアロンモジュール内の単一クラス**に置き、将来のプロジェクトから import できること。
公開する面は何か。何を private に留めるか。

**How to think about it / 考え方**

**EN** — A public API is a promise to a project that does not exist yet, and every promise is something we can no
longer change freely — so the useful instinct is to expose as little as possible. §VI names the minimum:
instantiate, pass parameters (size, seed), read the structure, read at least one solution. A method the caller
does not need is a method we will have to keep working. In Python the convention that marks the boundary is the
leading underscore, and it is worth applying deliberately rather than by accident.
**JA** — 公開 API は「まだ存在しないプロジェクト」への約束であり、
約束はすべて「もう自由に変えられないもの」になる。だから有用な直感は「できるだけ公開しない」。
§VI が最低限を挙げている:インスタンス化、パラメータ(サイズ・シード)、構造の読み取り、最低ひとつの解の読み取り。
呼び出し側が必要としないメソッドは、こちらが動かし続ける義務を負うだけのメソッド。
Python でその境界を示す慣習は先頭のアンダースコアで、
偶然そうなるのではなく意図して使う価値がある。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | A small surface is a small promise: §VI's four requirements are met and nothing else has to keep working.  **Cost:** the future project may need something we did not expose, and adding it later means a new version. | 小さな公開面は小さな約束。§VI の 4 要件を満たし、それ以外を動かし続ける義務が生じない。**コスト:** 将来のプロジェクトが公開していないものを必要とする可能性があり、後から足すと新バージョンになる。 |
| **B** | Anticipates reuse (algorithm choice, callbacks) and lines up with §VIII's multi-algorithm bonus.  **Cost:** every hook is a promise we must document and keep, and speculative APIs are usually the wrong shape. | 再利用(アルゴリズム選択、コールバック)を見越せ、§VIII の複数アルゴリズムボーナスと噛み合う。**コスト:** フックの数だけ、文書化し保守する約束が増える。しかも投機的な API はたいてい形を外す。 |
| **C** | The API ends up matching what the app genuinely calls, with no speculation.  **Cost:** the package cannot be built or rehearsed until late, and §VI's clean-venv rebuild is a graded step that should not be attempted for the first time at the end (see 5.2, 8.2). | アプリが実際に呼ぶものだけの API になり、投機がゼロ。**コスト:** パッケージのビルドとリハーサルが終盤まで出来ない。§VI のクリーン環境での再ビルドは採点工程であり、最後に初挑戦すべきではない(5.2、8.2 参照)。 |

**Options / 選択肢**

|             | EN                                                                                            | JA                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **A** | Minimal: constructor +`generate()` + `grid` + `solution`. Everything else `_private`. | 最小:コンストラクタ +`generate()` + `grid` + `solution`。他はすべて `_private`。 |
| **B** | Minimal plus hooks for future reuse (algorithm choice, callbacks).                            | 最小 + 将来の再利用向けフック(アルゴリズム選択、コールバック)。                          |
| **C** | Decide the API only after the engine works, from what the app actually calls.                 | エンジン完成後、アプリが実際に呼んでいるものから API を決める。                          |

> Decision:

### 5.2 🟡 Build tooling / ビルド方法

**EN** — The `mazegen-*` artifact must sit at the repo root, and everything needed to **rebuild it from source**
must be committed — we will be asked to do exactly that during the evaluation, in a clean virtualenv. Which build
backend? Who owns `pyproject.toml`? Who rehearses the rebuild, and when?
**JA** — `mazegen-*` 成果物はリポジトリ直下に置き、**ソースから再ビルド**するために必要なものをすべてコミットする。
評価では実際に、クリーンな virtualenv でそれを求められる。
ビルドバックエンドは何か。`pyproject.toml` は誰が持つか。再ビルドの練習は誰がいつやるか。

**How to think about it / 考え方**

**EN** — All modern backends are configured through the same `pyproject.toml`, so the choice matters less than
having done the rebuild **once, early, on a machine that has nothing installed**. Packaging failures are almost
always environment failures ("it works here"), and they surface at the worst possible moment. Treat the rebuild
as a rehearsal with a date, not as a final step.
**JA** — 現代のバックエンドはどれも同じ `pyproject.toml` で設定するので、
どれを選ぶかより「**何も入っていないマシンで、早い段階で一度**再ビルドを通したか」の方が重要。
パッケージングの失敗はほぼ常に環境の失敗(「こっちでは動く」)であり、最悪のタイミングで表面化する。
再ビルドは最後の工程ではなく、日付を決めたリハーサルとして扱う。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | The most examples and the most search results if something fails under time pressure.  **Cost:** more configuration surface than a single-module package needs. | 例と検索結果が最も多い。時間に追われた状況で失敗したときに強い。**コスト:** 単一モジュールのパッケージには過剰な設定項目を抱える。 |
| **B** | Minimal configuration and modern defaults.  **Cost:** fewer worked examples to copy from if the build misbehaves. | 設定が最小で、既定が現代的。**コスト:** ビルドが妙な挙動をしたときに参照できる実例が少ない。 |
| **C** | Simplest for exactly our shape — one module, one class.  **Cost:** least room to grow if the package later becomes more than a single module. | 「1 モジュール・1 クラス」という今回の形に最も簡単。**コスト:** 後でパッケージが単一モジュールを超えたとき、伸びる余地が最も小さい。 |

**EN** — Whichever we pick, the graded risk is not the backend but the rehearsal: §VI asks us to rebuild from source in a clean virtualenv during the evaluation (see 8.2).
**JA** — どれを選んでも、採点上のリスクはバックエンドではなくリハーサル。§VI は評価中に、クリーンな virtualenv でソースから再ビルドすることを求めている(8.2 参照)。

**Options / 選択肢**

|             | EN                                                                   | JA                                                               |
| ----------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **A** | setuptools — the most widely documented, most examples online.      | setuptools — 文書と例が最も多い。                               |
| **B** | hatchling — minimal configuration, modern default.                  | hatchling — 設定が最小で、現代的な既定。                        |
| **C** | flit — simplest for a single-module package, which is what this is. | flit — 単一モジュールのパッケージに最も簡単。今回はまさにそれ。 |

> Decision:

### 5.3 🟡 `LICENSE.md` / ライセンス

**EN** — Two things to fix. The subject asks for **`LICENSE.md`**; the repo has `LICENSE` with no extension. And it
reads `Copyright (c) 2026 Javier Pérez` — this is a pair project. §VI also says **choosing and writing the licence
is part of the assignment**: does MIT explicitly allow the reuse and redistribution the next project needs?
**JA** — 直すべき点が 2 つ。subject が求めるのは **`LICENSE.md`** だが、現在のファイルは拡張子なしの `LICENSE`。
さらに `Copyright (c) 2026 Javier Pérez` になっているが、これはペア課題。
§VI は**ライセンスを選び記述すること自体が課題の一部**とも言っている。
MIT は次のプロジェクトに必要な再利用と再配布を明示的に許可しているか。

**How to think about it / 考え方**

**EN** — The three common permissive licences differ mainly in what they ask of the person reusing the code: MIT
asks only that the notice be kept, Apache-2.0 adds an explicit patent grant and requires stating changes, BSD-3
adds a no-endorsement clause. A copyleft licence such as GPL would also allow reuse but would force the later
project to adopt the same terms — worth knowing so we can say why we did *not* pick it. Since §VI makes this a
graded choice, the answer we need is one sentence explaining the fit, not just a file.
**JA** — よく使われる 3 つの寛容型ライセンスの違いは、主に「再利用する人に何を求めるか」。
MIT は表示の保持だけを求め、Apache-2.0 は明示的な特許許諾を加えて変更の明示を要求し、
BSD-3 は「推奨表示の禁止」条項を加える。
GPL のようなコピーレフトも再利用は許すが、後続プロジェクトに同じ条件の採用を強制する。
「なぜそれを選ば*なかった*か」を言えるよう、知っておく価値がある。
§VI がこれを採点対象にしている以上、必要なのはファイルだけでなく、適合理由を述べる一文。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Shortest, most widely understood, and already in the repo — only the filename and the copyright line change.  **Cost:** no explicit patent grant, and "we kept what was there" is a weak answer to §VI's "choosing the licence is part of the assignment" unless we can say why MIT fits. | 最も短く広く理解されており、既にリポジトリにある。変えるのはファイル名と著作権表示だけ。**コスト:** 明示的な特許許諾がない。また §VI の「ライセンス選定も課題の一部」に対して、MIT が適合する理由を言えない限り「元からあったものを残した」は弱い答え。 |
| **B** | Explicit patent grant and a change-notice requirement — the most defensible answer about reuse.  **Cost:** a much longer file, and obligations heavier than a student maze generator needs. | 明示的な特許許諾と変更告知の要求があり、再利用について最も説明しやすい。**コスト:** ファイルがかなり長くなり、学生の迷路生成器に必要な以上の義務を背負う。 |
| **C** | Adds a no-endorsement clause on top of MIT-like terms.  **Cost:** the difference from MIT is small enough that we must be able to explain why it mattered to us. | MIT 相当の条件に「推奨表示の禁止」条項を足したもの。**コスト:** MIT との差が小さいため、「なぜ自分たちにとって重要だったか」を説明できる必要がある。 |

**Options / 選択肢**

|             | EN                                                                       | JA                                                                      |
| ----------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| **A** | Keep MIT, rename to`LICENSE.md`, add both names to the copyright line. | MIT のまま`LICENSE.md` にリネームし、著作権表示に二人の名前を入れる。 |
| **B** | Switch to Apache-2.0 for the explicit patent grant.                      | 明示的な特許許諾を理由に Apache-2.0 へ変更。                            |
| **C** | Switch to BSD-3-Clause.                                                  | BSD-3-Clause へ変更。                                                   |

> Decision:

---

## Part 6 — Testing / テスト

### 6.1 🟡 Framework and layout / フレームワークと配置

**EN** — §III.3: tests are **not submitted and not graded**, but they are how we know a module is finished. Where
do the files live, how are they named, and does each of us test our own code or each other's?
**JA** — §III.3:テストは**提出物でも採点対象でもない**。しかしモジュールの完成を判断する手段はこれしかない。
ファイルはどこに置き、どう命名し、各自が自分のコードをテストするか、相手のをテストするか。

**How to think about it / 考え方**

**EN** — Since tests are not graded, their only value is the value they give **us** — which means the interesting
question is not the framework but *who writes them*. Testing the other person's module forces you to read it and
to discover what it actually promises, which is the cheapest possible preparation for §IX. It also catches the
category of bug the author cannot see, because the author tests what they meant to write.
This project has an unusually good property to test: same seed ⇒ identical maze.
**JA** — テストは採点されないので、価値は**自分たちにとっての価値**しかない。
だから面白い問いはフレームワークではなく「誰が書くか」。
相方のモジュールをテストすると、それを読み、それが実際に何を約束しているかを知らざるを得なくなる。
§IX への準備として最も安い方法。
著者が見えない種類のバグも拾える(著者は「書いたつもりのもの」をテストするため)。
このプロジェクトには、テストしやすい良い性質がある:同じシード ⇒ 同一の迷路。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Fastest to write, since you test what you just built.  **Cost:** you test what you meant to write, so the bugs you cannot see stay invisible — and neither of us is forced to read the other's code (see 7.3). | 作ったものをそのままテストするので最も速い。**コスト:** 「書いたつもりのもの」をテストすることになり、自分に見えないバグは見えないまま残る。さらに、相手のコードを読む強制力が働かない(7.3 参照)。 |
| **B** | Reading the other's module becomes unavoidable — the cheapest §IX preparation available, and it doubles as coverage.  **Cost:** slower, and you may test the wrong thing until you have asked the author. | 相手のモジュールを読まざるを得なくなる。§IX への準備として最も安く、しかもカバレッジも増える。**コスト:** 遅い。著者に聞くまで見当違いのものをテストしうる。 |
| **C** | An end-to-end test catches the integration failures unit tests never see, including §IV.2's "must not crash".  **Cost:** the slowest suite, and a failure points at the whole pipeline rather than at one module. | E2E テストは単体テストが決して見ない統合時の失敗を捕まえる。§IV.2 の「クラッシュしない」も含む。**コスト:** 最も遅く、失敗しても原因が 1 モジュールではなくパイプライン全体を指す。 |

**EN** — Whatever we pick, "same seed ⇒ identical maze" is the cheapest high-value test this project offers (see 3.10).
**JA** — どれを選んでも、「同じシード ⇒ 同一の迷路」はこのプロジェクトで最も安く価値の高いテスト(3.10 参照)。

**Options / 選択肢**

|             | EN                                                                   | JA                                                                  |
| ----------- | -------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **A** | pytest,`tests/test_<module>.py`, each tests their own code.        | pytest、`tests/test_<module>.py`、各自が自分のコードをテスト。    |
| **B** | pytest, and we swap: each writes the tests for the other's module.   | pytest、担当を交換:相手のモジュールのテストを書く。                 |
| **C** | pytest for units, plus one end-to-end test driving`a_maze_ing.py`. | 単体は pytest、加えて`a_maze_ing.py` を動かす E2E テストを 1 本。 |

> Decision:

### 6.2 🟡 Definition of done / 「完成」の定義

**EN** — What must be true before a module is called finished, and who checks it — the author or the reviewer?
**JA** — モジュールを「完成」と呼ぶ条件は何か。確認するのは著者かレビュアーか。

**How to think about it / 考え方**

**EN** — Without a stated definition, "done" silently means "it ran once on my machine", and the gap surfaces at
integration. A workable definition is short enough to check in a minute and objective enough that two people
cannot disagree about it. Given the decision in 1.2 to work without Pull Requests, this checklist is one of the
few remaining places where quality is enforced, so it is worth being explicit about who applies it.
**JA** — 定義を決めないと、「完成」は静かに「自分の環境で一度動いた」を意味するようになり、
ズレは統合時に表面化する。
使える定義は、1 分で確認できる程度に短く、二人の解釈が割れない程度に客観的なもの。
1.2 で PR なしの運用を採るなら、このチェックリストは品質を担保する数少ない場所の一つになる。
誰が適用するかを明示しておく価値がある。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Objective enough that we cannot disagree, and it covers both graded checks (§III.1 and §IV.5).  **Cost:** slower to declare a module finished, and the analyzer only applies to some modules. | 解釈が割れない程度に客観的で、採点される 2 つの検査(§III.1 と §IV.5)を両方カバーする。**コスト:** 完成宣言までが遅く、analyzer が使えるモジュールは一部に限られる。 |
| **B** | Faster day to day, and it still covers lint and tests.  **Cost:** analyzer-detectable errors — wall coherence, the wrong mode — survive until a checkpoint. | 日々の速度が上がり、lint とテストは押さえられる。**コスト:** analyzer で検出できる誤り(ウォールの不整合、モード違い)がチェックポイントまで生き残る。 |
| **C** | No process overhead at all.  **Cost:** with no PRs (1.2) and no shared checklist, "done" silently means "ran once on my machine", and the gap surfaces at integration. | プロセス上の負荷がゼロ。**コスト:** PR がなく(1.2)共有のチェックリストもない状態では、「完成」は静かに「自分の環境で一度動いた」を意味し、ズレは統合時に表面化する。 |

**Options / 選択肢**

|             | EN                                                                                                                     | JA                                                                                                             |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **A** | Passes`make lint` + has tests for the edge cases in its plan file + accepted by `maze_analyzer.py` where relevant. | `make lint` が通る + 計画ファイルのエッジケースにテストがある + 該当時は `maze_analyzer.py` に受理される。 |
| **B** | Same, minus the analyzer (checked only at integration checkpoints).                                                    | 同じだが analyzer は除く(統合チェックポイントでのみ確認)。                                                     |
| **C** | Author declares it done; reviewer may reopen it after reading.                                                         | 著者が完成を宣言。レビュアーは読んだ後に差し戻せる。                                                           |

> Decision:

---

## Part 7 — Role division / 役割分担

### 7.1 🔴 Which split / どの分け方にするか

**EN** — Javier's document proposes two options and recommends the second. Do we take it as written, adjust it, or
invent a third split? On what basis do we choose sides — interest, prior experience, or deliberately the less
familiar side to learn more?
**JA** — Javier の文書は 2 案を提示し、2 つ目を推奨している。
そのまま採るか、調整するか、第三の分け方を作るか。
どちらの側を取るかの根拠は、興味か、経験か、それとも「あえて不慣れな側を取って学ぶ」か。

**How to think about it / 考え方**

**EN** — Two axes are worth separating. **Efficiency** says put each person where they are already strong;
**learning** says the opposite, and this is a school. Between the two extremes there is a common middle: split by
strength for the parts on the critical path, and deliberately swap for one or two non-critical pieces. Whatever we
choose, the split should follow a **seam in the design** — a place where the two halves talk through a small,
written interface — otherwise the division creates more coordination than it saves.
**JA** — 分けて考えるべき軸が 2 つある。**効率**は「各自が既に強い場所に置け」と言い、
**学習**は逆を言う。そしてここは学校である。
両極の間によくある中庸がある:クリティカルパス上は強みで分け、
そうでない 1〜2 個はあえて交換する。
どれを選ぶにせよ、分割は**設計上の継ぎ目**に沿わせること。
つまり、両半分が小さな書かれたインターフェース越しに話す場所で切る。
そうでない分割は、節約する以上の調整コストを生む。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Follows the document javi already wrote, so there is nothing to re-litigate, and the boundary sits at the output encoder — a small, writable interface.  **Cost:** all algorithmic difficulty lands on side A, and W19 (packaging) lands there too, making it the heavier of the two readings. | javi が既に書いた文書に沿うので蒸し返しがなく、境界が出力エンコーダに来る(小さく文書化しやすいインターフェース)。**コスト:** アルゴリズム的な難所がすべて A 側に集まり、さらに W19(パッケージング)も A 側。2 案のうち重い方の読み方になる。 |
| **B** | Same boundary, but packaging moves to the app side, which balances the load a little.  **Cost:** the person who did not write `MazeGenerator` has to package it, so they must understand its API — a cost or a benefit depending on what we decide in 7.3. | 境界は同じだが、パッケージングがアプリ側に移り、負荷が少し均される。**コスト:** `MazeGenerator` を書いていない方がそれを梱包するので、API を理解する必要がある。7.3 の決定次第でコストにも利点にもなる。 |
| **C** | A split shaped around what we actually want to learn.  **Cost:** we lose alignment with javi's document, which is already written and already understood by both of us. | 「何を学びたいか」に合わせて分けられる。**コスト:** 既に書かれ、二人とも理解している javi の文書との対応が失われる。 |

**Options / 選択肢**

|             | EN                                                                                         | JA                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| **A** | Javier's split A:*Maze Core & Generation* vs *Output, Visualisation & Infrastructure*. | Javier の A 案:「迷路コアと生成」対「出力・可視化・インフラ」。                               |
| **B** | Javier's split B (his recommendation):*Algorithm/Backend* vs *Frontend/Application*.   | Javier の B 案(彼の推奨):「アルゴリズム/バックエンド」対「フロントエンド/アプリケーション」。 |
| **C** | A third split of our own, derived from the table in 7.4.                                   | 7.4 の表から導く、独自の第三案。                                                              |

> Decision: A

### 7.2 🔴 Guarding against a lopsided split / 偏りを防ぐ

**EN** — Javier's own document warns against a split where one person only writes documentation or only rendering.
Does the interface side get real algorithmic work too, and how do we check mid-project that the balance held?
**JA** — Javier 自身の文書が「片方がドキュメントだけ、描画だけ」になる分け方を戒めている。
インターフェース側にもアルゴリズム的な仕事は回るか。途中でバランスが保たれているかをどう確認するか。

**How to think about it / 考え方**

**EN** — "Backend vs frontend" sounds balanced but is not automatically so: the generator concentrates the
algorithmic difficulty, while the other side can drift towards glue, config and docs. The output side does contain
genuine algorithmic work — the encoder, the validator, the solver — so the balance is a matter of where those
three land. A simple check is to name, at each integration checkpoint, one non-trivial thing each of us has
implemented since the last one.
**JA** — 「バックエンド対フロントエンド」は釣り合って聞こえるが、自動的に釣り合うわけではない。
生成器にアルゴリズム的な難所が集中し、もう一方は接着・設定・ドキュメントに流れやすい。
出力側にも本物のアルゴリズム的仕事はある(エンコーダ、バリデータ、ソルバ)。
つまりバランスはこの 3 つをどちらに置くかの問題。
簡単な確認方法は、統合チェックポイントごとに「前回以降に自分が実装した非自明なもの」を各自 1 つ挙げること。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Rebalances immediately and gives javi genuine algorithmic work.  **Cost:** §VI requires the reusable module to expose a solution, so moving the solver inverts the dependency between package and app (see 3.8). | すぐに均衡し、javi に本物のアルゴリズム作業が渡る。**コスト:** §VI が再利用モジュールに解の公開を求めるため、ソルバを移すとパッケージとアプリの依存方向が逆転する(3.8 参照)。 |
| **B** | Both of us understand the hardest code, which serves §IX directly.  **Cost:** two people on one task, in a project with about one month of calendar. | 最も難しいコードを二人とも理解でき、§IX に直接効く。**コスト:** 1 か月しかない日程で、1 つのタスクに 2 人を張り付ける。 |
| **C** | Guarantees both sides get touched by both people.  **Cost:** a context switch at the busiest moment, with handover cost paid twice. | 両方の側を二人とも触ることが保証される。**コスト:** 最も忙しい時期に文脈の切り替えが起き、引き継ぎコストを二人分払う。 |
| **—** | **Deferring (the decision below):** no cost now, and we act on evidence instead of prediction.  **Cost:** by the time an imbalance is visible the work is already written, so the correction is a handover rather than an assignment.  Naming *when* we look — at an integration checkpoint — is what stops "later" from meaning "never". | **判断を保留(下の決定):** 今のコストがゼロで、予測ではなく事実に基づいて動ける。**コスト:** 偏りが見える頃には作業は書き終わっているので、修正は「割り当て」ではなく「引き継ぎ」になる。*いつ見るか*(統合チェックポイント)を決めておくことが、「後で」を「結局やらない」にしない唯一の方法。 |

**Options / 選択肢**

|             | EN                                                                                       | JA                                                                       |
| ----------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **A** | Move the solver and the validator to the interface side to balance the algorithmic load. | ソルバとバリデータをインターフェース側に移し、アルゴリズム的負荷を均す。 |
| **B** | Keep the split, but pair on the two hardest parts (generation, "42").                    | 分割は維持し、最難所 2 つ(生成、「42」)はペアで書く。                    |
| **C** | Swap sides at the halfway milestone.                                                     | 中間マイルストーンで担当を交換する。                                     |

> Decision: 現時点では決めず、実際に実装してみて作業に偏りがあれば一部作業をもう一方に渡すことを検討する。

### 7.3 🔴 Both must be able to explain everything / 二人とも全部説明できること

**EN** — §IX: at the evaluation a small modification may be requested, and **both** of us must understand and be
able to change the implementation. What is the mechanism that makes this true rather than hoped for?
**JA** — §IX:評価では小さな修正を求められることがあり、**二人とも**実装を理解し変更できなければならない。
これを「願望」ではなく「事実」にする仕組みは何か。

**How to think about it / 考え方**

**EN** — This is the direct consequence of 1.2: without Pull Requests, nothing in the workflow *forces* either of
us to read the other's code, so the mechanism has to be added deliberately somewhere else. The options below are
ordered roughly by cost — and the honest test of whichever we pick is not "did we do it" but "can I make a small
change to their module, alone, in five minutes". That is literally what §IX describes.
**JA** — これは 1.2 の直接の帰結。PR がないなら、運用の中に「相手のコードを読まざるを得ない」場面が存在しない。
だから仕組みは、どこか別の場所に意図的に足す必要がある。
下の選択肢はおおむねコスト順。
そして選んだものの正直な検証は「やったかどうか」ではなく、
「相手のモジュールに、一人で、5 分で小さな変更を入れられるか」。§IX が描写しているのはまさにそれ。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | A fixed event forces the reading to happen whether or not we feel like it.  **Cost:** a recurring meeting slot. | 固定のイベントが、気分に関係なく「読むこと」を発生させる。**コスト:** 定例枠が 1 つ増える。 |
| **B** | Reading the other's module becomes a side effect of work we were going to do anyway.  **Cost:** tests take longer to write when you did not write the code. | 相手のモジュールを読むことが、どのみちやる作業の副産物になる。**コスト:** 自分が書いていないコードのテストは書くのに時間がかかる。 |
| **C** | The deepest shared understanding of the parts that matter most.  **Cost:** the most expensive option in hours. | 最重要部分について最も深い共通理解が得られる。**コスト:** 時間当たりのコストが最も高い。 |
| **D** | Rehearses exactly what §IX describes, under time pressure.  **Cost:** it happens at the end, so it finds gaps when there is least time to close them. | §IX が描写するものを、時間の制約付きでそのまま予行演習できる。**コスト:** 終盤に行うため、穴が見つかるのが最も時間のない時期になる。 |
| **—** | **The decision below (docstrings + written intent + read until understood):** no meeting overhead, and the reasoning lives next to the code where it is needed.  **Cost:** it relies on discipline rather than on an event — nothing visibly fails if we skip it for a week.  The cheapest way to add a trigger is to confirm at an existing checkpoint that we have each read the other's notes since the last one. | **下の決定(docstring + 変更意図の記録 + 理解するまで読む):** 会議の負荷がなく、理由が必要な場所(コードの隣)に残る。**コスト:** イベントではなく規律に依存するため、1 週間飛ばしても目に見える形では何も壊れない。引き金を足す最も安い方法は、既存のチェックポイントで「前回以降、相手のメモを読んだか」を確認すること。 |

**Options / 選択肢**

|             | EN                                                                                               | JA                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| **A** | Weekly walkthrough: each explains the**other's** module out loud, with questions.          | 週 1 の読み合わせ会:各自が**相手の**モジュールを声に出して説明し、質問を受ける。 |
| **B** | Test swap (6.1 option B): writing tests for the other's module forces reading it.                | テスト交換(6.1 の B):相手のモジュールのテストを書くことで読まざるを得なくする。        |
| **C** | Pair programming on the hardest parts only.                                                      | 最難所だけペアプログラミング。                                                         |
| **D** | A "modification drill" before the defense: each makes a small change in the other's code, timed. | ディフェンス前の「修正ドリル」:相手のコードに小さな変更を、時間を計って入れる。        |

> Decision: Docstrings (`"""   """`) on every function and class, **plus**: whenever either of us changes
> something, we record the **intent behind the change and the reasoning** in the docs, and each of us reads the
> other's until we actually understand it — not just until we have seen it.
> / docstring(`"""   """`)を全関数・全クラスに残す。**加えて**、どちらかが何かを変更したら、
> その**変更意図と理由**を doc に残し、相手はそれを「目を通した」ではなく「理解した」と言えるまで読む。

### 7.4 🔴 Work areas — assignment table / 担当表

**EN** — One row per work area. The two middle columns show how Javier's document assigns it, so we can see where
we agree with his proposal and where we deliberately differ. Fill the **Owner** column; use `both` only where it
is genuinely shared, because `both` often means nobody.
**JA** — 1 行 1 領域。中央 2 列は Javier の文書での割り当てを示す。
彼の案とどこで一致し、どこで意図的に外れるかが見えるようにするため。
**Owner** 列を埋める。`both` は本当に共有する場合だけにする(`both` はしばしば「誰もやらない」を意味するため)。

**EN** — In Javier's document, **A** = *Maze Core & Generation* (split A) or *Algorithm/Backend* (split B);
**B** = *Output, Visualisation & Infrastructure* (split A) or *Frontend/Application* (split B).
**JA** — Javier の文書での **A** は「迷路コアと生成」(A 案)または「アルゴリズム/バックエンド」(B 案)。
**B** は「出力・可視化・インフラ」(A 案)または「フロントエンド/アプリケーション」(B 案)。

| #   | Work area / 領域                                                      | Javier split A / A 案 | Javier split B / B 案 | Owner / 担当 | Note                                                           |
| --- | --------------------------------------------------------------------- | :-------------------: | :-------------------: | ------------ | -------------------------------------------------------------- |
| W01 | Config parsing (`KEY=VALUE`, comments) / 設定パース                 |           A           |           A           | so |                                                                |
| W02 | Config validation & error messages / 設定の検証とエラー文言           |           A           |           A           | so | see 3.9                                                        |
| W03 | Cell / Maze data structure / セル・迷路のデータ構造                   |           A           |           A           | so | **shared contract** — see 3.1                           |
| W04 | Wall representation (bitmask) / ウォール表現                          |           A           |           A           | so | **shared contract** — see 3.3                           |
| W05 | Generation algorithm / 生成アルゴリズム                               |           A           |           A           | so | see 3.5                                                        |
| W06 | Seed & reproducibility / シードと再現性                               |           A           |           A           | so | see 3.10                                                       |
| W07 | `PERFECT=True` mode / 完全迷路モード                                |           A           |           A           | so | see 3.4                                                        |
| W08 | `PERFECT=False` playable board / 遊べる盤面                         |           A           |           A           | so | see 3.4 — the default                                         |
| W09 | "42" pattern / 「42」パターン                                         |           A           |           A           | so | see 3.6                                                        |
| W10 | Maze validation (coherence, connectivity, width) / 迷路の検証         |           A           |           A           | so | see 3.7                                                        |
| W11 | Entry / exit validation / 入口・出口の検証                            |           A           |           A           | so |                                                                |
| W12 | Shortest-path solver / 最短経路ソルバ                                 |           A           |           A           | so | see 3.8, 7.2                                                   |
| W13 | Hex output encoding / 16 進エンコード                                 |           B           |           B           | javi |                                                                |
| W14 | Output file writing (entry, exit, path,`\n`) / 出力ファイル書き出し |           B           |           B           | javi |                                                                |
| W15 | Renderer (terminal / MLX) / 描画                                      |           B           |           B           | javi | see 4.1                                                        |
| W16 | User interactions (regen, path, colours) / ユーザー操作               |           B           |           B           | javi | see §V                                                        |
| W17 | `a_maze_ing.py` integration / 統合                                  |           B           |           B           | javi |                                                                |
| W18 | `MazeGenerator` reusable class / 再利用クラス                       |           A           |           A           | so | see 5.1                                                        |
| W19 | `mazegen-*` package build / パッケージビルド                        |           A           |      **B**      | so | **the two splits differ here** / ここだけ 2 案が食い違う |
| W20 | Makefile, lint setup,`.gitignore` / ビルド・lint 設定               |           B           |           B           | javi | see 2.2, 2.3                                                   |
| W21 | Unit tests (core) / コアの単体テスト                                  |           A           |           A           | so | see 6.1                                                        |
| W22 | Integration tests / 統合テスト                                        |           B           |           B           | javi |                                                                |
| W23 | README / README                                                       |           B           |           B           | javi | **whole file to one owner** — see 1.4                   |
| W24 | `LICENSE.md` / ライセンス                                           |           B           |           B           | javi | see 5.3                                                        |
| W25 | Docs upkeep (`Docs/`) / ドキュメント維持                            |          —          |          —          |              | not in Javier's doc / Javier の文書にない                      |

**EN** — Reading the table: Javier's two splits agree on everything except **W19**, and the real difference
between them is one of emphasis, not of boundary. So the genuine decision is narrower than it looks — it is
mainly *who takes side A*, plus what we deliberately move (7.2).
**JA** — 表の読み方:Javier の 2 案は **W19** を除いてすべて一致しており、
両者の違いは境界線ではなく力点の置き方にある。
つまり実際の判断は見た目より狭い。主として「どちらが A 側を取るか」と、
そこから意図的に動かすもの(7.2)だけ。

---

## Part 8 — Schedule / スケジュール

### 8.1 🟡 Milestones with dates / 日付付きマイルストーン

**EN** — Javier's document lists six milestones (skeleton → core → validation & solver → output & display →
package → finalisation). Attach a real date to each, and agree the **integration checkpoints**.
**JA** — Javier の文書は 6 つのマイルストーンを挙げている(骨組み → コア → 検証とソルバ → 出力と表示 →
パッケージ → 仕上げ)。それぞれに実際の日付を付け、**統合チェックポイント**を決める。

**How to think about it / 考え方**

**EN** — The dangerous shape for a two-person project is two long parallel branches meeting once at the end: every
mismatch surfaces simultaneously, at the moment there is no time left. The counter-measure is to force an early
integration even when both halves are incomplete — a generator that only makes a 3x3 maze, wired to a renderer
that only draws walls, is worth more than two impressive halves that have never met. Milestone dates are also the
raw material for the README's "how the planning evolved" (§VII), which only works if the original dates were
written down.
**JA** — 二人プロジェクトで危険な形は、長い並行ブランチが最後に一度だけ出会うこと。
食い違いが一斉に表面化し、しかもその時点で時間が残っていない。
対策は、両半分が未完成でも早期に統合を強制すること。
3x3 の迷路しか作れない生成器と、壁しか描けない描画がつながっている方が、
一度も出会っていない立派な半分 2 つより価値がある。
マイルストーンの日付は §VII の「計画がどう変化したか」の材料でもある。
これは当初の日付を書き残していて初めて成立する。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Follows the plan javi already wrote, and each boundary forces the two halves to meet.  **Cost:** six checkpoints in a one-month project is a lot of ceremony, and skipped checkpoints stop meaning anything. | javi が既に書いた計画に沿い、各境界で両半分が出会うことを強制できる。**コスト:** 1 か月のプロジェクトに 6 回のチェックポイントは儀式が多い。飛ばした瞬間に意味を失う。 |
| **B** | One fixed integration day is easy to remember and hard to skip.  **Cost:** coarse milestones make slippage visible late — a week can be lost before the plan shows it. | 統合日が週 1 で固定なら覚えやすく飛ばしにくい。**コスト:** マイルストーンが粗いため遅れの発覚が遅く、計画に現れる前に 1 週間失われうる。 |
| **C** | The rehearsal and the deadline are fixed first, so the schedule cannot silently eat the buffer.  **Cost:** it needs an honest estimate up front, and we do not yet know how long generation will take because 3.5 is still open. | リハーサル日と締切を先に固定するので、スケジュールがバッファを静かに食えなくなる。**コスト:** 最初に正直な見積もりが必要。3.5 が未決なので、生成にどれだけかかるかまだ分からない。 |

**EN** — Context: the deadline decided in 1.1 is 9/17, about one month, and 3.5 is still open — so the buffer is the part most worth protecting.
**JA** — 前提:1.1 で決めた締切は 9/17、約 1 か月。そして 3.5 が未決。つまり最も守る価値があるのはバッファ。

**Options / 選択肢**

|             | EN                                                                               | JA                                                                |
| ----------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **A** | Javier's six milestones with dates + an integration checkpoint at each boundary. | Javier の 6 マイルストーンに日付 + 各境界に統合チェックポイント。 |
| **B** | Fewer, larger milestones but a fixed weekly integration day.                     | マイルストーンは少なく大きく。ただし統合日を週 1 で固定。         |
| **C** | Deadline-backwards planning: fix the rehearsal date first, then work backwards.  | 締切から逆算:先にリハーサル日を固定し、そこから逆向きに置く。     |

> Decision:

### 8.2 🟡 Defense rehearsal / ディフェンスのリハーサル

**EN** — Pick a date, before the deadline, where we run the whole project from a clean clone, rebuild the package
in a fresh virtualenv, run `maze_analyzer.py`, and each explain the other's code out loud.
**JA** — 締切より前に日付を 1 つ決める。クリーンな clone からプロジェクトを動かし、
新しい virtualenv でパッケージを再ビルドし、`maze_analyzer.py` を回し、
お互いに相手のコードを声に出して説明する。

**How to think about it / 考え方**

**EN** — A rehearsal is only useful if what it finds can still be fixed, which means its value is set entirely by
its date — one scheduled for the last evening is not a rehearsal, it is a discovery. The clean clone matters
because it is the only way to catch the file we forgot to commit, and §VI's rebuild-in-a-virtualenv is a graded
step we should have performed at least once before the day it is graded.
**JA** — リハーサルは、見つかったものをまだ直せる場合にだけ有用。
つまり価値はその日付で完全に決まる。最終日の夜に置いたものはリハーサルではなく「発覚」。
クリーンな clone が重要なのは、コミットし忘れたファイルを捕まえる唯一の方法だから。
そして §VI の「virtualenv での再ビルド」は採点される工程なので、
採点される日より前に最低一度は通しておくべき。

**Consequences / 帰結**

|             | EN | JA |
| ----------- | -- | -- |
| **A** | Whatever it finds still has time to be fixed, and it covers §VI's clean-venv rebuild before that step is graded.  **Cost:** one shot — if the rehearsal itself is blocked by a broken build, we lose the day. | 見つかったものを直す時間が残る。§VI のクリーン環境での再ビルドを、採点される前に一度通せる。**コスト:** 一発勝負。ビルドが壊れていてリハーサル自体が進まないと、その日を失う。 |
| **B** | The early one finds environment and packaging problems while they are cheap; the late one is a real dress rehearsal.  **Cost:** two days of feature work spent on process. | 早い方は環境とパッケージングの問題を安いうちに見つけ、遅い方が本番同様のリハーサルになる。**コスト:** 機能開発の 2 日をプロセスに使う。 |
| **C** | No extra day in the schedule.  **Cost:** the final checkpoint is already the busiest moment, so the rehearsal is the first thing cut — and it is the one that finds the file we forgot to commit. | スケジュールに追加の日を取らない。**コスト:** 最後のチェックポイントは既に最も忙しい時点なので、真っ先に削られるのがリハーサル。そしてそれは「コミットし忘れたファイル」を見つける唯一の工程。 |

**Options / 選択肢**

|             | EN                                                              | JA                                     |
| ----------- | --------------------------------------------------------------- | -------------------------------------- |
| **A** | One rehearsal, 3–4 days before the deadline.                   | 締切の 3〜4 日前に 1 回。              |
| **B** | Two: a light one at the halfway point, a full one near the end. | 2 回:中間で簡易版、終盤で完全版。      |
| **C** | Merge it into the final integration checkpoint.                 | 最後の統合チェックポイントに統合する。 |

> Decision:

---

## Part 9 — All other decisions — summary table / その他の決定事項 — 一覧表

**EN** — The **Decision** column is filled for every row: this table is what we read six months from now.

The **Reason** column is deliberately *not* filled everywhere. Each item above now carries a Consequences table,
so for most rows the reason is already recorded — re-typing it here would be duplication, not documentation.
Fill Reason only where the subject demands a justification in its own words: **1.1** and **8.1** (§VII planning
and how it evolved), **1.4** (§VII AI usage), **3.5** (§VII the algorithm *and why*), **4.1** (§VII technical
choices), **5.1** (§VI what is reusable and how), **5.3** (§VI choosing the licence is part of the assignment).
Everything else may stay blank on purpose — a blank cell here is not unfinished work.

**JA** — **Decision** 列は全行埋める。半年後に読み返すのはこの表だから。

**Reason** 列は意図的に全部は埋めない。各項目に Consequences 表が付いたので、ほとんどの行では理由が既に記録されている。
ここに書き写すのは記録ではなく重複になる。Reason を埋めるのは、subject が「自分たちの言葉での説明」を要求する行だけ:
**1.1** と **8.1**(§VII 計画とその変化)、**1.4**(§VII AI の使い方)、**3.5**(§VII アルゴリズム*とその理由*)、
**4.1**(§VII 技術選定)、**5.1**(§VI 再利用可能な部分とその使い方)、**5.3**(§VI ライセンス選定も課題の一部)。
それ以外は意図的に空でよい。**ここの空欄は「やり残し」ではない。**

| #    | Item / 項目                                  | Pri | Decision / 決定 | Reason / 理由 | Owner |
| ---- | -------------------------------------------- | :-: | --------------- | ------------- | ----- |
| 1.1  | Deadline and rhythm / 締切とリズム           | 🔴 | ¹ヶ月（9/17） |               |       |
| 1.2  | Git workflow / git の運用                    | 🔴 | A |               |       |
| 1.3  | Documentation habit / ドキュメントの運用     | 🟡 |                 |               |       |
| 1.4  | AI usage & README owner / AI と README 担当  | 🟡 |                 |               |       |
| 2.1  | Python version & venv / バージョンと仮想環境 | 🔴 | ~~A~~ → **D — Poetry** (see `03_poetry_switch.md`) / D — Poetry に変更 | The subject allows any package manager (§III.2 names pip, uv, pipx). Poetry was chosen for the lock file, the dev/runtime split, and a build backend we need for §VI anyway. / subject は任意のパッケージマネージャを許容している。lock による版固定、dev/runtime の分離、§VI で必要になるビルド機構を理由に Poetry を選んだ。 | both |
| 2.2  | Lint configuration / lint 設定               | 🟡 |                 |               |       |
| 2.3  | Makefile ownership / Makefile 担当           | 🟡 |                 |               |       |
| 2.4  | `maze_analyzer.py` gate / 受け入れ判定     | 🟡 |                 |               |       |
| 3.1  | Maze data structure / データ構造             | 🔴 | A + D. ただし`Maze` クラスで包む。 |               |       |
| 3.2  | Coordinate convention / 座標規約             | 🔴 | A — `grid[y][x]`, origin top-left / A — 原点左上、`grid[y][x]` |               |       |
| 3.3  | Wall encoding invariant / 符号化の不変条件   | 🔴 | A |               |       |
| 3.4  | `PERFECT` modes / 2 つのモード             | 🔴 | A |               |       |
| 3.5  | Generation algorithm / 生成アルゴリズム      | 🔴 | A — recursive backtracker, iterative / A — 再帰的バックトラッカー(反復版) | Default mode is `PERFECT=False`, so braiding must remove nearly every dead end; this algorithm starts with the fewest (~10% vs ~30%, to be measured per §5.4 of the reference). Recursion depth is removed by the iterative form. / 既定が `PERFECT=False` で braiding が行き止まりをほぼ全部潰す必要があり、開始時の行き止まりが最少。再帰の深さは反復版で消える。 | so |
| 3.6  | "42" pattern / 「42」                        | 🔴 | A |               |       |
| 3.7  | Corridor width / 通路幅                      | 🟡 |                 |               |       |
| 3.8  | Shortest path / 最短経路                     | 🟡 |                 |               |       |
| 3.9  | Config keys & errors / 設定キーとエラー      | 🔴 | A |               |       |
| 3.10 | Seed / シード                                | 🟡 |                 |               |       |
| 4.1  | Terminal or MLX / 描画方式                   | 🔴 | A |               |       |
| 4.2  | MLX per OS / OS ごとの MLX                   | 🟡 |                 |               |       |
| 4.3  | Rendering and "42" / 描画と「42」            | 🟡 |                 |               |       |
| 5.1  | `MazeGenerator` API                        | 🟡 |                 |               |       |
| 5.2  | Build tooling / ビルド方法                   | 🟡 |                 |               |       |
| 5.3  | `LICENSE.md`                               | 🟡 |                 |               |       |
| 6.1  | Test framework & layout / テスト構成         | 🟡 |                 |               |       |
| 6.2  | Definition of done / 完成の定義              | 🟡 |                 |               |       |
| 8.1  | Milestones / マイルストーン                  | 🟡 |                 |               |       |
| 8.2  | Defense rehearsal / リハーサル               | 🟡 |                 |               |       |

### Rejected alternatives / 却下した案

**EN** — The evaluator will ask "why not the other option?". Answer it here while we still remember.
**JA** — 評価者は「なぜもう一方にしなかったのか」を聞く。覚えているうちにここに答えを書く。

| Item | Option rejected / 却下した案 | Why / 理由 |
| ---- | ---------------------------- | ---------- |
| 3.5 | Randomized Kruskal / ランダム化 Kruskal | On a grid, adjacency follows from the coordinates, so an edge list plus union-find is more machinery for the same result. Its dead-end ratio is no better than Prim's. Rejected as a generator only — union-find is still a candidate tool for validation (W10). / 格子では隣接関係が座標から決まるため、エッジ一覧と union-find は同じ結果に対して機構が多い。行き止まりの割合も Prim と同程度。却下したのは生成器としてのみで、union-find は W10 の道具として候補に残る。 |
| 3.5 | Randomized Prim / ランダム化 Prim | Roughly three times as many dead ends to start from, which is exactly the work braiding has to undo for the default `PERFECT=False` mode. Everything else between the two was a draw. / 開始時の行き止まりがおよそ 3 倍で、それは既定の `PERFECT=False` で braiding が取り消さねばならない作業そのもの。それ以外の観点は引き分けだった。 |
| 2.1 | `venv` + `pip` (option A, the original decision) | No lock file, so the two machines and the evaluator's are only aligned by agreement; runtime and dev dependencies end up mixed in one `requirements.txt`; and §VI's package build would need separate tooling configured by hand. / lock がないため、二人と評価者の環境は口約束でしか揃わない。runtime と dev の依存が `requirements.txt` に混ざる。§VI のパッケージビルドに別途ツール設定が必要になる。 |
| 3.2 | `grid[x][y]` (option B) | Output encoding and rendering are both row-oriented, so storing columns first would make javi's side read transposed on every loop. The config's `(x, y)` is converted once at parse time instead. / 出力と描画がどちらも行単位なので、列を先に格納すると javi 側が毎回転置して読むことになる。設定の `(x, y)` はパース時に一度だけ変換する。 |

---

## Open questions / 未解決事項

| #  | Question / 論点 | Blocked? / 作業を止めるか | Who investigates / 調査担当 |
| -- | --------------- | ------------------------- | --------------------------- |
| Q1 | Measure the real dead-end ratio for the backtracker, before and after braiding / backtracker の行き止まり率を braiding 前後で実測する | no — but it is the evidence behind 3.5 and the §VII justification / 3.5 の根拠と §VII の理由づけ | so — procedure in `learning_log/maze-generation-algorithms.md` §5.4 |
| Q2 | Union-find in validation (W10). **Narrowed:** counting independent loops needs no union-find — it is `E − V + 1` (see `generation-algorithm.md` §4.2). It remains a candidate for checking **connectivity**. / W10 での union-find。**論点が狭まった:** 独立ループの計数に union-find は不要(`E − V + 1` の引き算)。**連結性**の確認の候補としては残る。 | no | so |
| Q3 | W25 — who maintains `Docs/`? / `Docs/` の維持は誰か | no | both / 二人で |
| Q4 | Where does `MazeGenerator` live? The skeleton has both `maze/generator.py` and `mazegen/generator.py`; §VI wants the generator in a standalone importable module. / `MazeGenerator` の置き場所。骨組みに両方あるが、§VI は独立モジュールを要求している。 | no — settle in `mazegen-package-api.md` | so — W18 / W19 |
| Q5 | Which machine will javi use on evaluation day? He develops on a company Windows PC, which cannot be brought to the defense (§IX). Affects how defensively W15 must be written. / 評価当日に javi はどのマシンを使うか。会社の Windows PC は持ち込めない。W15 の作り方に影響する。 | **yes, eventually** — §IX applies to both of us | javi — see `03_poetry_switch.md` §6 |

## TODO

**EN** — Every TODO gets an owner and a due date. No owner means it is a wish, not a task.
**JA** — TODO には必ず担当者と期日を付ける。担当者がないものはタスクではなく願望。

- [ ] Write `Docs/implementation_plans/maze-data-structure.md` from 3.1–3.3 (owner: / due: )
- [ ] Update `Docs/commit_guide.md` to match the decision in 1.2 (owner: / due: )
- [ ] Rename `LICENSE` → `LICENSE.md` and add both names (owner: / due: )
- [ ] (owner: so / due: )
- [ ] (owner: javi / due: )

## Next meeting / 次回

- **When / 日時**:
- **Goal / 目的**:
