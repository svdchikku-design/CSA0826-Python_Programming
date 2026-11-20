"""Task 8 - the algorithm exactly as in the pseudocode, a hand trace, and store-all vs running total."""
import tracemalloc, time
from decimal import Decimal
from calculator import validate_entry, count_steps, rate_per_litre, payout, STD_FAT, STD_SNF, BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE

entries = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3")]
print("HAND TRACE of TEN_DAY_TOTAL for three entries")
print(f"{'i':>2} {'litres':>7} {'fat':>5} {'snf':>5} {'fat_steps':>10} {'snf_steps':>10} {'rate':>7} {'amount':>9} {'total after':>12}")
total = Decimal("0.00")
for i, (l, f, s) in enumerate(entries, 1):
    litres, fat, snf = validate_entry(l, f, s)
    fs, ss = count_steps(fat, STD_FAT), count_steps(snf, STD_SNF)
    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)
    total += amount
    print(f"{i:>2} {litres:>7} {fat:>5} {snf:>5} {fs:>10} {ss:>10} {rate:>7} {amount:>9} {total:>12}")
print("ten-day total =", total)

# ---- Alternative: store every entry then add, versus keep a running total while reading ----
def stored_total(n):
    stored = []
    for i in range(n):                                   # "reading" the entries
        stored.append((Decimal("10.5"), Decimal("3.8"), Decimal("8.6")))
    total = Decimal("0.00")
    for l, f, s in stored:
        total += payout(l, f, s)
    return total

def running_total(n):
    total = Decimal("0.00")
    for i in range(n):
        total += payout(Decimal("10.5"), Decimal("3.8"), Decimal("8.6"))
    return total

print(f"\n{'n':>8} {'time list (ms)':>15} {'time running (ms)':>18} {'peak memory list (KB)':>22} {'peak memory running (KB)':>25}  equal?")
for n in (300, 6000, 150000):
    res = []
    for fn in (stored_total, running_total):
        tracemalloc.start(); t0 = time.perf_counter(); r = fn(n); dt = (time.perf_counter() - t0) * 1000
        peak = tracemalloc.get_traced_memory()[1] / 1024; tracemalloc.stop()
        res.append((r, dt, peak))
    print(f"{n:>8} {res[0][1]:>15.2f} {res[1][1]:>18.2f} {res[0][2]:>22.1f} {res[1][2]:>25.1f}  {res[0][0] == res[1][0]}")
