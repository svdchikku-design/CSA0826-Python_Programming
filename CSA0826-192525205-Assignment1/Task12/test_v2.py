"""Task 12 - tests for both seasons, two-decimal readings and the bonus (hand-calculated expected values)."""
import json
from datetime import date
from decimal import Decimal as D
from milkrate_v2 import rate_per_litre, payout, bonus, ten_day_settlement, season_of, parse_reading, EntryError
from calculator import FAT_MIN, FAT_MAX

NOV, MAY = date(2026, 11, 5), date(2026, 5, 5)
rows = []
def case(label, got, expected):
    ok = str(got) == expected
    rows.append((label, expected, str(got), ok))
    assert ok, (label, got, expected)

def pay(l, f, s, day):
    return payout(D(l), D(f), D(s), day)
def rate(f, s, day):
    return rate_per_litre(D(f), D(s), day)

# seasons (month check)
for d, exp in ((date(2026, 3, 31), "normal"), (date(2026, 4, 1), "season"), (date(2026, 6, 30), "season"), (date(2026, 7, 1), "normal")):
    case(f"season_of {d}", season_of(d), exp)
# normal season, one-decimal (original behaviour preserved)
case("normal: 10 L, 3.5/8.5", pay("10", "3.5", "8.5", NOV), "300.00")
case("normal: 8.5 L, 4.2/8.7  (original test)", pay("8.5", "4.2", "8.7", NOV), "283.90")
case("normal: 12 L, 3.1/8.3   (original test)", pay("12", "3.1", "8.3", NOV), "333.60")
# season
case("season: 10 L, 3.5/8.5", pay("10", "3.5", "8.5", MAY), "320.00")
case("season: rate 4.2/8.7", rate("4.2", "8.7", MAY), "35.75")
case("season: 8.5 L, 4.2/8.7 (half-paise)", pay("8.5", "4.2", "8.7", MAY), "303.88")
case("season: rate fat 2.00 / snf 8.50", rate("2.00", "8.50", MAY), "25.25")
# two-decimal readings
case("normal: rate 3.57/8.53", rate("3.57", "8.53", NOV), "30.37")
case("normal: 10 L, 3.57/8.53", pay("10", "3.57", "8.53", NOV), "303.70")
case("season: rate 3.57/8.53 (32.405 -> up)", rate("3.57", "8.53", MAY), "32.41")
case("season: 10 L, 3.57/8.53", pay("10", "3.57", "8.53", MAY), "324.10")
case("season: rate 3.46/8.44", rate("3.46", "8.44", MAY), "31.64")
# bonus
case("bonus 500 L (not more than 500)", bonus(D("500")), "0.00")
case("bonus 500.01 L", bonus(D("500.01")), "250.01")
case("bonus 520 L", bonus(D("520")), "260.00")
case("bonus 120 L", bonus(D("120")), "0.00")
# whole ten-day settlement: 20 shifts x 26 L, 3.5/8.5, in May
entries = [(date(2026, 5, 1 + i // 2), "26", "3.50", "8.50") for i in range(20)]
litres, pays, b, total = ten_day_settlement(entries)
case("settlement May: litres", litres, "520")
case("settlement May: payments (20 x 832.00)", pays, "16640.00")
case("settlement May: bonus", b, "260.00")
case("settlement May: total", total, "16900.00")
entries_nov = [(date(2026, 11, 1 + i // 2), "26", "3.50", "8.50") for i in range(20)]
case("settlement Nov: total (20 x 780.00 + 260.00)", ten_day_settlement(entries_nov)[3], "15860.00")
entries_small = [(date(2026, 5, 1 + i // 2), "20", "3.50", "8.50") for i in range(20)]   # exactly 400 L: no bonus
case("settlement May 400 L: total (no bonus)", ten_day_settlement(entries_small)[3], "12800.00")
# invalid analyser readings
try:
    parse_reading("3.555", "fat", FAT_MIN, FAT_MAX); got = "accepted"
except EntryError as e:
    got = "rejected"
case("fat 3.555 (3 decimals)", got, "rejected")

print(f"{'Case':<46}{'Expected':>12}{'Actual':>12}  Result")
for label, exp, got, ok in rows:
    print(f"{label:<46}{exp:>12}{got:>12}  {'PASS' if ok else 'FAIL'}")
print(f"\n{len(rows)} cases, all passed: {all(r[3] for r in rows)}")
json.dump([dict(case=a, expected=b, actual=c, ok=d) for a, b, c, d in rows], open("test_results_v2.json", "w"), indent=1)
