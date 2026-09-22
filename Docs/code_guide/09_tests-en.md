# 9. Tests — `tests/`

|               |                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Authors**   | so (Config, Maze, first half of Generator), javi (Display, Output), Claude (second half of Generator, Solver, requested by so) |
| **Execution** | `make test` (`poetry run pytest -q`)                                                                                           |
| **Subject**   | §III.3 (Tests are not deliverables, but serve as completion criteria)                                                          |

## What You'll Learn in This Chapter

- pytest fundamentals (test discovery, `assert`, verifying exceptions, capturing output)
- What each of the 6 test files and 135 tests guards
- The role of test helper functions
- The philosophy of "breaking things to verify" (Mutation Testing)

---

## 1. Core Concepts

### 1.1 pytest Fundamentals

| Mechanism             | Syntax                                                    | Meaning                                                                         |
| --------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Test discovery        | `def test_...():` inside `tests/test_*.py`                | pytest automatically discovers and executes it                                  |
| Verification          | `assert expression`                                       | If the expression is false, test fails and inspects values in detail            |
| Verifying exceptions  | `with pytest.raises(SomeError) as excinfo:`               | Fails if `SomeError` is not raised. Verify the message via `str(excinfo.value)` |
| Capturing output      | Add `capsys` to test arguments, `capsys.readouterr().out` | Captures and inspects stdout / stderr output                                    |
| Mocking input         | `monkeypatch.setattr("builtins.input", ...)`              | Makes `input()` return predetermined values instead of waiting                  |
| Temporary directories | Add `tmp_path` to test arguments                          | Provides a fresh empty directory for each test run                              |

→ Learning Log: [`pytest-basics.md`](../learning_log/pytest-basics.md)

### 1.2 "A Test That Has Never Failed Proves Nothing"

Passing tests do not necessarily mean the test suite is capable of **catching bugs**. A test that merely calls `print` will always pass.

To verify test effectiveness, this project employed **Mutation Testing**:

1. Copy the genuine production code and intentionally introduce a single subtle bug (e.g. changing `popleft()` to `pop()`, or `>= 2` to `>= 1`).
2. Run the test suite.
3. If any test **fails**, the test suite is capable of detecting that specific bug (killed mutant). If all tests still pass, the bug slipped through undetected (survived mutant).

Results (from work logs):

| Target    | Injected Mutants | Detected                                                              |
| --------- | ---------------- | --------------------------------------------------------------------- |
| Generator | 44 variations    | 43 detected (the remaining 1 cannot change the resulting maze output) |
| Solver    | 12 variations    | 12 detected (1 detected via test timeout / infinite loop)             |

---

## 2. Test Files Overview

| File                | Tests | Target                              |
| ------------------- | ----- | ----------------------------------- |
| `test_maze.py`      | 18    | `maze/maze.py` (Chapter 1)          |
| `test_config.py`    | 43    | `maze/config.py` (Chapter 2)        |
| `test_generator.py` | 47    | `maze/generator.py` (Chapter 3)     |
| `test_solver.py`    | 10    | `maze/solver.py` (Chapter 4)        |
| `test_output.py`    | 3     | `output/maze_writer.py` (Chapter 5) |
| `test_display.py`   | 14    | `display/` (Chapter 6)              |

There is no full automated integration test for `main()` in `a_maze_ing.py` because it requires an interactive terminal session.

---

## 3. `test_maze.py` (18 Tests)

