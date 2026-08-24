# Python Docstrings

|                                |                                                                                        |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| **Author / 筆者**              | javi                                                                                   |
| **Date / 日付**                | 2026-08-24                                                                             |
| **Where it is used / 使い所**  | `display/terminal_renderer.py`, Python project documentation                           |
| **Written with AI? / AI 併用** | yes — drafted and reviewed with AI using the current renderer as the example           |
| **Confidence / 理解度**        | 4/5 — can explain the purpose and structure, but should practise writing more examples |

---

## 1. In one sentence / 一言でいうと

**EN** — A docstring is a string written inside a Python module, class, or function to explain its purpose, inputs, outputs, and important behaviour.

**JA** — docstring は Python のモジュール・クラス・関数の中に書く文字列で、目的、入力、出力、重要な動作を説明するものです。

## 2. Why it is needed / なぜ必要か

**EN** — A docstring makes code easier to understand without reading every implementation detail, helps teammates maintain the project, and can be displayed by tools such as `help()` and documentation generators.

**JA** — docstring があると、実装の細部をすべて読まなくてもコードを理解しやすくなり、チームメンバーの保守を助けます。また、`help()` やドキュメント生成ツールで表示できます。

## 3. What you need to know first / 前提として知っておくこと

**EN** — A docstring is the first string literal in a module, class, or function body. Python stores it in the object's `__doc__` attribute. It is different from a normal comment: comments explain code to readers, while docstrings describe the public purpose and contract of a code object.

The opening line should be a short summary. Add more detail only when the behaviour, parameters, return value, exceptions, or invariants need clarification. The documentation should describe what the code does, not repeat every line of how it does it.

**JA** — docstring はモジュール・クラス・関数の本体の最初に置く文字列リテラルです。Python はそれをオブジェクトの `__doc__` 属性に保存します。通常のコメントとは異なります。コメントはコードを読む人に補足を与え、docstring はコードオブジェクトの公開目的と契約を説明します。

最初の行は短い要約にします。動作、引数、戻り値、例外、不変条件の説明が必要な場合だけ詳細を追加します。コードの各行を繰り返すのではなく、何をするコードなのかを説明します。

## 4. How it works / 仕組み

**EN** — Use triple double quotes for multi-line docstrings. A clear function docstring normally has these parts:

1. A one-line summary of the function's responsibility.
2. A `Parameters` section when arguments need explanation.
3. A `Returns` section when the return value needs explanation.
4. An `Raises` section when callers need to know about expected exceptions.
5. Additional notes for side effects, optional attributes, formats, or invariants.

For a function that returns `None` and only prints or mutates state, explicitly explain the side effect. For a constructor, `Returns: None` is technically true but often unnecessary; the important information is what object is configured or created.

**JA** — 複数行の docstring には三重のダブルクォートを使います。分かりやすい関数の docstring は通常、次の部分で構成します。

1. 関数の責任を一行で要約する。
2. 引数の説明が必要なら `Parameters` セクションを書く。
3. 戻り値の説明が必要なら `Returns` セクションを書く。
4. 呼び出し側が知るべき例外があれば `Raises` セクションを書く。
5. 副作用、オプションの属性、形式、不変条件があれば補足する。

`None` を返して表示や状態変更だけを行う関数では、その副作用を明確に説明します。コンストラクタでは `Returns: None` は技術的には正しいですが、必ずしも必要ではありません。重要なのは、どのようなオブジェクトを設定・生成するかです。

## 5. Figure, example, trace / 図・具体例・トレース

**EN** — The following example is based on `TerminalRenderer._horizontal_wall()`:

```python
def _horizontal_wall(
    self, maze: MazeLike, y: int, wall: int
) -> str:
    """Build one horizontal border for a maze row.

    Parameters
    ----------
    maze:
        Maze whose cells provide the wall masks.
    y:
        Row index to inspect.
    wall:
        Wall bit to inspect, normally ``N`` or ``S``.

    Returns
    -------
    str
        A border string with one three-character segment per cell and a
        corner at each end.
    """
```

The first sentence says what the function builds. `Parameters` explains the meaning of each input instead of merely repeating its type. `Returns` explains the shape and purpose of the returned string.

With a four-cell row and masks indicating that the selected wall is closed in cells 0 and 2, the function produces:

```text
+---+   +---+   +
```

The example is useful because it connects the documentation to the renderer's real fixed-width format.

