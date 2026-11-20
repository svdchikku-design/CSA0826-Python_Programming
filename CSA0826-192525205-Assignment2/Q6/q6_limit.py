"""Q6 - recursion limit, deployment decision, and the three versions at n = 1000."""
import sys, time, tracemalloc
from functools import lru_cache

@lru_cache(maxsize=None)
def ways_memo(n):
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_loop(n):
    """Keeps only the last two values: O(n) time, O(1) extra space, no recursion."""
    prev, cur = 1, 1                      # ways(0), ways(1)
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur

def ways_naive_calls(n):
    return 2 * ways_loop(n) - 1           # number of calls the plain recursion WOULD make (proved on small n)

print("sys.getrecursionlimit() =", sys.getrecursionlimit())
print("\n1) Cold cache (fresh program state):")
ways_memo.cache_clear()
try:
    ways_memo(1000)
    print("   ways_memo(1000) worked")
except RecursionError as e:
    print("   ways_memo(1000) -> RecursionError:", e)
print("   reason: ways_memo(1000) calls ways_memo(999) before it can add anything, ..., down to ways_memo(1): about 1000 nested frames, which hits the limit of", sys.getrecursionlimit())

print("\n2) Warm cache (the program of the assignment first called ways_memo(25)):")
ways_memo.cache_clear(); ways_memo(25)
try:
    r = ways_memo(1000); print("   ways_memo(1000) worked: the cache already holds n = 0..25, so the nesting is only about 975 deep (< limit); digits:", len(str(r)))
except RecursionError as e:
    print("   RecursionError:", e)

print("\n3) Largest n that works with a cold cache and the default limit:")
lo, hi = 1, 5000
while lo < hi:
    mid = (lo + hi + 1) // 2
    ways_memo.cache_clear()
    try:
        ways_memo(mid); lo = mid
    except RecursionError:
        hi = mid - 1
print("   n =", lo)

print("\n4) Raising the limit (sys.setrecursionlimit(5000)):")
sys.setrecursionlimit(5000)
ways_memo.cache_clear()
t0 = time.perf_counter(); r_memo = ways_memo(1000); t_memo = time.perf_counter() - t0      # timed without the memory tracer
ways_memo.cache_clear(); tracemalloc.start(); ways_memo(1000)
mem_memo = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
print(f"   works for n = 1000 ({len(str(r_memo))} digits); time {t_memo * 1e6:.0f} us, peak memory {mem_memo / 1024:.0f} KB (cache of {ways_memo.cache_info().currsize} entries)")
sys.setrecursionlimit(1000)

print("\nThe three versions at n = 1000:")
t0 = time.perf_counter(); r_loop = ways_loop(1000); t_loop = time.perf_counter() - t0
tracemalloc.start(); ways_loop(1000); mem_loop = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
calls_naive = ways_naive_calls(1000)
# measured speed of the plain version, used to estimate its running time
import q6_speed
rate = q6_speed.calls_per_second()
print(f"  plain recursion : would make {len(str(calls_naive))}-digit number of calls (about 10^{len(str(calls_naive)) - 1}); at the measured {rate:,.0f} calls/second that is more than 10^{len(str(calls_naive)) - 9} seconds (the universe is about 4x10^17 seconds old) - it cannot finish. NOT RUN.")
print(f"  memoised        : {t_memo * 1e6:8.0f} us (cold cache, recursion limit raised), peak {mem_memo / 1024:6.0f} KB, 1001 calls")
print(f"  loop, last two  : {t_loop * 1e6:8.0f} us, peak {mem_loop / 1024:6.1f} KB, 999 additions")
print("  memo == loop for n=1000:", r_memo == r_loop)
print("  loop and memo agree for n = 1..300:", all(ways_loop(n) == ways_memo(n) for n in range(1, 301)))
print("  loop for n = 100000 (no limit problem):", end=" ")
t0 = time.perf_counter(); big = ways_loop(100000); print(f"about {int(big.bit_length() * 0.30103)} digits in {time.perf_counter() - t0:.3f} s")
