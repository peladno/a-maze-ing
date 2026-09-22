# Code Guide — All Modules of A-Maze-ing

This collection of documentation explains **all the code written by so and javi, along with its full architecture**, so that both partners or either of us six months later can re-read and fully understand it.

- **No omissions:** Covers every file, class, and function.
- **Starting from first principles:** Explains foundational concepts like "what is a spanning tree?", "what is a queue?", and "how walls are represented with bits".
- **Showing the mechanics:** Includes step-by-step execution traces using real values obtained by running the code.
- **Visualizing relationships:** Illustrates call graphs showing which method calls which.

> **Language / 言語:** [日本語 (Japanese)](README.md) | English

---

## Table of Contents and Reading Order

Reading from top to bottom is recommended, as each chapter builds upon knowledge from preceding chapters.

| Chapter | File                                                | Target Code                                                           | Author                    |
| ------- | --------------------------------------------------- | --------------------------------------------------------------------- | ------------------------- |
| 0       | [Overview](00_overview-en.md)                       | Whole program, module relationships, exceptions, Python prerequisites | —                         |
| 1       | [Maze Data Structure](01_maze_structure-en.md)      | `maze/maze.py`                                                        | so                        |
| 2       | [Configuration Parsing](02_config-en.md)            | `maze/config.py`, `config.txt`                                        | so                        |
| 3       | [Maze Generation](03_generator-en.md)               | `maze/generator.py`                                                   | so                        |
| 4       | [Shortest Path](04_solver-en.md)                    | `maze/solver.py`                                                      | so                        |
| 5       | [Output File](05_output_writer-en.md)               | `output/maze_writer.py`                                               | javi                      |
| 6       | [Display and Controls](06_display-en.md)            | `display/`                                                            | javi                      |
| 7       | [Entry Point](07_entry_point-en.md)                 | `a_maze_ing.py`                                                       | javi                      |
| 8       | [Package and Tooling](08_package_and_tooling-en.md) | `mazegen/`, `pyproject.toml`, `Makefile`, `.gitignore`, etc.          | javi                      |
| 9       | [Tests](09_tests-en.md)                             | `tests/`                                                              | so & javi (partly Claude) |

**Quick reading strategy:** Read the "Single Run Execution Flow" in Chapter 0, then view only the "Architecture Diagram" and "Call Graph" in the chapter of the specific module you want to understand.

---

## Chapter Structure

Every chapter follows this consistent outline:

1. **What this chapter covers**
2. **First principles / foundational concepts** — the core reasoning behind what the module does
3. **Architecture diagram** — components within the module and their relationships
4. **Class and function breakdowns** — signatures, purpose, operational steps, raised exceptions, callers/callees
5. **Trace** — step-by-step execution trace with concrete values
6. **Caveats & common misconceptions**
7. **Related documentation**

---

## Diagram Conventions

| Diagram Type               | Usage                                                                      | Example               |
| -------------------------- | -------------------------------------------------------------------------- | --------------------- |
| ASCII diagrams (monospace) | Shapes and layouts: mazes, bit sequences, cell grids, terminal output      | `+---+---+`           |
| mermaid diagrams           | Flows and relationships: execution order, call graphs, module dependencies | ` ```mermaid ` blocks |

Mermaid diagrams render natively on GitHub. In VS Code, a Markdown extension with Mermaid support is required.

How to read ASCII maze diagrams:

```text
+---+---+        + is a corner, --- is a horizontal wall, | is a vertical wall
| E     |        empty spaces represent open corridors (passable)
+   +---+        E = Entry, X = Exit, . = shortest path, ███ or # = "42" pattern cells
|     X |
+---+---+
```

Coordinates are always `(x, y)`. `x` is the column index (from left: 0, 1, 2, ...), `y` is the row index (from top: 0, 1, 2, ...), and the top-left corner is `(0, 0)`.

---

## Glossary

| Term               | Meaning                                                                      | Chapter |
| ------------------ | ---------------------------------------------------------------------------- | ------- |
| Cell               | A single grid unit in the maze                                               | 1       |
| Wall               | The 4 boundaries (North, East, South, West) of a cell. Closed or open        | 1       |
| Mask (Bitmask)     | The state of a cell's 4 walls packed into a single 4-bit integer (0 to 15)   | 1       |
| Reserved cells     | Cells reserved to draw the "42" logo, kept fully closed                      | 1, 3    |
| Corridor / Passage | An open wall connecting two adjacent cells                                   | 1       |
| Graph              | A structure consisting of vertices (cells) and edges (passages)              | 3       |
| Spanning tree      | A connected acyclic graph covering all vertices. A perfect maze              | 3       |
| Loop (Cycle)       | A path returning to the starting cell without traversing any edge twice      | 3       |
| Dead end           | A cell with only one open passage                                            | 3       |
| Braiding           | Process of opening dead-end walls to create loops                            | 3       |
| Stack              | Last-In-First-Out container (LIFO)                                           | 3, 4    |
| Queue              | First-In-First-Out container (FIFO)                                          | 4       |
| DFS / BFS          | Depth-First Search / Breadth-First Search                                    | 3, 4    |
| Seed               | Random number generator starting state. Identical seed yields identical maze | 3       |
| Exception          | Error notification mechanism (`raise` to throw, `except` to catch)           | 0       |
| Generator          | Function yielding values lazily one at a time (`yield`)                      | 0, 1    |
| Protocol / ABC     | Two ways to define structural typing / interfaces in Python                  | 0, 6    |
| Wheel              | Distributable pre-built package archive (`.whl` file)                        | 8       |

---

## Related Documentation

This guide explains **how the current code works**. The reasoning behind **why it was designed this way** can be found in:

| Document                                                                                            | Contents                                                                    |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [`implementation_plans/architecture-overview.md`](../implementation_plans/architecture-overview.md) | Pipeline overview and work assignments                                      |
| [`implementation_plans/maze-data-structure.md`](../implementation_plans/maze-data-structure.md)     | `Maze` class architecture                                                   |
| [`implementation_plans/config-parser.md`](../implementation_plans/config-parser.md)                 | Config parser design and 31 edge cases                                      |
| [`implementation_plans/generation-algorithm.md`](../implementation_plans/generation-algorithm.md)   | Generator design and decisions Q1–Q11                                       |
| [`implementation_plans/shortest-path-solver.md`](../implementation_plans/shortest-path-solver.md)   | Solver design and decisions S1–S3                                           |
| [`pair_communication/01_kickoff.md`](../pair_communication/01_kickoff.md)                           | Numbered list of all design decisions                                       |
| [`learning_log/`](../learning_log/README.md)                                                        | Conceptual deep-dives (bit manipulation, generators, exceptions, BFS, etc.) |
