# 📦 Why Poetry Is Better Than pip for This Project

# 📦 なぜこのプロジェクトでは pip より Poetry が適しているのか

## English

The subject permits any package manager (it names `pip`, `uv`, and `pipx`); it
does not prescribe Poetry. We chose Poetry because it provides a clean,
reproducible workflow with dependency locking, development-dependency groups,
and a build backend for the reusable `mazegen-*` package.

subject は `pip`、`uv`、`pipx` など任意のパッケージマネージャを許可しており、Poetry を指定していません。
本プロジェクトでは、依存関係の固定、開発用依存の分離、`mazegen-*` 用のビルドバックエンドを一体で提供するため、Poetry を選択しました。

### 1. Reproducible environments 完全に再現可能な環境

Poetry generates a `poetry.lock` file that pins exact dependency versions.  
This ensures that all developers — and the evaluator — install **the same environment**, avoiding inconsistencies and “works on my machine” problems.

Poetry は poetry.lock に依存関係の正確なバージョンを記録します。
これにより、チームメンバーも評価者も 同じ環境 を確実に再現でき、「自分の環境では動く」という問題を避けられます。

### 2. Built‑in virtual environment management 仮想環境の自動管理

Poetry automatically creates and manages virtual environments:

Poetry は仮想環境の作成・管理を自動化します。

```bash
poetry install
poetry shell
```

No manual python -m venv creation or activation is required, which reduces setup errors and keeps the workflow simple.

手動で venv を作成・有効化する必要がなく、セットアップミスを減らし、ワークフローをシンプルに保てます。

### 3. Clear separation of runtime and development dependencies

The project requires tools like pytest, flake8, and mypy.
Poetry allows grouping them cleanly as development dependencies:

このプロジェクトでは pytest、flake8、mypy が必須です。
Poetry ならこれらを開発用依存としてきれいに分離できます。

```toml
[tool.poetry.group.dev.dependencies]
pytest = "*"
flake8 = "*"
mypy = "*"
```

With pip, all dependencies are usually mixed into a single requirements.txt, making it harder to distinguish between runtime and development tools.

pip では通常、すべてが requirements.txt に混在し、実行時と開発時の依存を区別しにくくなります。

### 4. Required for building the reusable mazegen-\* package パッケージのビルドに必須

The subject explicitly requires building a distributable package of the maze generator.
Poetry provides a simple and reliable build system:

subject は迷路ジェネレーターを配布可能なパッケージとしてビルドすることを要求しています。
Poetry は次のように簡単にビルドできます

```bash
poetry build
```

This produces .whl and .tar.gz files without extra configuration, which fits the requirement to deliver a reusable mazegen-\* package.

これにより .whl と .tar.gz が生成され、再利用可能な mazegen-\* パッケージを要件どおりに提供できます。

### 5. Centralized configuration with pyproject.toml - pyproject.toml による一元管理

The project structure document states that pyproject.toml is the central configuration file and is managed with Poetry.
This file contains metadata, dependencies, build settings, and tool configurations in one place, making the project easier to understand and maintain.

プロジェクト構成ドキュメントでは、pyproject.toml がプロジェクトの中心となる設定ファイルであり、Poetry によって管理されるとされています。
このファイルにはメタデータ、依存関係、ビルド設定、ツール設定がまとまっており、プロジェクトの理解と保守が容易になります。

### 6. Chosen workflow 選択したワークフロー

The subject allows package managers such as `pip`, `uv`, and `pipx`. Poetry is
our project choice, so these are our commands:

subject は `pip`、`uv`、`pipx` などを許可しています。以下の Poetry コマンドは、私たちが選択したワークフローです。

```bash
poetry install
poetry run pytest
poetry run flake8 .
poetry run mypy .
poetry build
```

These commands document the project workflow; they are not commands prescribed
by the subject or evaluator.

これらはプロジェクトの手順であり、subject や評価者が指定したコマンドではありません。

### Summary まとめ

Poetry is chosen because it provides:
Poetry を使う理由は以下の通りです：

- Reproducibility via poetry.lock
- 再現性の高い環境

- Automatic virtualenv management
- 仮想環境の自動管理

- Clear separation of runtime vs. development dependencies
- 依存関係の明確な分離

- Simple packaging for mazegen-\* (wheel and sdist)
- mazegen-\* のパッケージ化の容易さ

- Unified configuration in pyproject.toml
- pyproject.toml による統合管理

- A workflow we selected for this project
- 本プロジェクトで選択したワークフロー

Using pip alone is permitted by the subject. It would require us to select and
configure equivalent locking, environment, and build tooling ourselves, whereas
Poetry supplies those capabilities together.

pip のみでも subject の要件を満たすことは可能です。ただし同等の lock、仮想環境、ビルド機能を別途選択・設定する必要があります。Poetry はそれらを一体で提供します。
