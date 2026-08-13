<!--
How to use / 使い方
  EN: Copy this file to topic-name.md (kebab-case) BEFORE writing the code it describes.
      Fill "Scope" and "Interface" first, get the pair to review, then implement.
      The Interface section holds SIGNATURES ONLY — type hints, classes, exceptions.
      NEVER write a function body here. Write the body in English (shared contract).
      Delete this comment block.
  JA: 対象コードを書く**前**に topic-name.md(kebab-case)へコピーする。
      まず「Scope」と「Interface」を埋め、相方のレビューを受けてから実装する。
      Interface に書くのは**シグネチャだけ**(型ヒント・クラス・例外)。
      **関数の本体は絶対に書かない**。本文は共有の契約なので英語で書く。
      このコメントブロックは削除する。
-->

# <topic name>

| | |
| --- | --- |
| **Owner / 担当** | so \| javi \| both |
| **Status / 状態** | draft → reviewed → implemented |
| **Date / 日付** | YYYY-MM-DD |
| **Subject ref** | §IV.x, §V, … |
| **Related / 関連** | `Docs/learning_log/<topic>.md`, `Docs/pair_communication/YYYY-MM-DD_<topic>.md` |

---

## 1. Scope / 対象範囲

### In scope

<!-- What this module is responsible for. Be precise; this is a contract. -->

-

### Out of scope

<!-- Just as important: what it must NOT do, and who does it instead. -->
<!-- 同じくらい重要:何を「やらない」か、代わりに誰がやるか。 -->

-

### Requirement it satisfies / 対応する要件

<!-- Quote the subject with its section number. Every plan must trace back to the subject. -->

> §IV.x — "…"

## 2. Interface / インターフェース

> **Signatures only. No function bodies.** / **シグネチャのみ。関数本体は書かない。**

### Public API

```python
# Types / aliases
Coord = tuple[int, int]


class Example:
    """One line: what this object is responsible for."""

    def __init__(self, width: int, height: int, seed: int | None = None) -> None: ...

    @property
    def something(self) -> list[int]: ...

    def do_the_thing(self, target: Coord) -> str: ...


def parse(argv: list[str]) -> list[int]: ...
```

### Exceptions raised / 送出する例外

| Exception | Raised when / 条件 | Who catches it / 誰が捕まえるか |
| --- | --- | --- |
| `ValueError` | | `a_maze_ing.py` → user-facing message |
| | | |

### Data it owns / 保持するデータ

| Name | Type | Meaning / 意味 | Invariant / 不変条件 |
| --- | --- | --- | --- |
| | | | |

## 3. Implementation steps / 実装手順

<!-- Ordered steps, each small enough to be one commit. Describe WHAT each step achieves, -->
<!-- not the code that achieves it. / 1 ステップ = 1 コミットの粒度。何を達成するかを書く(書き方ではなく)。 -->

1.
2.
3.

## 4. Edge cases / エッジケース

<!-- The subject says the program must NEVER crash unexpectedly (§IV.2). -->
<!-- Every row here should become a test. / 各行がそのままテストになる。 -->

| # | Input / situation | Expected behaviour / 期待する挙動 |
| --- | --- | --- |
| E1 | | |
| E2 | | |
| E3 | | |

## 5. Complexity / 計算量とその根拠

| Operation | Time | Space | Why this is acceptable / 許容できる理由 |
| --- | --- | --- | --- |
| | O(?) | O(?) | for a WIDTH×HEIGHT grid, … |

<!-- "Why acceptable" matters more than the O() itself: state the realistic input size -->
<!-- and what would happen at 10x that size. -->
<!-- O() そのものより「なぜ許容できるか」が重要。現実的な入力サイズと、その 10 倍で何が起きるかを書く。 -->

## 6. Test plan / テスト方針

<!-- pytest. Tests are not graded (§III.3) but they are how we know we are done. -->

| Test | Kind | Checks / 何を保証するか |
| --- | --- | --- |
| `test_…` | unit | |
| `test_…` | edge | |
| `test_…` | property | e.g. same seed ⇒ identical maze |

- Verified with `maze_analyzer.py`? / `maze_analyzer.py` で検証するか: yes / no / n.a.

## 7. Rejected alternatives / 却下した案

<!-- The defense WILL ask "why not X?". Answer it here, now, while you remember. -->
<!-- ディフェンスでは必ず「なぜ X ではないのか」を聞かれる。覚えているうちに答えを書く。 -->

| Option | Why rejected / 却下理由 |
| --- | --- |
| | |

## 8. Open questions / 未解決

- [ ]

## 9. Changelog / 変更履歴

<!-- If the design changes during implementation, log it here in the SAME commit as the code. -->
<!-- 実装中に設計が変わったら、コードと同じコミットでここに記録する。 -->

| Date | Change / 変更 | Reason / 理由 |
| --- | --- | --- |
| YYYY-MM-DD | initial draft | — |