| Category       | Test Name                                           | What It Guards                                                                                           |
| -------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `Direction`    | `test_opposite_is_symmetric`                        | The opposite of the opposite returns to the original direction                                           |
|                | `test_delta_and_opposite_cancel_out`                | Adding `delta` of a direction and its opposite yields `(0, 0)`                                           |
| Creation       | `test_new_maze_has_given_size_and_all_walls_closed` | Dimensions are accurate, and all wall masks are initialized to 15                                        |
|                | `test_invalid_size_raises_value_error`              | Dimensions $\le 0$ raise `ValueError`                                                                    |
|                | `test_new_maze_has_no_open_wall`                    | A newly created maze has zero open walls in any direction                                                |
| Bounds         | `test_contains_only_accepts_positions_inside_grid`  | Returns true only inside the grid (detects x/y inversion on non-square grids)                            |
|                | `test_walls_at_raises_outside_grid`                 | Querying outside the grid raises `OutOfBoundsError`                                                      |
| `open_passage` | `test_open_passage_updates_both_cells`              | Clears wall bits symmetrically on both sides                                                             |
|                | `test_open_passage_raises_when_not_adjacent`        | Non-adjacent cells raise `NotAdjacentError`                                                              |
|                | `test_open_passage_is_idempotent`                   | Opening an already open wall leaves it unchanged                                                         |
|                | `test_open_passage_raises_outside_grid`             | Coordinates outside the grid raise `OutOfBoundsError`                                                    |
|                | `test_open_passage_refuses_reserved_cells`          | Reserved cells raise `MazeError`                                                                         |
| Neighbours     | `test_neighbours_stops_at_the_edge`                 | Inner cell (1,1) has 4 neighbours in N, E, S, W order; corner (0,0) filters out out-of-bounds neighbours |
|                | `test_neighbours_skips_reserved_cells`              | Reserved cells are omitted from neighbour lists                                                          |
|                | `test_neighbours_raises_outside_grid`               | Iterating neighbours outside the grid raises `OutOfBoundsError`                                          |
|                | `test_open_neighbours_only_returns_carved_cells`    | Only returns neighbours reachable through open passages                                                  |
| `rows`         | `test_rows_has_one_tuple_per_row`                   | Yields exactly one tuple per row                                                                         |
|                | `test_rows_agrees_with_walls_at`                    | `rows` yields the exact same values as `walls_at`                                                        |

---

## 4. `test_config.py` (43 Tests)

| Category               | What It Guards (Summary of Test Names)                                                                                                                                                                                                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Syntax (`_read_pairs`) | Lines without `=` error, parses valid config pairs, ignores blank lines and comments, strips whitespace, values may contain `=`, preserves `#` inside values, preserves unrecognized keys, case-insensitivity on keys, `\r\n` line endings, empty keys error, duplicate keys error                                 |
| Error Messages         | Includes filename and line number, duplicate key error messages reference both line numbers                                                                                                                                                                                                                        |
| `_as_filename`         | Accepts valid filenames, rejects empty strings                                                                                                                                                                                                                                                                     |
| `_as_bool`             | Accepts `True` / `False`, rejects other spellings                                                                                                                                                                                                                                                                  |
| `_as_int`              | Accepts valid integers, rejects non-numeric strings, rejects values below minimum, **minimum 1 requires `must be a positive integer` whereas other minimums format as `must be at least N`** (asserts exact message), **minimum 0 still enforces range check**, accepts negative numbers when no minimum specified |
| `_as_coord`            | Accepts `x,y`, rejects 1 or 3 numbers, rejects non-integer / negative coordinates, allows whitespace around coordinates                                                                                                                                                                                            |
| `parse_config`         | Parses complete valid config, lists all missing mandatory keys, `SEED` defaults to `None`, **`SEED=0` remains `0`**, rejects entry/exit outside grid bounds, rejects entry equal to exit                                                                                                                           |
| `load_config`          | Successfully reads valid config files, handles missing files, handles directory path passed as file, **reads committed `config.txt` without error**                                                                                                                                                                |

**Why tests for `SEED=0` and "minimum 0" exist:** If written as `if seed:` or `if minimum:`, `0` is treated as falsy (equivalent to `None`), introducing a silent bug. These specific tests ensure `0` is respected as a valid numeric value.

**Design behind `test_comments_are_ignored`:** If a test comment were `# a comment`, it has no `=` sign; thus, even if comment stripping logic were deleted, the parser would fail with a syntax error (falsely passing the test). By using `# WIDTH=99` and comparing the **entire** parsed dictionary, the test only fails if comment stripping actually breaks (Work Log 9/5).

---

## 5. `test_generator.py` (47 Tests)

### Helper Functions

