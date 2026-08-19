# 📦 Why Poetry Is Better Than pip for This Project

# 📦 なぜこのプロジェクトでは pip より Poetry が適しているのか

## English

Poetry is used in this project because it provides a **clean, reproducible, and professional development workflow** that aligns with the requirements of the A‑Maze‑ing subject. While `pip` is only an installer, Poetry is a **full dependency and packaging manager**, which is essential for building the reusable `mazegen-*` package and maintaining consistent environments across the team.

Poetry がこのプロジェクトで使用される理由は、A‑Maze‑ing の要件に合った 再現性・依存関係管理・パッケージ化・開発フロー を提供するためです。
pip は単なるインストーラーですが、Poetry は 依存管理とパッケージ管理を統合したツール であり、このプロジェクトに最適です。

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

### 6. Officially recommended workflow 公式に推奨されている開発フロー

The subject lists Poetry commands as the expected workflow:

ドキュメントには、期待されるワークフローとして Poetry のコマンドが記載されています。

```bash
poetry install
poetry run pytest
poetry run flake8 .
poetry run mypy .
poetry build
```

This confirms Poetry is part of the project design and evaluation process.

つまり、Poetry は単なる選択肢ではなく、このプロジェクトの設計と評価プロセスの一部です。

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

- A workflow that matches the project subject and evaluator expectations
- subject に完全準拠したワークフロー

Using pip alone would require additional tools and manual steps (manual venv creation, separate lock/requirements management, explicit build tooling configuration) and would not meet the project’s stated requirements as cleanly or reliably.

pip のみでは、追加ツールや手動設定なしにこれらの要件を満たすことは困難です。
