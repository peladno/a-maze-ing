# 9. テスト — `tests/`

| | |
| --- | --- |
| **書いた人** | so(設定・迷路・生成器の前半)、javi(表示・出力)、Claude(生成器の後半・ソルバー、so の依頼による) |
| **実行** | `make test`(`poetry run pytest -q`) |
| **subject** | §III.3(テストは提出物ではないが、完成の判断に使う) |

## この章で分かること

- pytest の基本(テストの見つけ方、`assert`、例外の確かめ方、出力の捕まえ方)
- 6 つのテストファイルと 133 本のテストが、それぞれ何を守っているか
- 補助関数の役目
- 「壊して確かめる」(ミューテーションテスト)の考え方

---

## 1. そもそもの概念

### 1.1 pytest の基本

| 仕組み | 書き方 | 意味 |
| --- | --- | --- |
| テストの発見 | `tests/test_*.py` の中の `def test_...():` | pytest が自動で見つけて実行する |
| 確かめる | `assert 式` | 式が偽ならテストが失敗し、値を詳しく表示する |
| 例外を確かめる | `with pytest.raises(SomeError) as excinfo:` | 中で `SomeError` が投げられなければ失敗。`str(excinfo.value)` でメッセージを確かめる |
| 表示を捕まえる | 引数に `capsys` を書き、`capsys.readouterr().out` | 標準出力・標準エラーに何が出たかを確かめる |
| 入力を差し替える | `monkeypatch.setattr("builtins.input", ...)` | `input()` の代わりに決めた値を返させる |
| 一時フォルダ | 引数に `tmp_path` | テストごとに新しい空のフォルダがもらえる |

→ 学習ノート [`pytest-basics.md`](../learning_log/pytest-basics.md)

### 1.2 「一度も失敗したことのないテストは、何も証明しない」

テストが通っても、そのテストが**バグを見つけられる**とは限りません。`print` しかしないテストは常に通ります。

そこでこのプロジェクトでは、**ミューテーションテスト**で確かめました。

1. 本物のコードをコピーし、わざと 1 か所だけ壊す(例:`popleft()` を `pop()` にする、`>= 2` を `>= 1` にする)。
2. テストを実行する。
3. どれかのテストが**失敗すれば**、そのテストはそのバグを見つけられる(検出)。全部通ってしまえば、見逃している(生存)。

結果(作業ログより):

| 対象 | 入れたバグ | 検出 |
| --- | --- | --- |
| 生成器 | 44 種類 | 43 種類(残りの 1 つは、実際の迷路の結果を変えられないもの) |
| ソルバー | 12 種類 | 12 種類(1 つはテストが止まらなくなる形で検出) |

---

## 2. ファイルごとの一覧

| ファイル | 本数 | 対象 |
| --- | --- | --- |
| `test_maze.py` | 18 | `maze/maze.py`(1 章) |
| `test_config.py` | 41 | `maze/config.py`(2 章) |
| `test_generator.py` | 47 | `maze/generator.py`(3 章) |
| `test_solver.py` | 10 | `maze/solver.py`(4 章) |
| `test_output.py` | 3 | `output/maze_writer.py`(5 章) |
| `test_display.py` | 14 | `display/`(6 章) |

エントリポイント `a_maze_ing.py` の `main` を丸ごと動かすテストはありません(対話の入力が必要なため)。

---

## 3. `test_maze.py`(18 本)

| 分類 | テスト | 守っていること |
| --- | --- | --- |
| `Direction` | `test_opposite_is_symmetric` | 反対の反対は元に戻る |
| | `test_delta_and_opposite_cancel_out` | ある向きと反対の向きの `delta` を足すと `(0, 0)` |
| 作成 | `test_new_maze_has_given_size_and_all_walls_closed` | 大きさが正しく、全部 15 |
| | `test_invalid_size_raises_value_error` | 大きさ 0 以下は `ValueError` |
| | `test_new_maze_has_no_open_wall` | 新しい迷路にはどの向きにも開いた壁が無い |
| 範囲 | `test_contains_only_accepts_positions_inside_grid` | 盤面の中だけ真(正方形でない盤面で、x と y の取り違えも見つける) |
| | `test_walls_at_raises_outside_grid` | 盤面の外は `OutOfBoundsError` |
| `open_passage` | `test_open_passage_updates_both_cells` | 両側のビットが消える |
| | `test_open_passage_raises_when_not_adjacent` | 隣でない 2 つは `NotAdjacentError` |
| | `test_open_passage_is_idempotent` | 2 回開けても同じ |
| | `test_open_passage_raises_outside_grid` | 盤面の外は `OutOfBoundsError` |
| | `test_open_passage_refuses_reserved_cells` | 確保セルは `MazeError` |
| 隣 | `test_neighbours_stops_at_the_edge` | 内側のセル (1,1) の隣は N・E・S・W の順に 4 つ、角のセル (0,0) では盤面の外が除かれる |
| | `test_neighbours_skips_reserved_cells` | 確保セルは出てこない |
| | `test_neighbours_raises_outside_grid` | 盤面の外は(回したときに)`OutOfBoundsError` |
| | `test_open_neighbours_only_returns_carved_cells` | 開けた壁の向こうだけ |
| `rows` | `test_rows_has_one_tuple_per_row` | 行の数だけタプルが出る |
| | `test_rows_agrees_with_walls_at` | `rows` と `walls_at` が一致する |

