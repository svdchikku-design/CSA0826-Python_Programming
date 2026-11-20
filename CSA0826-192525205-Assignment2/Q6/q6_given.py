from functools import lru_cache

calls = 0

def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    # TODO 1 (completed): same base case and recursive case as ways_naive, calling ways_memo
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

calls = 0; print("naive:", ways_naive(25), "calls =", calls)
calls = 0; print("memo :", ways_memo(25), "calls =", calls)
import sys
print("\nsys.getrecursionlimit() =", sys.getrecursionlimit())
try:
    print(ways_memo(1000))
except RecursionError as e:
    print("ways_memo(1000) -> RecursionError:", e)
