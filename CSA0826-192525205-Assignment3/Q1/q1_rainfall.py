"""Q1 - village rain-gauge station: slicing, weekly totals, max/min, moving average, dry days, edge cases."""
import random
from datetime import date, timedelta

def make_readings(n, seed=2026):
    rnd = random.Random(seed)
    return [0.0 if rnd.random() < 0.6 else round(rnd.uniform(0.1, 60.0), 1) for _ in range(n)]

def weekly_totals(readings):
    """Totals of consecutive 7-day blocks using slicing; the last block may be shorter."""
    return [round(sum(readings[i:i + 7]), 1) for i in range(0, len(readings), 7)]

def max_min_positions(readings):
    """(max value, index, min value, index) of the first occurrences; None for an empty list."""
    if not readings:
        return None
    hi, lo = max(readings), min(readings)
    return hi, readings.index(hi), lo, readings.index(lo)

def moving_average_naive(readings, w=7):
    """Average of every full window of w days, by summing each slice again."""
    return [sum(readings[i:i + w]) / w for i in range(len(readings) - w + 1)]

def moving_average_running(readings, w=7):
    """Same result with a running sum: add the new day, subtract the day that left."""
    if len(readings) < w:
        return []
    total = sum(readings[:w])
    out = [total / w]
    for i in range(w, len(readings)):
        total += readings[i] - readings[i - w]
        out.append(total / w)
    return out

def dry_days(readings, start=date(2026, 1, 1)):
    return [(i, start + timedelta(days=i)) for i, v in enumerate(readings) if v == 0]

if __name__ == "__main__":
    # ---------------- slicing explained on a small list ----------------
    demo = list(range(1, 31))                       # 30 'days' with the reading equal to the day number
    print("demo list (day numbers 1..30):", demo)
    print("demo[7:14]  ->", demo[7:14], "  (index 7 up to but not including 14: the 2nd week, days 8-14)")
    print("demo[-7:]   ->", demo[-7:], "  (the last 7 values)")
    print("demo[::7]   ->", demo[::7], "  (every 7th value starting at index 0: days 1, 8, 15, 22, 29)")

    # ---------------- the year ----------------
    readings = make_readings(365)
    print("\nreadings: n =", len(readings), "| first 10:", readings[:10])
    weeks = weekly_totals(readings)
    print("number of weekly blocks:", len(weeks), "(52 full weeks + a block of", len(readings[364:]), "day)")
    print("first 8 weekly totals:", weeks[:8])
    full = weeks[:52]                                # the 1-day last block is not a week, so it is not ranked
    wet, dry = max(full), min(full)
    print(f"wettest full week: week {full.index(wet) + 1} with {wet} mm | driest full week: week {full.index(dry) + 1} with {dry} mm")
    hi, hi_i, lo, lo_i = max_min_positions(readings)
    print(f"maximum daily rainfall {hi} mm at index {hi_i} (day {hi_i + 1}, {date(2026, 1, 1) + timedelta(days=hi_i)}); minimum {lo} mm first at index {lo_i}")
    ma_n, ma_r = moving_average_naive(readings), moving_average_running(readings)
    print("moving average windows:", len(ma_n), "| first 5:", [round(x, 2) for x in ma_n[:5]])
    print("naive and running-sum results agree (max difference):", max(abs(a - b) for a, b in zip(ma_n, ma_r)))
    dd = dry_days(readings)
    print("dry days:", len(dd), "| first 5:", [(i, str(d)) for i, d in dd[:5]])

    # ---------------- edge cases ----------------
    print("\nEdge cases:")
    for label, data in (("empty list", []), ("3 values", [1.0, 2.0, 3.0]), ("exactly 7 values", [7.0] * 7)):
        print(f"  {label:<17}: weekly={weekly_totals(data)} max/min={max_min_positions(data)} "
              f"naive={moving_average_naive(data)} running={moving_average_running(data)} dry={dry_days(data)}")