| Function                                | Purpose                                                                                                                                   |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `_count_passages(m)`                    | Counts open passages (counting East and South only to avoid double counting)                                                              |
| `_count_reachable(m)`                   | Counts cells reachable from (0,0) (independent traversal implementation separate from solver)                                             |
| `_open_all_but(w, h, closed, reserved)` | Builds a grid with all walls open **except** specified closed walls. Used in 3x3 tests to easily set up "only this wall is closed" states |

### Test Classification

| Phase               | What It Guards                                                                                                                                                                                                                                                                                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__init__`          | Preserves passed seed (including 0), generates new seed if none provided (distinct across generators), enforces keyword-only `perfect` and `seed`, rejects dimensions < 1 (including negative $\times$ negative), rejects dimensions too small for default mode, accepts 3x2 and 2x3, allows 1-column mazes in perfect mode                                |
| Carving             | Passages = cells − 1, all cells reachable, deterministic maze for identical seeds, supports 1-column mazes, supports 300 $\times$ 300, reserved cells remain completely closed, raises `GenerationError("only 3 of 6")` if reserved cells isolate uncarved cells                                                                                           |
| `generate`          | Produces perfect maze when requested, repeated calls on same instance yield identical maze, default mode produces Pac-Man playable board (tested on 20 seeds: full connectivity, loops $\ge 2$, dead ends $\le 2$), no 3x3 open areas, minimal board yields exactly 2 loops, deterministic with same seed, **outputs nothing to stdout/stderr** (`capsys`) |
| "42" Pattern        | Omitted when size < 9x7, centered on 20x15, keeps 4 corners and center open across 9x7 to 29x29, pattern cells remain fully closed, works correctly on both modes for 9x7                                                                                                                                                                                  |
| Dead Ends           | Accurately identifies tree dead ends `[(0,0), (1,0), (0,2)]`, does not count dead ends facing solely "42" pattern cells, eliminates dead ends after braiding                                                                                                                                                                                               |
| 3x3 Open Areas      | Counts all 12 potential 3x3 blocks, detects completion on the final wall (both horizontal and vertical), 2 closed walls prevent completion, 3x2 has no 3x3 blocks, skips out-of-bounds blocks, blocks containing reserved cells never complete                                                                                                             |
| Braiding            | Handcrafted tree returns 2 (not 3), 3x2 corridor returns 1, refuses to open walls that would form a 3x3 open area, return value matches count of added passages, deterministic with same seed, reserved cells remain intact, no 3x3 areas remain                                                                                                           |
| Supplementary Loops | 3x2 corridor produces 7 passages, identifies walls on boundary rows/columns, raises `GenerationError` if no candidates remain, prevents opening walls that would form 3x3 open areas (horizontal and vertical)                                                                                                                                             |

---

## 6. `test_solver.py` (10 Tests)

### Helper Functions

| Function                    | Purpose                                                                                                                                                                                   |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_build(w, h, passages)`    | Creates a maze opening only specified passages                                                                                                                                            |
| `_traced_maze()`            | 3 $\times$ 3 maze used in architecture plan and Chapter 4 execution trace                                                                                                                 |
| `_distance(m, start, goal)` | Computes shortest path distance **without using a queue** (iteratively updates distances until convergence). Testing with an independent algorithm prevents identical flaws from matching |
| `_generated_cases()`        | Both modes $\times$ 20x15 and 9x7 $\times$ 10 seeds $\times$ 2 corner pairings = 80 test cases                                                                                            |

### Tests

| Test Name                                             | What It Guards                                                                                      |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `test_shortest_path_of_the_traced_maze`               | Returns 4-step path (rather than 6-step detour)                                                     |
| `test_path_of_a_single_cell`                          | Entry == Exit yields `[entry]`; $\le 1$ cell yields `""`                                            |
| `test_to_directions_of_the_traced_path`               | Returns `"ESEN"` and `"W"`                                                                          |
| `test_to_directions_rejects_cells_not_one_step_apart` | Disjoint or diagonal cells raise `KeyError`                                                         |
| `test_path_follows_open_walls`                        | Across 80 cases, following direction characters traverses only open passages and terminates at exit |
| `test_path_is_shortest`                               | Path length matches `_distance`                                                                     |
| `test_same_maze_same_path`                            | Solving twice yields identical path                                                                 |
| `test_reserved_entry_or_exit_raises`                  | Entry/exit on "42" pattern raises with `8,7` and "42" in message                                    |
| `test_unreachable_exit_raises`                        | Unreachable exit raises with both coordinates in message                                            |
| `test_solving_prints_nothing`                         | Solver produces no stdout/stderr output                                                             |

