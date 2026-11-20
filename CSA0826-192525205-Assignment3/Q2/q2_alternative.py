"""Q2 alternative: the zone grid as a dictionary keyed by (row, col) holding only non-empty zones."""
import time, random, tracemalloc, sys

class ListGrid:
    def __init__(self, rows, cols): self.cells = [[0] * cols for _ in range(rows)]
    def add(self, r, c, n=1): self.cells[r][c] += n
    def get(self, r, c): return self.cells[r][c]
class DictGrid:
    def __init__(self, rows, cols): self.cells = {}; self.rows, self.cols = rows, cols
    def add(self, r, c, n=1): self.cells[(r, c)] = self.cells.get((r, c), 0) + n
    def get(self, r, c): return self.cells.get((r, c), 0)

# same answers
rnd = random.Random(3)
a, b = ListGrid(50, 40), DictGrid(50, 40)
events = [(rnd.randrange(50), rnd.randrange(40)) for _ in range(5000)]
for r, c in events: a.add(r, c); b.add(r, c)
assert all(a.get(r, c) == b.get(r, c) for r in range(50) for c in range(40))
print("list-of-lists and dictionary grids give identical counts for 5,000 boardings on a 50 x 40 grid: True\n")

print(f"{'grid (rows x cols)':>20} {'non-empty zones k':>18} | {'list memory':>12} {'dict memory':>12} | {'list access':>12} {'dict access':>12}")
for rows, cols, k in ((100, 100, 500), (1000, 1000, 1000), (1000, 1000, 100000), (3000, 3000, 1000)):
    cells = [(rnd.randrange(rows), rnd.randrange(cols)) for _ in range(k)]
    tracemalloc.start(); g1 = ListGrid(rows, cols)
    for r, c in cells: g1.add(r, c)
    m1 = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    tracemalloc.start(); g2 = DictGrid(rows, cols)
    for r, c in cells: g2.add(r, c)
    m2 = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    probes = [(rnd.randrange(rows), rnd.randrange(cols)) for _ in range(200000)]
    t0 = time.perf_counter()
    for r, c in probes: g1.get(r, c)
    t1 = (time.perf_counter() - t0) / len(probes) * 1e6
    t0 = time.perf_counter()
    for r, c in probes: g2.get(r, c)
    t2 = (time.perf_counter() - t0) / len(probes) * 1e6
    print(f"{rows:>10} x {cols:<7} {len(set(cells)):>18} | {m1 / 1e6:>10.2f}MB {m2 / 1e6:>10.3f}MB | {t1:>10.3f}us {t2:>10.3f}us")
print("\nA list of lists needs rows x cols cells whether or not anything happened; the dictionary needs only the zones that were used.")