---

## 4. `test_config.py`(41 本)

| 分類 | 守っていること(テスト名の要点) |
| --- | --- |
| 文法(`_read_pairs`) | `=` の無い行はエラー、簡単な設定が読める、空行とコメントは無視、空白を取り除く、値に `=` が入ってよい、値の中の `#` は残る、知らないキーは残る、キーは大文字小文字を区別、`\r\n` の改行、空のキーはエラー、重複キーはエラー |
| メッセージ | ファイル名と行番号が入る、重複のメッセージは両方の行を示す |
| `_as_filename` | 名前を受け付ける、空は拒否 |
| `_as_bool` | `True`・`False` を受け付ける、ほかの綴りは拒否 |
| `_as_int` | 数を受け付ける、数でないものは拒否、最小値未満は拒否、**最小値 0 でも範囲を確かめる**、最小値なしなら負も受け付ける |
| `_as_coord` | `x,y` を受け付ける、数が 1 つ・3 つは拒否、数でない・負は拒否、数の前後の空白は許す |
| `parse_config` | 正しい設定が読める、足りないキーを全部示す、`SEED` が無ければ `None`、**`SEED=0` は `0` のまま**、入口・出口が盤面の外、入口 = 出口 |
| `load_config` | ファイルを読める、ファイルが無い、フォルダを渡した、**コミットされている `config.txt` が読める** |

**`SEED=0` と「最小値 0」のテストがある理由:** `if seed:` や `if minimum:` と書くと、`0` が「無い」と同じ扱いになるバグが入ります。そのバグだけを見つけるためのテストです。

**`test_comments_are_ignored` の工夫:** コメントを `# a comment` にすると、`=` が無いのでコメントの判定を消しても(構文エラーとして)失敗し、テストの意味がありません。`# WIDTH=99` にして、辞書**全体**を比べることで、コメントの判定が壊れたときだけ失敗するようにしています(作業ログ 9/5)。

---

## 5. `test_generator.py`(47 本)

### 補助関数

| 関数 | 役目 |
| --- | --- |
| `_count_passages(m)` | 開いた壁(東と南だけを数えて重複なし)の数 |
| `_count_reachable(m)` | (0,0) から歩いて届くセルの数(ソルバーとは別に書いた探索) |
| `_open_all_but(w, h, closed, reserved)` | 指定した壁**以外**を全部開けた盤面を作る。3x3 のテストで「この壁だけ閉じている」状態を簡単に作るため |

### テストの分類

| 段階 | 守っていること |
| --- | --- |
| `__init__` | 渡したシードを保つ(0 も)、無ければ作る(2 つの生成器で違う値)、`perfect`・`seed` はキーワード専用、1 未満は拒否(負×負も)、既定モードで小さすぎる盤面は拒否、3x2 と 2x3 は受け付ける、完全迷路なら 1 列でもよい |
| 掘る | 通路 = セル − 1、全セルに届く、同じシードで同じ迷路、1 列、300 × 300、確保セルは閉じたまま、確保セルで分断されたら `GenerationError`(`only 3 of 6`) |
| `generate` | 完全迷路になる、2 回呼んで同じ、既定モードは遊べる盤面(20 シード:届く・ループ 2 以上・行き止まり 2 以下)、3x3 が無い、最小の盤面でループがちょうど 2、同じシードで同じ、**何も表示しない**(`capsys`) |
| 「42」 | 9x7 未満は省く、20x15 で中央に置く、9x7〜29x29 で四隅と中央の候補が空く、確保セルは閉じたまま、9x7 で両モードとも正しい |
| 行き止まり | 木の行き止まり `[(0,0), (1,0), (0,2)]`、「42」だけに面した行き止まりは数えない、braiding 後は無い |
| 3x3 | 12 枚を数える、最後の 1 枚(横・縦)で完成、2 枚閉じていれば完成しない、3x2 にはブロックが無い、盤面の外のブロックは飛ばす、確保セルを含むブロックは完成しない |
| braiding | 手で作った木で戻り値 2(3 ではない)、3x2 の一本道で 1、3x3 を作る壁は開けない、戻り値 = 増えた通路の数、同じシードで同じ、確保セルは閉じたまま、3x3 が残らない |
| ループの補充 | 3x2 の一本道で通路 7 本、最後の行・列の壁も見つける、候補が無ければ `GenerationError`、3x3 を作る壁は開けない(横・縦の両方) |

---

## 6. `test_solver.py`(10 本)

