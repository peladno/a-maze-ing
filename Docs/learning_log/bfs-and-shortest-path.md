# Queues and breadth-first search — why taking the oldest cell first finds the shortest path

| | |
| --- | --- |
| **Author / 筆者** | so |
| **Date / 日付** | 2026-09-17 |
| **Where it is used / 使い所** | `maze/solver.py` (`shortest_path`), subject §IV.5, §V — plan: `Docs/implementation_plans/shortest-path-solver.md` §3 |
| **Written with AI? / AI 併用** | yes — drafted with Claude before writing the solver, after the concept of a queue was explained; the timings in §5.3 were measured on the school machine (§VII の記録用) |
| **Confidence / 理解度** | — (fill after answering §8 / §8 に答えてから記入) |

---

## 1. In one sentence / 一言でいうと

**EN** — A queue hands things back in the order they were put in, so a search that always continues from the oldest
cell in a queue reaches cells in order of distance — and the first time it reaches the exit, it has used a
shortest route.
**JA** — キューは入れた順に取り出す入れ物。だから、キューで一番古いセルから常に続ける探索は、セルに**近い順に**
たどり着く。**出口に初めて着いたとき、それは最短の道で着いている。**

## 2. Why it is needed / なぜ必要か

**EN** — The output file ends with the **shortest** path from entry to exit (§IV.5), and the display shows it
(§V). In the default mode the maze has loops, so there is usually more than one way through, and a search that
simply finds *a* way can return a detour. The stack used to carve the maze does exactly that. Changing one thing —
which end the next cell is taken from — turns it into a search that is shortest by construction.
**JA** — 出力ファイルの最後には、入口から出口への**最短**経路を書く(§IV.5)。表示でもそれを見せる(§V)。
既定モードの迷路にはループがあるので、通り抜ける道はふつう複数ある。「ある道」を見つけるだけの探索は、遠回りを
返しうる。迷路を掘るのに使ったスタックが、まさにそうなる。**次のセルをどちらの端から取るか**という 1 点を変える
だけで、作りからして最短になる探索に変わる。

## 3. What you need to know first / 前提として知っておくこと

**EN** — Two things from the generator. First, the maze is a graph: cells are the points, and an open wall joins two
of them; `Maze.open_neighbours` lists the cells one step away. Second, `_carve_spanning_tree` walks that kind of
graph with a **stack** — a `list` used with `append` and `pop`, always continuing from the cell added last — and a
`visited` set marked the moment a cell is added. The search in this note has the same skeleton; only the container
changes.
**JA** — 生成器から 2 つ。1 つ目:迷路はグラフで、セルが点、開いた壁が 2 つの点をつなぐ線。`Maze.open_neighbours`
が 1 歩先のセルを並べる。2 つ目:`_carve_spanning_tree` はそういうグラフを**スタック**でたどった。`list` を
`append` と `pop` で使い、常に**最後に**入れたセルから続け、セルを入れた瞬間に `visited` に印を付けた。
このノートの探索も骨組みは同じで、**変わるのは入れ物だけ**。

## 4. How it works / 仕組み

### 4.1 Stack and queue / スタックとキュー

**EN** — Both are containers you put things into and take things out of. The only difference is **which item comes
out next**. A stack gives back the newest item, like a pile of plates: the plate put on last is taken first
(LIFO, last in, first out). A queue gives back the oldest, like a line at a till: whoever joined first leaves first
(FIFO, first in, first out).
**JA** — どちらも、ものを入れて取り出す入れ物。違いは**次にどれが出てくるか**だけ。スタックは一番新しいものを返す。
積んだ皿のように、最後に置いた皿を最初に取る(LIFO:後入れ先出し)。キューは一番古いものを返す。レジの行列のように、
最初に並んだ人が最初に抜ける(FIFO:先入れ先出し)。

```text
put in A, then B, then C — take one out

stack                              queue

put → [ A  B  C ]                  put → [ A  B  C ]
                ↑                        ↑
take ← C   (the newest)            take ← A   (the oldest)
left   [ A  B ]                    left   [ B  C ]
```

