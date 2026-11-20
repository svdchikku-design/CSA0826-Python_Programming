"""A2 alternatives measured: drop / forward-fill / median-fill for missing readings, effect on daily means; and normalisation demo."""
import csv, glob, statistics, sys, time
sys.path.insert(0, "../common")
from cleaning import clean_file, min_max, z_scores
from datagen import make_station_rows, STATIONS, BASE_PM25

# truth: the same station-month generated WITHOUT faults; observed: the same readings with 10% randomly blanked
def daily_means(rows, how):
    out = {}
    by = {}
    for r in rows: by.setdefault(r["date"], []).append(r["pm25"])
    for d, vals in by.items():
        ok = [v for v in vals if v is not None]
        out[d] = sum(ok) / len(ok) if ok else None
    return out
import random
rnd = random.Random(5)
station, base = "Manali", 88
truth = [{"date": r[1], "hour": int(r[2]), "pm25": float(r[3])} for r in make_station_rows(station, base, seed=9, faults=False)]
def blank(rows, frac, burst=False):
    rows = [dict(r) for r in rows]
    idx = set()
    if not burst:
        idx = set(rnd.sample(range(len(rows)), int(len(rows) * frac)))
    else:                                        # bursts: whole stretches of 6 hours lost (sensor down)
        while len(idx) < int(len(rows) * frac):
            s = rnd.randrange(len(rows) - 6); idx |= set(range(s, s + 6))
    for i in idx: rows[i]["pm25"] = None
    return rows
def fill_prev(rows, limit=3):
    last, gap = None, 0
    for r in rows:
        if r["pm25"] is None:
            if last is not None and gap < limit: r["pm25"] = last; gap += 1
        else: last, gap = r["pm25"], 0
    return rows
def fill_median(rows):
    m = statistics.median(r["pm25"] for r in rows if r["pm25"] is not None)
    for r in rows:
        if r["pm25"] is None: r["pm25"] = m
    return rows
tm = daily_means(truth, "")
print("Error of the daily mean PM2.5 against the true value (mean absolute error over 31 days, in ug/m3); truth = faultless data, then values blanked")
print(f"{'pattern':<34}{'drop (average what is left)':>28}{'forward fill (max 3 h)':>24}{'fill with median':>18}")
for name, frac, burst in (("5% scattered single hours", .05, False), ("20% scattered single hours", .20, False), ("20% in 6-hour sensor outages", .20, True)):
    obs = blank(truth, frac, burst)
    res = {}
    res["drop"] = daily_means(obs, "")
    res["ffill"] = daily_means(fill_prev([dict(r) for r in obs]), "")
    res["median"] = daily_means(fill_median([dict(r) for r in obs]), "")
    errs = {k: sum(abs(v[d] - tm[d]) for d in tm if v[d] is not None) / len(tm) for k, v in res.items()}
    print(f"{name:<34}{errs['drop']:>28.2f}{errs['ffill']:>24.2f}{errs['median']:>18.2f}")
print("\nTime and extra space for n = 1,000,000 readings with 5% missing (list of values)")
vals = [None if rnd.random() < .05 else rnd.uniform(20, 120) for _ in range(1_000_000)]
t0 = time.perf_counter(); d = [v for v in vals if v is not None]; t_drop = time.perf_counter() - t0
t0 = time.perf_counter(); out = []; last = None
for v in vals:
    if v is None: out.append(last)
    else: last = v; out.append(v)
t_ff = time.perf_counter() - t0
t0 = time.perf_counter(); m = statistics.median(d); t_med = time.perf_counter() - t0
t0 = time.perf_counter(); s = sorted(d); t_sort = time.perf_counter() - t0
print(f"  drop: {t_drop:.3f} s, O(n), a new list of {len(d):,} values | forward fill: {t_ff:.3f} s, O(n), a new list of {len(out):,} | median (sorting): {t_med:.3f} s, O(n log n), copy of {len(d):,} values (sorted() alone {t_sort:.3f} s)")

print("\nA2.2 normalisation on one day of Ennore PM2.5 (24 hourly values) with and without one sensor spike")
day = [round(95 + 25 * ((h - 9) ** 2 < 6) + h * 0.5, 1) for h in range(24)]
spiked = day[:]; spiked[5] = 900.0
for name, vals in (("normal day", day), ("same day, one reading 900", spiked)):
    mm, zs = min_max(vals), z_scores(vals)
    print(f"  {name:<28}min {min(vals):>6} max {max(vals):>6} | min-max of the typical 12:00 value ({vals[12]}): {mm[12]:.3f} | z-score: {zs[12]:+.2f} | z-score of the extreme value: {max(zs):+.2f}")
print("  The spike squeezes every other value toward 0 in min-max (range set by two points), so remove impossible values BEFORE scaling.")
