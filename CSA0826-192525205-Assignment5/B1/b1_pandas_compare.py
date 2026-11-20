"""B1 alternative: the same cleaning with pandas (read_csv, replace, to_numeric, drop_duplicates, groupby-ffill, vectorised scaling)."""
import io, random, sys, time, tracemalloc, glob, csv
import pandas as pd
sys.path.insert(0, "../common")
from cleaning import clean_rows, LIMITS, FAHRENHEIT_STATIONS, MAX_FILL, min_max
from datagen import make_station_rows, STATIONS, BASE_PM25, HEADER

def clean_pandas(text):
    df = pd.read_csv(io.StringIO(text), dtype=str)
    df["station"] = df["station"].str.strip().str.title()
    d1 = pd.to_datetime(df["date"].str.strip(), format="%Y-%m-%d", errors="coerce")
    d2 = pd.to_datetime(df["date"].str.strip(), format="%d/%m/%Y", errors="coerce")
    df["date"] = d1.fillna(d2).dt.strftime("%Y-%m-%d")
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    df = df[df["date"].notna() & df["hour"].between(0, 23)].copy(); df["hour"] = df["hour"].astype(int)
    df = df.drop_duplicates(["station", "date", "hour"], keep="first")
    for col in ("pm25", "pm10", "no2", "temp"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    f = df["station"].isin(FAHRENHEIT_STATIONS)
    df.loc[f, "temp"] = ((df.loc[f, "temp"] - 32) * 5 / 9).round(1)
    for col, (lo, hi) in LIMITS.items():
        df.loc[~df[col].between(lo, hi), col] = float("nan")
    df = df.sort_values(["station", "date", "hour"]).reset_index(drop=True)
    cols = ["pm25", "pm10", "no2", "temp"]
    df[cols] = df.groupby("station")[cols].ffill(limit=MAX_FILL)
    return df

def raw_text(n_rows, seed=1):
    """About n_rows raw CSV lines (with all the faults), by repeating station-months with different seeds."""
    out, k, rows = [",".join(HEADER)], 0, 0
    while rows < n_rows:
        name, base = STATIONS[k % 12], BASE_PM25[k % 12]
        for r in make_station_rows(name, base, seed=seed + k, year=2026 - k // 12):    # a new year per round of 12 stations: no duplicate keys across blocks
            out.append(",".join(str(x) for x in r)); rows += 1
            if rows >= n_rows: break
        k += 1
    return "\n".join(out) + "\n"

# 1. same answer?
text = open("raw_data/" + sorted(__import__("os").listdir("raw_data"))[0]).read()
allfiles = sorted(glob.glob("raw_data/*.csv"))
big = "".join((open(p).read() if i == 0 else open(p).read().split("\n", 1)[1]) for i, p in enumerate(allfiles))
loops = clean_rows(csv.DictReader(io.StringIO(big)))
pdf = clean_pandas(big)
same_len = len(loops) == len(pdf)
mism = 0
for rec, (_, row) in zip(loops, pdf.iterrows()):
    for c in ("pm25", "pm10", "no2", "temp"):
        a, b = rec[c], row[c]
        if (a is None) != pd.isna(b) or (a is not None and abs(a - b) > 1e-9): mism += 1
print(f"1. correctness on the whole network ({len(loops)} rows): same number of rows: {same_len}; differing cells: {mism}")

# 2. time and memory
print("\n2. time and peak memory (best of 3 for time; tracemalloc for memory; both start from the same raw text)")
print(f"{'rows':>10} {'loops+csv (s)':>14} {'pandas (s)':>11} {'speed-up':>9} | {'loops mem (MB)':>15} {'pandas mem (MB)':>16}")
for n in (1000, 100000, 1000000):
    t = raw_text(n)
    def run_loops(): return clean_rows(csv.DictReader(io.StringIO(t)))
    def run_pd(): return clean_pandas(t)
    def best(fn, reps):
        b = 99
        for _ in range(reps):
            t0 = time.perf_counter(); fn(); b = min(b, time.perf_counter() - t0)
        return b
    reps = 3 if n < 1000000 else 1
    tl, tp = best(run_loops, reps), best(run_pd, reps)
    tracemalloc.start(); run_loops(); ml = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    tracemalloc.start(); run_pd(); mp = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"{n:>10,} {tl:>14.3f} {tp:>11.3f} {tl/tp:>8.1f}x | {ml/1e6:>15.1f} {mp/1e6:>16.1f}")
    del t
print("\n3. vectorised normalisation (pandas) versus loop on the PM2.5 column (1,000,000 values)")
import random as _r
vals = [_r.random() * 200 for _ in range(1_000_000)]
s = pd.Series(vals)
t0 = time.perf_counter(); a = min_max(vals); t1 = time.perf_counter() - t0
t0 = time.perf_counter(); b = ((s - s.min()) / (s.max() - s.min())).round(3); t2 = time.perf_counter() - t0
print(f"   min-max loop {t1:.3f} s | pandas vectorised {t2:.4f} s ({t1/t2:.0f}x) | same values: {max(abs(x - y) for x, y in zip(a[:1000], b[:1000])) < 1e-9}")
