"""Q5 experiments: timing of the three versions, list versus generator memory, generator pitfalls."""
import time, sys, tracemalloc
from q5_sensors import make_temps, clean_loop, clean_comp, clean_map, LOW_ERR, HIGH_ERR

def best(f, reps):
    b = 1e9
    for _ in range(reps):
        t0 = time.perf_counter(); f(); b = min(b, time.perf_counter() - t0)
    return b

print("1. Time to clean and convert (seconds, best of 5/3/3)")
print(f"{'readings':>10} | {'for + append':>13} {'comprehension':>14} {'map + filter':>13} | loop/comp  map/comp")
rows = []
for n in (10_000, 100_000, 1_000_000):
    data = make_temps(n)
    reps = 5 if n < 1_000_000 else 3
    a, b, c = best(lambda: clean_loop(data), reps), best(lambda: clean_comp(data), reps), best(lambda: clean_map(data), reps)
    assert clean_loop(data) == clean_comp(data) == clean_map(data)
    rows.append((n, a, b, c))
    print(f"{n:>10} | {a:>13.4f} {b:>14.4f} {c:>13.4f} | {a / b:>8.2f}x {c / b:>8.2f}x")
print("identical results for all three sizes: True")
print("note: the comprehension version walks the data twice (one list for Celsius, one for Fahrenheit); a single comprehension of tuples would walk it once.")
def one_pass(data):
    return [(c, round(c * 9 / 5 + 32, 2)) for c in data if LOW_ERR <= c <= HIGH_ERR]
data = make_temps(1_000_000)
print(f"   one-pass comprehension of (C, F) pairs at 1,000,000: {best(lambda: one_pass(data), 3):.4f} s")

print("\n2. Memory: list comprehension versus generator expression (1,000,000 readings)")
valid_list = [c for c in data if LOW_ERR <= c <= HIGH_ERR]
valid_gen = (c for c in data if LOW_ERR <= c <= HIGH_ERR)
print(f"   sys.getsizeof(list comprehension result) = {sys.getsizeof(valid_list):>10,} bytes (just the pointers; the {len(valid_list):,} floats are shared with the input)")
print(f"   sys.getsizeof(generator expression)      = {sys.getsizeof(valid_gen):>10,} bytes (a generator stores its position, not its values - whatever the input size)")
for n in (10_000, 100_000, 1_000_000):
    d = make_temps(n)
    tracemalloc.start(); s1 = sum([c for c in d if LOW_ERR <= c <= HIGH_ERR]); p1 = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    tracemalloc.start(); s2 = sum(c for c in d if LOW_ERR <= c <= HIGH_ERR); p2 = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    assert abs(s1 - s2) < 1e-6
    print(f"   n = {n:>9,}: peak extra memory  sum([list comp]) = {p1 / 1024:>9.1f} KB | sum(generator) = {p2 / 1024:>6.2f} KB")

print("\n3. Time of the alternative: sum of valid readings by list comprehension vs generator expression")
print(f"{'readings':>10} | {'sum(list comp)':>15} {'sum(generator)':>15}")
for n in (10_000, 100_000, 1_000_000):
    d = make_temps(n)
    t1 = best(lambda: sum([c for c in d if LOW_ERR <= c <= HIGH_ERR]), 5); t2 = best(lambda: sum(c for c in d if LOW_ERR <= c <= HIGH_ERR), 5)
    print(f"{n:>10} | {t1:>14.5f}s {t2:>14.5f}s  (generator {t2 / t1:.2f}x)")

print("\n4. A generator can be used only once, and cannot be indexed or measured:")
g = (c for c in [3.0, 4.0, 5.0])
print("   first sum(g) =", sum(g), "| second sum(g) =", sum(g), "(exhausted)")
try:
    len((c for c in [1, 2]))
except TypeError as e:
    print("   len(generator) ->", e)
try:
    gen2 = (c for c in [1, 2]); gen2[0]
except TypeError as e:
    print("   generator[0]   ->", e)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.4)); ns = [r[0] for r in rows]
ax.plot(ns, [r[1] for r in rows], "o-", label="for + append"); ax.plot(ns, [r[2] for r in rows], "s-", label="list comprehension"); ax.plot(ns, [r[3] for r in rows], "^-", label="map + filter + lambda")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("readings n"); ax.set_ylabel("time (s)"); ax.set_title("Cleaning and converting temperatures"); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("chart_cleaning.png", dpi=130)
