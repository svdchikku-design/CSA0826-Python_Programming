"""Q1 alternative: match-case and a (upper limit, decision) table, versus if-elif-else, for k slabs."""
import time, bisect

def build_elif(k):
    """if-elif chain with k slabs: units <= 10, <= 20, ... then a final else."""
    lines = ["def f(units):"]
    for i in range(1, k):
        lines.append(f"    {'if' if i == 1 else 'elif'} units <= {i * 10}: return {i}")
    lines.append(f"    else: return {k}")
    ns = {}; exec("\n".join(lines), ns); return ns["f"], len(lines)

def build_match(k):
    lines = ["def f(units):", "    match units:"]
    for i in range(1, k):
        lines.append(f"        case u if u <= {i * 10}: return {i}")
    lines.append(f"        case _: return {k}")
    ns = {}; exec("\n".join(lines), ns); return ns["f"], len(lines)

def build_table(k):
    table = [(i * 10, i) for i in range(1, k)]
    def f(units):
        for limit, decision in table:
            if units <= limit:
                return decision
        return k
    return f, table

def build_bisect(k):
    limits = [i * 10 for i in range(1, k)]
    def f(units):
        return bisect.bisect_left(limits, units) + 1
    return f, limits

def per_call_us(f, units, reps):
    t0 = time.perf_counter()
    for _ in range(reps):
        f(units)
    return (time.perf_counter() - t0) / reps * 1e6

print("The real rule has k = 3 slabs. Generated rules with more slabs show how the cost grows.")
print("Worst case = value that falls in the LAST slab (every test is tried); best case = first slab.")
print(f"{'k':>5} | {'elif worst':>11} {'match worst':>12} {'table worst':>12} {'bisect worst':>13} | {'elif best':>10} {'table best':>11} | source lines elif/match | table entries")
for k in (3, 10, 100, 1000):
    fe, le = build_elif(k); fm, lm = build_match(k); ft, tab = build_table(k); fb, lim = build_bisect(k)
    worst, best = k * 10 + 5, 5
    reps = 200000 if k <= 10 else (20000 if k == 100 else 2000)
    for u in (worst, best, 55):                      # all four must agree
        assert fe(u) == fm(u) == ft(u) == fb(u), (k, u)
    print(f"{k:>5} | {per_call_us(fe, worst, reps):>9.3f}us {per_call_us(fm, worst, reps):>10.3f}us {per_call_us(ft, worst, reps):>10.3f}us {per_call_us(fb, worst, reps):>11.3f}us | "
          f"{per_call_us(fe, best, reps):>8.3f}us {per_call_us(ft, best, reps):>9.3f}us | {le:>5}/{lm:<5}           | {len(tab)}")
