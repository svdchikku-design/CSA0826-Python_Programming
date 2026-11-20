"""Q4 experiments: membership, common students (nested loops, sorted walk, set &), memory."""
import time, random, tracemalloc, sys

def best(f, reps=5):
    b = 1e9
    for _ in range(reps):
        t0 = time.perf_counter(); f(); b = min(b, time.perf_counter() - t0)
    return b

print("1. membership test x in list vs x in set (register numbers as 9-digit strings)")
print(f"{'n':>9} | {'list, x present (middle)':>25} {'list, x absent (worst)':>23} {'set, x present':>15} {'set, x absent':>14}")
rows = []
for n in (10_000, 100_000, 1_000_000):
    nums = [f"{192000000 + i}" for i in range(n)]
    s = set(nums); mid, absent = nums[n // 2], "000000000"
    reps = 200 if n <= 100_000 else 20
    def tm(f):
        t0 = time.perf_counter()
        for _ in range(reps): f()
        return (time.perf_counter() - t0) / reps * 1e6
    a, b = tm(lambda: mid in nums), tm(lambda: absent in nums)
    c, d = tm(lambda: mid in s), tm(lambda: absent in s)
    rows.append((n, a, b, c, d))
    print(f"{n:>9} | {a:>22.2f} us {b:>20.2f} us {c:>12.3f} us {d:>11.3f} us")
print("(the list time grows with n: O(n); the set time does not: O(1) average)")

print("\n2. finding the students common to two electives of n students each (overlap about 10 %)")
def make(n, seed=1):
    r = random.Random(seed)
    pool = r.sample(range(190_000_000, 190_000_000 + 10 * n), 2 * n - n // 10)
    a = [str(x) for x in pool[:n]]
    b = [str(x) for x in pool[n - n // 10:2 * n - n // 10]]
    return a, b
def nested(a, b):
    return [x for x in a for y in b if x == y]
def nested_break(a, b):
    out = []
    for x in a:
        for y in b:
            if x == y:
                out.append(x); break
    return out
def sorted_walk(a, b):
    a, b = sorted(a), sorted(b); i = j = 0; out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]: out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]: i += 1
        else: j += 1
    return out
def by_set(a, b):
    return sorted(set(a) & set(b))
print(f"{'n = m':>9} | {'nested loops':>13} {'sorted walk':>12} {'set &':>9} | same result")
prev = None
for n in (500, 1000, 2000, 4000):
    a, b = make(n)
    t1 = best(lambda: nested(a, b), 1); t2 = best(lambda: sorted_walk(a, b), 3); t3 = best(lambda: by_set(a, b), 3)
    assert sorted(nested(a, b)) == sorted_walk(a, b) == by_set(a, b)
    print(f"{n:>9} | {t1:>12.4f}s {t2 * 1e3:>10.3f}ms {t3 * 1e3:>7.3f}ms | True" + (f"   (nested: x{t1 / prev:.1f} for 2x n)" if prev else ""))
    prev = t1
print("larger sizes (nested loops would take hours; measured only the two fast methods):")
print(f"{'n = m':>9} | {'sorted walk':>12} {'set &':>9} {'nested loops (extrapolated from n=4000 x n^2)':>48}")
t_ref = prev
for n in (10_000, 100_000, 1_000_000):
    a, b = make(n)
    t2 = best(lambda: sorted_walk(a, b), 1); t3 = best(lambda: by_set(a, b), 1)
    est = t_ref * (n / 4000) ** 2
    print(f"{n:>9} | {t2:>11.3f}s {t3:>8.3f}s {est:>40,.0f} s  (~{est / 3600:,.1f} hours)")

print("\n3. memory of a list and a set of 1,000,000 register numbers (container only, strings shared)")
nums = [f"{192000000 + i}" for i in range(1_000_000)]
print(f"   list: {sys.getsizeof(nums):>11,} bytes | set: {sys.getsizeof(set(nums)):>11,} bytes (hash table with spare room)")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.4))
ns = [r[0] for r in rows]
ax.plot(ns, [r[2] for r in rows], "o-", label="list, x absent"); ax.plot(ns, [r[1] for r in rows], "s-", label="list, x in middle"); ax.plot(ns, [r[4] for r in rows], "^-", label="set")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("register numbers n"); ax.set_ylabel("microseconds per test"); ax.set_title("x in list versus x in set"); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("chart_membership.png", dpi=130)