### 4.2 A queue in Python: `collections.deque` / Python のキュー:`collections.deque`

**EN** — A `list` is a good stack, because `append`, `[-1]` and `pop()` all work at the end. It is a poor queue:
taking the first item with `pop(0)` makes the list move every remaining item one place to the left, so emptying a
list of n items from the front costs about n² moves. `collections.deque` ("deck", a double-ended queue) adds and
removes at either end without moving the rest. As a queue, two methods are all it takes: `append` to join at the
back, `popleft` to leave from the front.
**JA** — `list` はスタックとしては良い。`append`・`[-1]`・`pop()` がすべて末尾で済むから。キューとしては向かない。
`pop(0)` で先頭を取ると、リストは残りの要素を全部 1 つずつ左にずらす。n 個の要素を先頭から空にするには、
およそ n² 回の移動がかかる。`collections.deque`(「デック」、両端キュー)は、残りを動かさずにどちらの端でも
出し入れできる。キューとして使うなら、メソッドは 2 つで足りる。後ろに並ぶ `append` と、前から抜ける `popleft`。

```text
>>> from collections import deque
>>> line = deque(["Alice"])
>>> line.append("Bob")
>>> line.append("Carol")
>>> line.popleft()
'Alice'
>>> line
deque(['Bob', 'Carol'])
>>> len(line)
2
>>> deque().popleft()
IndexError: pop from an empty deque
```

### 4.3 Breadth-first search / 幅優先探索

**EN** — Start with the entry alone in the queue, marked as reached. Repeat: take the oldest cell out; for each
open neighbour not reached yet, mark it reached, note which cell it came from, and add it to the back. Because a
cell joins the line only after every cell already waiting, all cells one step away leave before any cell two steps
away, all of those before any three steps away, and so on. That is the whole proof: **cells leave the queue in
order of distance**, so the first time the exit leaves, no shorter route to it can still be waiting.
**JA** — 入口だけをキューに入れ、到達済みの印を付けて始める。これを繰り返す:一番古いセルを取り出し、まだ到達して
いない開いた隣それぞれに、到達済みの印を付け、どのセルから来たかを記録し、後ろに並べる。セルは、すでに待っている
すべてのセルの**後ろ**にしか並べないので、1 歩のセルは全部、2 歩のセルより先に抜ける。2 歩のセルは全部、3 歩の
セルより先に抜ける。証明はこれで全部。**セルは距離の順にキューを出ていく**ので、出口が初めて出ていくとき、
それより短い道で出口に着くものは、もう待っていない。

**EN** — The search does not store paths. It stores, for each cell, the one cell it was reached from. The path is
recovered afterwards by following those records back from the exit to the entry, then reversing.
**JA** — 探索は経路を保存しない。保存するのは、各セルについて「どのセルから来たか」の 1 つだけ。経路は後から、
その記録を出口から入口までたどり、反転して取り出す。

## 5. Figure, example, trace / 図・具体例・トレース

### 5.1 The maze / 迷路

```text
E = entry (0,0), X = exit (2,0); numbers on the right = distance from E

      x=0 x=1 x=2                  x=0 x=1 x=2
    +---+---+---+                +---+---+---+
y=0 | E     | X |            y=0 | 0   1 | 4 |
    +   +   +   +                +   +   +   +
y=1 |   |       |            y=1 | 1 | 2   3 |
    +   +---+   +                +   +---+   +
y=2 |           |            y=2 | 2   3   4 |
    +---+---+---+                +---+---+---+

short way:  (0,0) (1,0) (1,1) (2,1) (2,0)               ESEN     4 steps
long way:   (0,0) (0,1) (0,2) (1,2) (2,2) (2,1) (2,0)   SSEENN   6 steps
```

### 5.2 Queue against stack, on the same maze / 同じ迷路でキューとスタック

**EN** — Neighbours are taken in the order `Maze.neighbours` yields them: N, E, S, W. Both runs mark a cell when it
is added. The queue column was produced by running it on the real `Maze`.
**JA** — 隣は `Maze.neighbours` の順、N・E・S・W で取る。どちらもセルを入れたときに印を付ける。キューの列は実際の
`Maze` で実行して得たもの。