---

## 7. `test_output.py` (3 Tests)

| Test Name                                | What It Guards                                                                  |
| ---------------------------------------- | ------------------------------------------------------------------------------- |
| `test_maze_writer_encode_structure`      | Fresh 2 $\times$ 2 produces 6 lines: `ff`, `ff`, blank line, `0,0`, `1,1`, `SE` |
| `test_maze_writer_encode_hex_formatting` | Value 15 formats as lowercase `ff`                                              |
| `test_maze_writer_write_file`            | File written to `tmp_path` exactly matches `encode` output                      |

---

## 8. `test_display.py` (14 Tests)

| Test Name                                              | What It Guards                                                             |
| ------------------------------------------------------ | -------------------------------------------------------------------------- |
| `test_terminal_renderer_init_valid`                    | `show_path` and `color_mode` are stored                                    |
| `test_terminal_renderer_init_invalid_color_mode`       | Modes -1 and 4 raise `ValueError`                                          |
| `test_terminal_renderer_horizontal_wall`               | Top wall of fresh 2 $\times$ 2 renders as `+---+---+`                      |
| `test_terminal_renderer_cell_content`                  | Entry, exit, and path markers. Path markers hidden when `show_path=False`  |
| `test_terminal_renderer_render_output`                 | 2 $\times$ 2 renders 5 lines, line 1 starting with `+`                     |
| `test_apply_action_toggle_path`                        | `t` toggles visibility and returns `True`                                  |
| `test_apply_action_change_color`                       | `c` cycles colors 0→1, 3→0                                                 |
| `test_apply_action_quit`                               | `q` returns `False`                                                        |
| `test_get_user_action_valid`                           | Reads `t`, `c`, `r`, `q`, `" T "`; reprompts on invalid input              |
| `test_display_menu_content`                            | Menu title and 4 actions are displayed                                     |
| `test_terminal_renderer_init_with_explicit_params`     | Entry, exit, and path can be passed as explicit arguments                  |
| `test_terminal_renderer_render_shortest_path_override` | `render(maze, shortest_path=...)` overrides stored path                    |
| `test_apply_action_regenerate`                         | Invokes callback when provided                                             |
| `test_run_interactive_session_regenerate_and_quit`     | Sequence `r` → `q` invokes regeneration callback and updates renderer path |

_(Note: In `test_terminal_renderer_horizontal_wall`, the test comment mentions masks "9" and "3", but fresh mazes are initialized to 15. The test assertions are correct; only the comment diverged from the final implementation.)_

---

## 9. Caveats & Common Misconceptions

| Misconception                                                 | Reality                                                                                                         |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| A passing test implies code correctness                       | You cannot be certain until you verify that introducing a bug makes the test fail (Mutation Testing)            |
| Multiple assertions can be grouped into one `pytest.raises`   | Execution aborts at the first raised exception; subsequent calls are never executed                             |
| `str(excinfo)` returns the error message                      | It returns pytest's internal wrapper string. Use `str(excinfo.value)`                                           |
| Testing on square grids is sufficient                         | Inversion of x and y cannot be detected on symmetric square grids                                               |
| Using the solver algorithm in tests to verify results is fine | If the algorithm has an inherent bug, both will produce the same incorrect result. Use independent verification |

---

## Related Documentation

- Learning Log: [`pytest-basics.md`](../learning_log/pytest-basics.md)
- Work Log (`Docs/work_log/`) "Stuck" sections — Real bugs encountered during development and the tests that caught them
- [Back to Table of Contents](README-en.md)
