"""Task 6 alternative: duplicates found by searching a list of earlier registrations versus a set / dictionary lookup."""
import random, time, tracemalloc

def dedupe_list(regs):
    seen, dups = [], 0
    for r in regs:
        if r in seen: dups += 1           # linear search of all earlier registrations: O(n)
        else: seen.append(r)
    return len(seen), dups

def dedupe_set(regs):
    seen, dups = set(), 0
    for r in regs:
        if r in seen: dups += 1           # hash lookup: O(1) average
        else: seen.add(r)
    return len(seen), dups

def make(n, seed=5):
    rnd = random.Random(seed); base = [str(192000000 + i) for i in range(int(n * 0.9))]
    regs = base + [rnd.choice(base) for _ in range(n - len(base))]      # about 10 % duplicate registrations
    rnd.shuffle(regs); return regs

print("Both use the same validation; only the duplicate test differs. About 10 % of registrations are duplicates.\n")
print(f"{'n':>8} {'list search (s)':>16} {'set lookup (s)':>15} {'ratio':>8} {'list x per doubling':>20} | {'list mem (KB)':>14} {'set mem (KB)':>13} | same result")
prev = None; per_cmp = []
for n in (2000, 4000, 8000, 16000, 32000):
    regs = make(n)
    t0 = time.perf_counter(); a = dedupe_list(regs); tl = time.perf_counter() - t0
    t0 = time.perf_counter(); b = dedupe_set(regs); ts = time.perf_counter() - t0
    tracemalloc.start(); dedupe_list(regs); ml = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    tracemalloc.start(); dedupe_set(regs); ms = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    comps = n * (n - 1) / 2 * 0.9 * 0.9; per_cmp.append(tl)
    print(f"{n:>8} {tl:>16.4f} {ts:>15.5f} {tl/ts:>7.0f}x {('x%.1f' % (tl/prev)) if prev else '-':>20} | {ml/1024:>14.0f} {ms/1024:>13.0f} | {a == b}")
    prev = tl
k = per_cmp[-1] / 32000**2
for n in (100000, 1000000):
    print(f"  extrapolated list search at n = {n:>9,}: about {k*n*n:,.0f} s = {k*n*n/60:,.1f} minutes (time grows as n^2; not run)")
t0 = time.perf_counter(); dedupe_set(make(1000000)); print(f"  measured set lookup at n = 1,000,000: {time.perf_counter()-t0:.2f} s")