```text
                queue (BFS)                          stack (DFS)
take   container after adding          dist   take   container after adding
-----  ------------------------------  ----   -----  -----------------------
(0,0)  (1,0) (0,1)                       0    (0,0)  (1,0) (0,1)
(1,0)  (0,1) (1,1)                       1    (0,1)  (1,0) (0,2)
(0,1)  (1,1) (0,2)                       1    (0,2)  (1,0) (1,2)
(1,1)  (0,2) (2,1)                       2    (1,2)  (1,0) (2,2)
(0,2)  (2,1) (1,2)                       2    (2,2)  (1,0) (2,1)
(2,1)  (1,2) (2,0) (2,2)                 3    (2,1)  (1,0) (2,0) (1,1)
(1,2)  (2,0) (2,2)                       3    (1,1)  (1,0) (2,0)
(2,0)  exit                              4    (2,0)  exit

came from:  (2,0)←(2,1)←(1,1)←(1,0)←(0,0)        came from:  (2,0)←(2,1)←(2,2)←(1,2)←(0,2)←(0,1)←(0,0)
path:       ESEN, 4 steps                         path:       SSEENN, 6 steps
```

**EN** — Read the "dist" column: 0, 1, 1, 2, 2, 3, 3, 4. The queue takes cells in order of distance. The stack
dives down the left side because `(0,1)` was added last, and reaches the exit the long way.
**JA** — 「dist」の列を読む:0, 1, 1, 2, 2, 3, 3, 4。キューは距離の順にセルを取り出している。スタックは `(0,1)` を
最後に入れたので左側を潜っていき、遠回りで出口に着く。

### 5.3 Why `pop(0)` matters / `pop(0)` がなぜ問題か

**EN** — Emptying a container from the front, measured:
**JA** — 入れ物を先頭から空にする時間を測った:

| items / 要素数 | `list.pop(0)` | `deque.popleft()` |
| --- | --- | --- |
| 10,000 | 5.7 ms | 0.3 ms |
| 100,000 | **645 ms** | 3.0 ms |

**EN** — Ten times the items made the list about a hundred times slower, and the deque about ten times: n² against
n. A 300x300 maze already has 90,000 cells.
**JA** — 要素を 10 倍にすると、list は約 100 倍、deque は約 10 倍遅くなった。n² と n の違い。300x300 の迷路で、
セルはすでに 9 万個ある。

## 6. Common misconceptions / よくある誤解・ハマりどころ

| Misconception / 誤解 | Reality / 実際は |
| --- | --- |
| Any search that reaches the exit gives the shortest path / 出口に着く探索なら、どれでも最短が得られる | Only if cells come out in order of distance. The stack of §5.2 reaches the exit in 6 steps where 4 exist. / セルが距離の順に出てくる場合だけ。§5.2 のスタックは、4 歩の道があるのに 6 歩で着く。 |
| A queue is a special Python type called `queue` / キューは `queue` という Python の特別な型 | A queue is a way of using a container. `collections.deque` is the usual one; the `queue` module is for sharing work between threads, which we do not need. / キューは入れ物の使い方のこと。ふつうは `collections.deque` を使う。`queue` モジュールはスレッド間で仕事を受け渡すためのもので、この課題には要らない。 |
| `list.pop(0)` is fine for a queue / キューには `list.pop(0)` で十分 | It works, but moves every remaining item each time: 645 ms against 3 ms at 100,000 items (§5.3). / 動くが、毎回残り全部を動かす。10 万要素で 645 ms 対 3 ms(§5.3)。 |
| Mark a cell as reached when it is taken out / セルは取り出したときに到達済みにする | Then the same cell can be added several times before it is taken, and a later, longer route can overwrite where it came from. Mark it when it is added — the same rule as `visited` in the carving. / そうすると、取り出される前に同じセルが何度も入り、後から来た長い道が「どこから来たか」を上書きしうる。入れたときに印を付ける。掘る段階の `visited` と同じ規則。 |
| The queue holds the path / キューに経路が入っている | The queue holds cells waiting to be explored. The path is rebuilt afterwards from the "came from" records (§4.3). / キューにあるのは、これから調べるセル。経路は後から「どこから来たか」の記録で組み立てる(§4.3)。 |
| BFS has to visit the whole maze / BFS は迷路全体を回らないといけない | It can stop as soon as the exit is taken out; §5.2 stops with `(2,2)` still waiting. / 出口を取り出した時点で止めてよい。§5.2 では `(2,2)` がまだ待っている状態で止まる。 |