### 補助関数

| 関数 | 役目 |
| --- | --- |
| `_build(w, h, passages)` | 指定した通路だけを開けた迷路を作る |
| `_traced_maze()` | 計画書と 4 章のトレースで使った 3 × 3 の迷路 |
| `_distance(m, start, goal)` | **キューを使わずに**最短距離を求める(変化がなくなるまで距離を更新し続ける)。ソルバーと同じ考え方で確かめると、同じ間違いを 2 か所でしても一致してしまうため |
| `_generated_cases()` | 両モード × 20x15 と 9x7 × シード 10 個 × 角の組 2 通り = 80 ケース |

### テスト

| テスト | 守っていること |
| --- | --- |
| `test_shortest_path_of_the_traced_maze` | 4 歩の経路を返す(6 歩の遠回りではない) |
| `test_path_of_a_single_cell` | 入口 = 出口なら `[entry]`、1 つ以下のセルなら `""` |
| `test_to_directions_of_the_traced_path` | `"ESEN"` と `"W"` |
| `test_to_directions_rejects_cells_not_one_step_apart` | 離れたセル・斜めのセルは `KeyError` |
| `test_path_follows_open_walls` | 80 ケースで、文字をたどると開いた壁だけを通って出口に着く |
| `test_path_is_shortest` | 長さが `_distance` と等しい |
| `test_same_maze_same_path` | 2 回解いて同じ |
| `test_reserved_entry_or_exit_raises` | 「42」の上の入口・出口で、メッセージに `8,7` と「42」 |
| `test_unreachable_exit_raises` | 届かない出口で、両方の座標がメッセージに入る |
| `test_solving_prints_nothing` | 何も表示しない |

---

## 7. `test_output.py`(3 本)

| テスト | 守っていること |
| --- | --- |
| `test_maze_writer_encode_structure` | 新しい 2 × 2 で `ff`、`ff`、空行、`0,0`、`1,1`、`SE` の 6 行 |
| `test_maze_writer_encode_hex_formatting` | 15 が小文字の `ff` になる |
| `test_maze_writer_write_file` | `tmp_path` に書いたファイルの中身が `encode` と同じ |

---

## 8. `test_display.py`(14 本)

| テスト | 守っていること |
| --- | --- |
| `test_terminal_renderer_init_valid` | `show_path` と `color_mode` が保存される |
| `test_terminal_renderer_init_invalid_color_mode` | -1 と 4 は `ValueError` |
| `test_terminal_renderer_horizontal_wall` | 新しい 2 × 2 の上の壁が `+---+---+` |
| `test_terminal_renderer_cell_content` | 入口・出口・経路の印。`show_path=False` なら経路の印は出ない |
| `test_terminal_renderer_render_output` | 2 × 2 で 5 行描かれ、1 行目は `+` で始まる |
| `test_apply_action_toggle_path` | `t` で表示が切り替わり、`True` を返す |
| `test_apply_action_change_color` | `c` で 0→1、3→0 |
| `test_apply_action_quit` | `q` で `False` |
| `test_get_user_action_valid` | `t`・`c`・`r`・`q`・`" T "` を正しく読む、間違った入力は聞き直す |
| `test_display_menu_content` | メニューの見出しと 4 つの操作が表示される |
| `test_terminal_renderer_init_with_explicit_params` | 入口・出口・経路を引数で渡せる |
| `test_terminal_renderer_render_shortest_path_override` | `render(maze, shortest_path=...)` で経路を差し替えられる |
| `test_apply_action_regenerate` | コールバックがあれば呼ばれる |
| `test_run_interactive_session_regenerate_and_quit` | `r` → `q` で、コールバックが呼ばれ、描画器の経路が新しくなる |

(`test_terminal_renderer_horizontal_wall` のコメントには、マスクが「9」と「3」とありますが、新しい迷路は全部 15 です。テストの確かめている内容は正しく、コメントだけが実際と違います。)

---

## 9. 注意点・よくある誤解

| 誤解 | 実際 |
| --- | --- |
| テストが通れば正しい | そのテストがバグで失敗するかを確かめるまで分からない(ミューテーションテスト) |
| 1 つの `pytest.raises` に複数の呼び出しを入れてよい | 最初の呼び出しで例外が出た時点で抜けるので、2 つ目以降は実行されない |
| `str(excinfo)` でメッセージが取れる | pytest の包みの文字列になる。`str(excinfo.value)` を使う |
| 正方形の盤面で十分 | x と y の取り違えは、正方形では見つからない |
| テストの中でソルバーと同じ方法で答えを出してよい | 同じ間違いが両方にあると一致してしまう。別の方法で求める |

---

## 関連文書

- 学習ノート:[`pytest-basics.md`](../learning_log/pytest-basics.md)
- 作業ログ(`Docs/work_log/`)の「Stuck」欄 — 実際に起きたバグと、それを捕まえたテスト
- [目次に戻る](README.md)
