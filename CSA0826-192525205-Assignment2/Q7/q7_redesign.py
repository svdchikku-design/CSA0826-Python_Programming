"""Q7 C/D/E - redesign of the temple-steps counter, predictions recorded BEFORE measuring, then validation.

Property exploited: ways(n) depends only on ways(n-1) and ways(n-2) (overlapping sub-problems, optimal substructure),
so solve the sub-problems once, in increasing order (bottom-up), keeping only the last two values.
"""
import time, sys, tracemalloc
from functools import lru_cache

# ---------------------------------------------------------------- original (Q6 plain recursion)
calls = 0
def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

# ---------------------------------------------------------------- redesign: bottom-up, two variables
additions = 0
def ways_bottom_up(n):
    """Number of ways to climb n steps (1 or 2 at a time). O(n) additions, O(1) extra space, no recursion."""
    global additions
    prev, cur = 1, 1                     # ways(0), ways(1)
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur      # ways(k) = ways(k-1) + ways(k-2)
        additions += 1
    return cur

# ---------------------------------------------------------------- the middle option kept for comparison (Q6 memo)
@lru_cache(maxsize=None)
def ways_memo(n):
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

# ---------------------------------------------------------------- PREDICTIONS (fixed before any measurement of the redesign)
PREDICT = {
    "n=30 operations": "2,692,537 calls -> 29 additions (a reduction of about 92,800x)",
    "n=30 time": "naive about 0.25 s (from the diagnosis) -> a few microseconds (about 10^4-10^5 x faster)",
    "n=1000": "naive impossible; redesign about 30-150 microseconds, no RecursionError",
    "extra space": "O(1): two integers, instead of a 1001-entry cache or 1000 stack frames",
    "n=100000": "the loop still works (no recursion limit); time grows faster than linearly because the integers have ~20,000 digits",
}
print("PREDICTIONS (written before measuring):")
for k, v in PREDICT.items():
    print(f"  {k:<16}: {v}")

# ---------------------------------------------------------------- validation: same inputs, counts, times
print("\nCorrectness: redesign equals the original for every n = 0..30:", end=" ")
assert all(ways_naive(n) == ways_bottom_up(n) for n in range(0, 31))
print("True")
print("Redesign equals the hand values for n = 1..6 (1, 2, 3, 5, 8, 13):", [ways_bottom_up(n) for n in range(1, 7)])

def best_time(f, n, reps):
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        for _ in range(reps):
            f(n)
        best = min(best, (time.perf_counter() - t0) / reps)
    return best

print(f"\n{'n':>4} | {'original calls':>15} {'redesign additions':>19} {'call reduction':>15} | {'original time':>14} {'redesign time':>14} {'speed-up':>10}")
for n in (10, 20, 25, 30):
    calls = 0; t0 = time.perf_counter(); ways_naive(n); t_o = time.perf_counter() - t0; c = calls
    additions = 0; ways_bottom_up(n); a = additions
    t_r = best_time(ways_bottom_up, n, 2000)
    print(f"{n:>4} | {c:>15} {a:>19} {c / a:>14.0f}x | {t_o * 1e3:>11.3f} ms {t_r * 1e6:>11.3f} us {t_o / t_r:>9.0f}x")

print("\nLarger inputs (the original cannot run these):")
sys.setrecursionlimit(1000)
print(f"{'n':>8} | {'redesign time':>14} {'additions':>10} {'peak memory':>12} | memoised recursion (default limit)")
for n in (1000, 10_000, 100_000):
    reps = 200 if n == 1000 else (10 if n == 10_000 else 1)
    t = best_time(ways_bottom_up, n, reps)
    additions = 0; tracemalloc.start(); r = ways_bottom_up(n); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    ways_memo.cache_clear()
    try:
        ways_memo(n); memo = "works"
    except RecursionError:
        memo = "RecursionError"
    print(f"{n:>8} | {t * 1e6:>11.1f} us {additions:>10} {peak / 1024:>9.1f} KB | {memo}")

print("\nWhere the original (memoised) design is still preferable - many queries of different n:")
Q = 1000
t0 = time.perf_counter(); 
for n in range(1, Q + 1): ways_bottom_up(n)
t_each = time.perf_counter() - t0
ways_memo.cache_clear(); sys.setrecursionlimit(5000)
t0 = time.perf_counter()
for n in range(1, Q + 1): ways_memo(n)
t_memo = time.perf_counter() - t0
t0 = time.perf_counter(); table = [1, 1]
for k in range(2, Q + 1): table.append(table[-1] + table[-2])
t_table = time.perf_counter() - t0
additions = 0
for n in range(1, Q + 1): ways_bottom_up(n)
print(f"  answering ways(1)..ways({Q}) once each:  redesign called {Q} times: {t_each * 1e3:.2f} ms ({additions} additions) | memoised (shared cache): {t_memo * 1e3:.2f} ms (1000 additions) | one pass building a table: {t_table * 1e3:.3f} ms (999 additions)")
sys.setrecursionlimit(1000)