## 7. How we use it here / この課題での使い方

**EN** — `shortest_path(maze, entry, exit)` in `maze/solver.py` runs this search over `Maze.open_neighbours` and
returns the cells of the path, which the renderer marks (§V). `to_directions` turns consecutive cells into
`N`/`E`/`S`/`W` for the last line of the output file (§IV.5). If the queue empties before the exit is taken out,
there is no path, and `SolveError` says why. The contract, the trace on the real `Maze` and the decisions S1–S3 are
in `shortest-path-solver.md`.
**JA** — `maze/solver.py` の `shortest_path(maze, entry, exit)` が、`Maze.open_neighbours` の上でこの探索を行い、
経路のセルを返す。描画はそのセルに印を付ける(§V)。`to_directions` は隣り合うセルを `N`/`E`/`S`/`W` に変え、
出力ファイルの最終行にする(§IV.5)。出口を取り出す前にキューが空になれば経路は無く、`SolveError` がその理由を
伝える。契約、実際の `Maze` でのトレース、決定 S1〜S3 は `shortest-path-solver.md` にある。

## 8. Self-check / 確認問題

- [ ] Q1. With A, B, C put in that order, which comes out first from a stack, and which from a queue? /
  A, B, C の順に入れたとき、スタックとキューからそれぞれ最初に出てくるのはどれか。
- [ ] Q2. Why is `pop()` fast on a `list` but `pop(0)` slow? / `list` の `pop()` は速いのに、`pop(0)` はなぜ遅いか。
- [ ] Q3. In one or two sentences, why is the first arrival at the exit a shortest route in BFS? /
  BFS で出口に初めて着いた道が最短である理由を、1〜2 文で。
- [ ] Q4. On the maze of §5.1, which path does a stack find, and why does it go that way? /
  §5.1 の迷路で、スタックはどの道を見つけるか。なぜその道になるか。
- [ ] Q5. What goes wrong if a cell is marked reached only when it is taken out? /
  セルを取り出したときにだけ到達済みにすると、何がまずいか。
- [ ] Q6. The queue empties before the exit comes out. What does that mean for the maze? /
  出口が出てくる前にキューが空になった。迷路について何が言えるか。

## 9. Still unclear / まだ分かっていないこと

- [ ] **EN** — When several shortest paths exist, which one BFS returns depends on the neighbour order. Is that
  worth documenting for the user, or only for us? / **JA** — 最短経路が複数あるとき、BFS がどれを返すかは隣の順番
  で決まる。利用者向けに説明すべきか、自分たち向けだけでよいか。
- [ ] **EN** — Dijkstra's algorithm and A* also find shortest paths. Where exactly do they stop being overkill? /
  **JA** — ダイクストラ法と A* も最短経路を求める。どこから大げさでなくなるのか。

## 10. Related / 関連

- `Docs/implementation_plans/shortest-path-solver.md`
- `Docs/implementation_plans/generation-algorithm.md` §3.1 — the stack-based carving this note contrasts with
- `Docs/learning_log/maze-generation-algorithms.md`
- `Docs/learning_log/python-generators.md` — why `open_neighbours` can be walked only once
- `Docs/pair_communication/01_kickoff.md` § 3.8

## 11. Sources

- Python tutorial, "Using Lists as Queues" — https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues
- Python library reference, `collections.deque` — https://docs.python.org/3/library/collections.html#collections.deque
