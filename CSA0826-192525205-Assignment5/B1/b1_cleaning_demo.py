"""B1.1: every problem on a small file - data before and after cleaning (rules from common/cleaning.py)."""
import csv, sys
sys.path.insert(0, "../common")
from cleaning import clean_rows

with open("small_all_problems.csv", newline="") as f:
    raw = list(csv.DictReader(f))
print("BEFORE cleaning (13 raw rows):")
print(f"{'#':>2} {'station':<8} {'date':<11} {'hr':>2} {'pm25':>6} {'pm10':>5} {'no2':>5} {'temp':>5}   problem")
problems = {1: "blank PM2.5", 2: "'NA' PM2.5", 3: "negative PM2.5", 4: "impossible PM2.5 (9999)", 5: "text '--' in PM10", 6: "ok", 7: "exact duplicate of row 6",
            8: "station 'ADYAR ' (case, space) and date 02/10/2026", 9: "hour 24 does not exist", 10: "Manali temperature in Fahrenheit (84.2 F)", 11: "Manali PM2.5 missing", 12: "Manali temperature 'NA'"}
for i, r in enumerate(raw):
    print(f"{i:>2} {r['station']:<8} {r['date']:<11} {r['hour']:>2} {r['pm25']:>6} {r['pm10']:>5} {r['no2']:>5} {r['temp']:>5}   {problems.get(i, '')}")
stats = {}
clean = clean_rows(raw, stats)
print(f"\nAFTER cleaning ({len(clean)} rows; None = still missing):")
print(f"{'station':<8} {'date':<11} {'hr':>2} {'pm25':>6} {'pm10':>6} {'no2':>6} {'temp_C':>7}")
for r in clean:
    f = lambda v: "None" if v is None else f"{v:.1f}"
    print(f"{r['station']:<8} {r['date']:<11} {r['hour']:>2} {f(r['pm25']):>6} {f(r['pm10']):>6} {f(r['no2']):>6} {f(r['temp']):>7}")
print("\ncleaning report:")
for k in sorted(stats): print(f"  {k}: {stats[k]}")
print("\nexpected by hand: Adyar 00 keeps 48.0; hours 01,02 (blank, NA) are filled with 48.0 (forward fill, gap 1 and 2);")
print("hour 03 (-5 -> missing) is filled with 48.0 (gap 3); hour 04 (9999 -> missing) stays missing (gap would be 4, limit is 3);")
print("hour 05 PM10 '--' is filled with the previous valid PM10 (90.0); duplicate hour 06 and the hour-24 row are removed; Manali temp 84.2 F = 29.0 C.")
checks = {("Adyar", "2026-10-01", 1, "pm25"): 48.0, ("Adyar", "2026-10-01", 3, "pm25"): 48.0, ("Adyar", "2026-10-01", 4, "pm25"): None,
          ("Adyar", "2026-10-01", 5, "pm10"): 90.0, ("Manali", "2026-10-01", 0, "temp"): 29.0}
index = {(r["station"], r["date"], r["hour"]): r for r in clean}
for (s, d, h, c), want in checks.items():
    got = index[(s, d, h)][c]; print(f"  check {s} {d} {h:02d} {c}: got {got}, expected {want} -> {'OK' if got == want else 'WRONG'}"); assert got == want
assert ("Adyar", "2026-10-01", 6) in index and len([r for r in clean if r["hour"] == 6 and r["date"] == "2026-10-01"]) == 1
assert not any(r["hour"] == 24 for r in clean)
print("all checks passed")