The class-level documentation in `TerminalRenderer` is shorter because the class has one main responsibility:

```python
class TerminalRenderer:
    """Render a maze as a fixed-width ASCII drawing in the terminal."""
```

**JA** — 次の例は `TerminalRenderer._horizontal_wall()` に基づいています。

最初の文は関数が作るものを説明します。`Parameters` は型を繰り返すのではなく、各入力の意味を説明します。`Returns` は返される文字列の形と目的を説明します。

4 セルの行で、指定された壁がセル 0 とセル 2 で閉じている場合、関数の結果は次のようになります。

```text
+---+   +---+   +
```

この例は、ドキュメントを renderer の実際の固定幅形式と結び付けています。

`TerminalRenderer` クラスの docstring は、主な責任が一つなので短く書かれています。

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解                                                                          | Reality / 実際は                                                                                                                                                   |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A docstring should describe every implementation line. / すべての実装行を説明する必要がある。 | It should explain the public purpose and contract. / 公開される目的と契約を説明する。                                                                              |
| The return type alone explains the result. / 戻り値の型だけで十分である。                     | Explain what the value means and its format when it is not obvious. / 型だけで意味や形式が分からない場合は説明する。                                               |
| `Returns None` means there is nothing important to document. / `None` なら説明は不要である。  | Printing and state changes are side effects and should be documented. / 表示や状態変更は副作用なので説明する。                                                     |
| Comments and docstrings are interchangeable. / コメントと docstring は同じである。            | Docstrings belong to modules, classes, and functions and are available through `__doc__`. / docstring はモジュール・クラス・関数に属し、`__doc__` から取得できる。 |
| A long docstring is always better. / 長い docstring ほど良い。                                | Prefer a concise summary and only the detail needed by the caller. / 短い要約を基本に、呼び出し側に必要な詳細だけを書く。                                          |

## 7. How we use it here / この課題での使い方

**EN** — In this project, docstrings document the display contract and make the renderer easier for both teammates to understand and modify. `display/terminal_renderer.py` uses docstrings for `MazeLike`, `TerminalRenderer`, `render()`, `_horizontal_wall()`, `_vertical_wall()`, and `_cell_content()`.

The renderer documentation records that the maze must provide `width`, `height`, and `walls_at((x, y))`. It also explains the wall-bit encoding (`N=1`, `E=2`, `S=4`, `W=8`) and the optional `entry`, `exit`, and `shortest_path` attributes. This is especially useful while `maze/maze.py` is still a structural reference and `DummyMaze` is temporary.

**JA** — このプロジェクトでは、docstring を使って表示処理の契約を説明し、二人のメンバーが renderer を理解して変更しやすくします。`display/terminal_renderer.py` では `MazeLike`、`TerminalRenderer`、`render()`、`_horizontal_wall()`、`_vertical_wall()`、`_cell_content()` に docstring があります。

renderer のドキュメントには、maze が `width`、`height`、`walls_at((x, y))` を提供する必要があることを書いています。また、壁のビット表現（`N=1`、`E=2`、`S=4`、`W=8`）と、オプションの `entry`、`exit`、`shortest_path` 属性も説明しています。`maze/maze.py` がまだ構造の参照で、`DummyMaze` が一時的な実装である間に特に役立ちます。

## 8. Self-check / 確認問題

- [ ] Q1. What is the difference between a comment and a docstring, and where can Python find a docstring at runtime?
- [ ] Q2. What should a function's `Parameters` and `Returns` sections explain beyond the type hints?
- [ ] Q3. What side effect must `render()` document even though its return type is `None`?

## 9. Still unclear / まだ分かっていないこと

- [ ] Decide whether the project should standardise on NumPy-style sections or Google-style sections for all future modules.
- [ ] Add documentation for expected exceptions once the real `Maze` implementation is complete.

## 10. Related / 関連

- [`display/terminal_renderer.py`](../../display/terminal_renderer.py)
- [`maze/maze.py`](../../maze/maze.py)
- [`Docs/implementation_plans/maze-data-structure.md`](../implementation_plans/maze-data-structure.md)
- [`Docs/work_log/2026-08-24_javi.md`](../work_log/2026-08-24_javi.md)

## 11. Sources

- Python Documentation — Documentation Strings: https://peps.python.org/pep-0257/
- Python Documentation — Tutorial: Documentation: https://docs.python.org/3/tutorial/controlflow.html#documentation
