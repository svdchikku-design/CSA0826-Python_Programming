"""Q4 - three ways of building the statement, measured; plus the case where CPython cannot optimise +=."""
import time, sys, tracemalloc

def make(n):
    return [f"Item{i}:Rs{i % 50}" for i in range(n)]

def build_plus(parts):                     # (a) repeated += on a local variable
    text = ""
    for p in parts:
        text += p + ";"
    return text

def build_join(parts):                     # (b) list of parts, one join
    return ";".join(parts) + ";"

def build_fstring(n):                      # (c) an f-string for every line, then join
    return "".join([f"Item{i}:Rs{i % 50};" for i in range(n)])

class Statement:                           # += on an ATTRIBUTE: CPython cannot do the in-place trick here
    text = ""
def build_plus_attr(parts):
    st = Statement()
    for p in parts:
        st.text += p + ";"
    return st.text

print("PREDICTION (before measuring): join and f-string+join grow ~linearly; += copies the growing text, so I expect it to be slowest and worse than linear.")
print("\nAverage of 3 runs, seconds (perf_counter):")
print(f"{'lines':>9} | {'a) +=':>9} {'b) join':>9} {'c) f-string+join':>17} {'(c) formatting only':>20} | {'+= on attribute':>16} | same text?")
for n in (1000, 10000, 200000):
    parts = make(n)
    times = {k: [] for k in "abcdf"}
    for _ in range(3):
        t0 = time.perf_counter(); a = build_plus(parts); times["a"].append(time.perf_counter() - t0)
        t0 = time.perf_counter(); b = build_join(parts); times["b"].append(time.perf_counter() - t0)
        t0 = time.perf_counter(); c = build_fstring(n); times["c"].append(time.perf_counter() - t0)
        t0 = time.perf_counter(); _ = [f"Item{i}:Rs{i % 50};" for i in range(n)]; times["f"].append(time.perf_counter() - t0)
        if n <= 50000:
            t0 = time.perf_counter(); d = build_plus_attr(parts); times["d"].append(time.perf_counter() - t0)
    avg = {k: sum(v) / len(v) if v else None for k, v in times.items()}
    attr = f"{avg['d']:.4f}" if avg["d"] is not None else "(skipped: too slow)"
    print(f"{n:>9} | {avg['a']:>9.4f} {avg['b']:>9.4f} {avg['c']:>17.4f} {avg['f']:>20.4f} | {attr:>16} | {a == b == c}")

print("\nThe attribute case alone, to see the growth (each doubling of n):")
prev = None
for n in (5000, 10000, 20000, 40000, 80000):
    parts = make(n)
    t0 = time.perf_counter(); build_plus_attr(parts); t = time.perf_counter() - t0
    print(f"  n={n:>6}: {t:8.4f} s" + (f"   x{t / prev:.2f} for 2x the lines" if prev else ""))
    prev = t
print("  (a factor near 2 means O(n); a factor near 4 means O(n^2) characters copied)")

print("\nTotal characters copied if every += made a full copy (the worst case, n(n+1)/2 * average line length):")
for n in (1000, 10000, 200000):
    L = len(build_join(make(n))) / n
    print(f"  n={n:>7}: about {n * (n + 1) / 2 * L:,.0f} characters  vs  join: {n * L:,.0f} characters")

print("\nIdentity check - += really makes a new object in the general case:")
s = "ab"; before = id(s); t = s; s += "c"
print("  s was shared with t, then s += 'c':  id changed =", id(s) != before, "| t is still", repr(t))
