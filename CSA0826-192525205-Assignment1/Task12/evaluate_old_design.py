"""Task 12 A/B - how the ORIGINAL float design (milkrate.py) treats two-decimal readings, versus the new design."""
from datetime import date
from decimal import Decimal as D
import milkrate                     # original module: constants fixed, steps rounded to whole 0.1 % steps
import milkrate_v2 as v2

NOV = date(2026, 11, 5)
print("Normal season, 10 litres, analyser readings with two decimals")
print(f"{'fat':>5} {'snf':>5} | {'old raw steps (fat, snf)':>26} | {'old rate':>9} {'new rate':>9} | {'old amount':>11} {'new amount':>11} {'error (Rs)':>11}")
for fat, snf in (("3.57", "8.53"), ("3.54", "8.46"), ("3.46", "8.54"), ("3.62", "8.58"), ("4.25", "8.75"), ("3.55", "8.45")):
    raw = ((float(fat) - 3.5) / 0.1, (float(snf) - 8.5) / 0.1)
    old_rate = milkrate.rate_per_litre(float(fat), float(snf))
    old_amt = milkrate.payout(10, float(fat), float(snf))
    new_rate = v2.rate_per_litre(D(fat), D(snf), NOV)
    new_amt = v2.payout(D("10"), D(fat), D(snf), NOV)
    print(f"{fat:>5} {snf:>5} | {raw[0]:>12.4f} {raw[1]:>13.4f} | {old_rate:>9.2f} {new_rate:>9} | {old_amt:>11.2f} {new_amt:>11} {float(new_amt) - old_amt:>11.2f}")
print("\nSeason (May) readings: the original module has no way to select 32.00 / 0.45 - its constants are fixed:")
print("  milkrate.rate_per_litre(3.5, 8.5) =", milkrate.rate_per_litre(3.5, 8.5), "| required in season = 32.00")
