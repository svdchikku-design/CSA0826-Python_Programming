"""Task 9 - automated tests with assert; also writes test_results.json for the report."""
import json, time
from decimal import Decimal
from calculator import validate_entry, rate_per_litre, payout, ten_day_total, EntryError

results = []

def check_valid(group, label, litres, fat, snf, exp_rate, exp_amount):
    l, f, s = validate_entry(litres, fat, snf)
    rate, amount = rate_per_litre(f, s), payout(l, f, s)
    ok = rate == Decimal(exp_rate) and amount == Decimal(exp_amount)
    results.append(dict(group=group, label=label, inp=f"{litres} L, fat {fat}, snf {snf}",
                        expected=f"rate {exp_rate}, amount {exp_amount}", actual=f"rate {rate}, amount {amount}", ok=ok))
    assert ok, (label, rate, amount)

def check_invalid(group, label, litres, fat, snf, fragment):
    try:
        validate_entry(litres, fat, snf)
        actual, ok = "accepted (WRONG)", False
    except EntryError as e:
        actual, ok = f"rejected: {e}", fragment in str(e)
    results.append(dict(group=group, label=label, inp=f"{litres!r} L, fat {fat!r}, snf {snf!r}",
                        expected=f"rejected ({fragment})", actual=actual, ok=ok))
    assert ok, (label, actual)

t0 = time.perf_counter()
# ---- normal entries in each direction ----
check_valid("Normal", "standard milk", "10", "3.5", "8.5", "30.00", "300.00")
check_valid("Normal", "fat above, SNF above", "8.5", "4.2", "8.7", "33.40", "283.90")
check_valid("Normal", "fat below, SNF below", "12", "3.1", "8.3", "27.80", "333.60")
check_valid("Normal", "fat above, SNF below", "10", "4.0", "8.2", "31.10", "311.00")
check_valid("Normal", "fat below, SNF above", "10", "3.0", "8.9", "29.20", "292.00")
# ---- boundaries ----
check_valid("Boundary", "exactly 3.5 fat / 8.5 SNF", "1", "3.5", "8.5", "30.00", "30.00")
check_valid("Boundary", "lowest fat 2.0", "10", "2.0", "8.5", "24.00", "240.00")
check_valid("Boundary", "highest fat 7.0", "10", "7.0", "8.5", "44.00", "440.00")
check_valid("Boundary", "largest litres 200", "200", "3.5", "8.5", "30.00", "6000.00")
check_valid("Boundary", "smallest litres 0.01", "0.01", "3.5", "8.5", "30.00", "0.30")
# ---- invalid ----
check_invalid("Invalid", "text litres", "eight", "3.5", "8.5", "not a valid number")
check_invalid("Invalid", "comma decimal", "8,5", "3.5", "8.5", "not a valid number")
check_invalid("Invalid", "negative litres", "-5", "3.5", "8.5", "greater than 0")
check_invalid("Invalid", "zero litres", "0", "3.5", "8.5", "greater than 0")
check_invalid("Invalid", "litres above limit", "201", "3.5", "8.5", "above the limit")
check_invalid("Invalid", "fat below 2.0", "10", "1.9", "8.5", "outside the allowed range")
check_invalid("Invalid", "fat above 7.0", "10", "7.1", "8.5", "outside the allowed range")
check_invalid("Invalid", "snf outside range", "10", "3.5", "10.1", "outside the allowed range")
check_invalid("Invalid", "empty text", "", "3.5", "8.5", "not a valid number")
check_invalid("Invalid", "two decimals of fat", "10", "3.55", "8.5", "at most 1 decimal")

# ---- five entries whose total was worked out by hand ----
five = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3"), ("10", "4.0", "8.2"), ("7.5", "3.8", "8.6")]
hand = {"10": 300.00}
amounts = [payout(*validate_entry(*e)) for e in five]
total = ten_day_total(five)
assert [str(a) for a in amounts] == ["300.00", "283.90", "333.60", "311.00", "236.25"], amounts
assert total == Decimal("1464.75"), total
results.append(dict(group="Hand total", label="5 entries", inp="; ".join(f"{a} L {b}/{c}" for a, b, c in five),
                    expected="300.00 + 283.90 + 333.60 + 311.00 + 236.25 = 1464.75",
                    actual=" + ".join(str(a) for a in amounts) + f" = {total}", ok=True))
elapsed = (time.perf_counter() - t0) * 1000

print(f"{'Group':<10}{'Case':<28}{'Expected':<42}{'Result'}")
for r in results:
    print(f"{r['group']:<10}{r['label']:<28}{r['expected'][:40]:<42}{'PASS' if r['ok'] else 'FAIL'}")
print(f"\n{len(results)} cases, all passed: {all(r['ok'] for r in results)}   (whole suite ran in {elapsed:.2f} ms)")
json.dump(results, open("test_results.json", "w"), indent=1)
