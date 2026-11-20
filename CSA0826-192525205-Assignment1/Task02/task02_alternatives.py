"""Alternatives to Decimal: integer paise, and float with round() after every addition."""
import sys, time, random
from decimal import Decimal

def total_paise(items):                      # integer paise, parsed from the text (no float involved)
    total = 0
    for a in items:
        rupees, paise = a.split(".")
        total += int(rupees) * 100 + int(paise)
    return total

def total_float_round(items):                # float, round() after every addition
    total = 0.0
    for a in items:
        total = round(total + float(a), 2)
    return total

def total_decimal(items):
    total = Decimal("0")
    for a in items:
        total += Decimal(a)
    return total

def total_float(items):
    total = 0.0
    for a in items:
        total += float(a)
    return total

random.seed(1)
def make(n):
    return [f"{random.randint(1, 20000)//100}.{random.randint(0, 99):02d}" for _ in range(n)]

print("memory per value (sys.getsizeof):")
print("  float   33.40       :", sys.getsizeof(33.40), "bytes")
print("  int     3340 paise  :", sys.getsizeof(3340), "bytes")
print("  Decimal('33.40')    :", sys.getsizeof(Decimal('33.40')), "bytes")
print()
print(f"{'n':>8} {'exact (paise)':>16} {'int paise':>10} {'Decimal':>10} {'float raw':>10} {'float,rnd end':>14} {'float+round':>12} | time per addition (microseconds)")
for n in (300, 6000, 150000):
    items = make(n)
    exact = total_paise(items)                              # reference: integer arithmetic
    res, tims = {}, {}
    for name, fn in (("paise", total_paise), ("dec", total_decimal), ("float", total_float), ("fround", total_float_round)):
        t0 = time.perf_counter(); r = fn(items); tims[name] = (time.perf_counter() - t0) / n * 1e6; res[name] = r
    ok_p = res["paise"] == exact
    ok_d = int(res["dec"] * 100) == exact
    ok_f = res["float"] == exact / 100          # raw float total identical to exact total?
    ok_fe = round(res["float"], 2) == exact / 100  # float total rounded once at the end
    ok_fr = round(res["fround"] * 100) == exact
    print(f"{n:>8} {exact/100:>16.2f} {str(ok_p):>10} {str(ok_d):>10} {str(ok_f):>10} {str(ok_fe):>14} {str(ok_fr):>12} | "
          f"paise {tims['paise']:.3f}  Decimal {tims['dec']:.3f}  float {tims['float']:.3f}  float+round {tims['fround']:.3f}")
    print(f"{'':>8} raw float total = {res['float']!r}   exact = {exact/100:.2f}   float error = {res['float'] - exact/100:.3e}")
