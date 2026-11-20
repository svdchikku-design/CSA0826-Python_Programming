"""Q6 - hand check, call tree for n = 5, growth of call counts versus prediction."""
import sys
from functools import lru_cache
sys.setrecursionlimit(5000)

calls = 0
def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

print("Base case: n <= 1 -> 1 way (zero steps: stay; one step: one way).  Recursive case: ways(n) = ways(n-1) + ways(n-2)")
print("(the last move was either a 1-step from n-1 or a 2-step from n-2)\n")

print("Hand-worked answers (ways(1)=1, ways(2)=2, then each is the sum of the previous two) versus the program:")
hand = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13}
for n, h in hand.items():
    print(f"  n={n}: by hand {h:>2} | program {ways_naive(n):>2} | {'OK' if ways_naive(n) == h else 'WRONG'}")

print("\nCall tree for n = 5 (plain recursion); the number in brackets is the value returned:")
tree_calls = 0
def tree(n, depth=0):
    global tree_calls
    tree_calls += 1
    if n <= 1:
        print("  " * depth + f"ways({n}) -> 1")
        return 1
    print("  " * depth + f"ways({n})")
    v = tree(n - 1, depth + 1) + tree(n - 2, depth + 1)
    print("  " * depth + f"ways({n}) = {v}")
    return v
tree(5)
print(f"\ncalls in the tree: {tree_calls}")
from collections import Counter
cnt = Counter()
def count_args(n):
    cnt[n] += 1
    if n <= 1: return 1
    return count_args(n - 1) + count_args(n - 2)
count_args(5)
print("how many times each argument was computed (n=5):", dict(sorted(cnt.items(), reverse=True)), "-> ways(3) is computed twice, ways(2) three times, ways(1) five times")

print("\nPREDICTION: calls(n) = 2*ways(n) - 1 for plain recursion (every call is a leaf or has two children), and n + 1 for the memoised version.")
print(f"{'n':>4} | {'ways(n)':>10} | {'predicted naive':>16} {'actual naive':>13} | {'predicted memo':>15} {'actual memo':>12}")
for n in (10, 20, 25, 30):
    calls = 0; w = ways_naive(n); cn = calls
    ways_memo.cache_clear(); calls = 0; wm = ways_memo(n); cm = calls
    assert w == wm
    print(f"{n:>4} | {w:>10} | {2 * w - 1:>16} {cn:>13} | {n + 1:>15} {cm:>12}")
