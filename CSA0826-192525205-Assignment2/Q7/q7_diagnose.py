"""Q7 A - diagnose the Q6 plain recursion: where the work is, what grows, what is repeated."""
import time
from collections import Counter

calls = Counter()
def ways_naive(n):
    calls[n] += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

N = 25
ways_naive(N)
total = sum(calls.values())
print(f"ways_naive({N}) made {total} calls but only {len(calls)} different arguments exist (0..{N}).")
print(f"=> {total - len(calls)} calls ({(total - len(calls)) / total * 100:.3f} %) recompute an answer that was already computed.\n")
print("Calls per argument (how often the same sub-problem is solved):")
print(f"{'argument k':>11} {'times ways(k) was computed':>28}")
for k in (25, 24, 23, 20, 15, 10, 5, 3, 2, 1, 0):
    print(f"{k:>11} {calls[k]:>28}")
print("\nWhere is the work done? Leaves (n <= 1) versus inner calls:")
leaves = calls[0] + calls[1]
print(f"  leaf calls (n = 0 or 1): {leaves}  ({leaves / total * 100:.1f} % of all calls) - each only returns 1, so the whole answer 121393 is built by adding 1s")
print(f"  inner calls            : {total - leaves}")

print("\nHow does the count grow with the input?")
prev = None
print(f"{'n':>4} {'calls':>10} {'ratio to previous n':>20} {'time (s)':>10}")
for n in range(20, 33, 2):
    calls.clear(); t0 = time.perf_counter(); ways_naive(n); dt = time.perf_counter() - t0
    c = sum(calls.values())
    print(f"{n:>4} {c:>10} {(c / prev) if prev else float('nan'):>20.3f} {dt:>10.4f}")
    prev = c
print("(two steps of n multiply the calls by about 2.618 = phi^2, i.e. each step by phi = 1.618: exponential growth, O(phi^n))")
print("time is proportional to the number of calls: it grows by the same factor, so n = 40 would take about half a minute (0.25 s x 1.618^10) and n = 1000 is impossible.")
