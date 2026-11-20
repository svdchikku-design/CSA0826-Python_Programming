"""Task 10 - float vs Decimal totals, timings, rounding policy, and the rate table (dictionary)."""
import random, time
from decimal import Decimal
from calculator import rate_per_litre, payout, validate_entry, money

# ---------- naive float pipeline (what the volunteer's program does) ----------
def f_rate(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)

def f_pay(litres, fat, snf):
    return round(litres * f_rate(fat, snf), 2)

def make_text_entries(n, seed=2026):
    """n entries as clerk text: litres with 2 decimals, fat 3.0-5.0, snf 8.0-9.0 (1 decimal)."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        k = rnd.randint(500, 6000)
        out.append((f"{k // 100}.{k % 100:02d}", f"{rnd.randint(30, 50) / 10:.1f}", f"{rnd.randint(80, 90) / 10:.1f}"))
    return out

print(f"{'n':>8} | {'bank total (exact)':>20} {'float total':>22} {'float - exact':>14} | payments differing by 1 paisa | float(unrounded)->round once | exact(unrounded)->round once")
summary = []
for n in (300, 6000, 150000):
    text = make_text_entries(n)
    dec = [validate_entry(*e) for e in text]                # Decimal entries (exact)
    flo = [(float(a), float(b), float(c)) for a, b, c in text]

    bank = Decimal("0.00")
    for l, f, s in dec:
        bank += payout(l, f, s)                            # each payment rounded to the paisa, then added exactly

    ftotal = 0.0
    for l, f, s in flo:
        ftotal += f_pay(l, f, s)                           # naive loop (not sum(): sum() uses compensated addition)
    mism = sum(1 for (l1, f1, s1), (l2, f2, s2) in zip(dec, flo) if Decimal(str(f_pay(l2, f2, s2))) != payout(l1, f1, s1))

    funr = 0.0
    for l, f, s in flo:
        funr += l * f_rate(f, s)                           # float, rounded only once at the end
    from decimal import Decimal as D
    eunr = sum((l * rate_per_litre(f, s) for l, f, s in dec), D("0"))   # exact, unrounded payments
    print(f"{n:>8} | {bank:>20} {ftotal!r:>22} {ftotal - float(bank):>14.3e} | {mism:>12} | {round(funr, 2):>20}   | {money(eunr):>20}")
    summary.append((n, bank, ftotal, mism, round(funr, 2), money(eunr)))

print("\nRounding policy (one 5-entry example, litres with 2 decimals):")
sample = [("12.35", "3.5", "8.5"), ("7.15", "3.6", "8.5"), ("9.85", "3.7", "8.6"), ("4.45", "3.5", "8.5"), ("20.05", "3.9", "8.5")]
rates = [rate_per_litre(*validate_entry(*e)[1:]) for e in sample]
raw = [validate_entry(*e)[0] * r for e, r in zip(sample, rates)]
rounded = [money(x) for x in raw]
print("  unrounded payments :", [str(x) for x in raw])
print("  rounded payments   :", [str(x) for x in rounded])
print("  sum of rounded (what the bank pays) =", sum(rounded), "| round(sum of unrounded) =", money(sum(raw)))

# ---------- timings (perf_counter) ----------
print(f"\n{'n':>8} {'float core (ms)':>16} {'Decimal core (ms)':>18} {'Decimal incl. validation (ms)':>30}")
for n in (300, 6000, 150000):
    text = make_text_entries(n)
    dec = [validate_entry(*e) for e in text]
    flo = [(float(a), float(b), float(c)) for a, b, c in text]
    t0 = time.perf_counter(); tot = 0.0
    for l, f, s in flo: tot += f_pay(l, f, s)
    t_f = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); tot = Decimal("0")
    for l, f, s in dec: tot += payout(l, f, s)
    t_d = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); tot = Decimal("0")
    for e in text: tot += payout(*validate_entry(*e))
    t_v = (time.perf_counter() - t0) * 1000
    print(f"{n:>8} {t_f:>16.1f} {t_d:>18.1f} {t_v:>30.1f}")

# ---------- Alternative: rate table (dictionary) ----------
text = make_text_entries(150000)
dec = [validate_entry(*e) for e in text]
t0 = time.perf_counter()
table = {}
for fat_i in range(30, 51):
    for snf_i in range(80, 91):
        fat, snf = Decimal(fat_i) / 10, Decimal(snf_i) / 10
        table[(fat, snf)] = rate_per_litre(fat, snf)
t_build = (time.perf_counter() - t0) * 1000
t0 = time.perf_counter(); tot_a = Decimal("0")
for l, f, s in dec: tot_a += money(l * rate_per_litre(f, s))
t_recalc = (time.perf_counter() - t0) * 1000
t0 = time.perf_counter(); tot_b = Decimal("0")
for l, f, s in dec: tot_b += money(l * table[(f, s)])
t_lookup = (time.perf_counter() - t0) * 1000
import sys
print(f"\nRate table: k = {len(table)} (fat, snf) pairs, build {t_build:.2f} ms, dict size {sys.getsizeof(table)} bytes (+ keys/values)")
print(f"150000 entries: recalculate {t_recalc:.1f} ms | table lookup {t_lookup:.1f} ms | same total: {tot_a == tot_b}")
print(f"per entry: recalculate {t_recalc / 150000 * 1000:.3f} us | lookup {t_lookup / 150000 * 1000:.3f} us")
