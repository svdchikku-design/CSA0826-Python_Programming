"""B3: daily mean PM2.5 per station by (1) plain Python loops + csv, (2) pandas groupby, (3) SQLite GROUP BY, (+) one-pass running sums."""
import csv, cProfile, io, os, pstats, random, sqlite3, statistics, sys, time, tracemalloc
from datetime import date, timedelta
import pandas as pd

def make_csv(path, n_stations, days=365, seed=3):
    """Cleaned readings: station,date,hour,pm25 - 24 readings a day, so about 8,760 per station-year."""
    rnd = random.Random(seed); d0 = date(2026, 1, 1)
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["station", "date", "hour", "pm25"])
        for s in range(n_stations):
            base = rnd.uniform(35, 100)
            for k in range(days):
                day = (d0 + timedelta(days=k)).isoformat()
                for h in range(24):
                    w.writerow([f"S{s+1:03d}", day, h, round(max(3, rnd.gauss(base, 15)), 1)])

def by_loops(path):
    groups = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            groups.setdefault((r["station"], r["date"]), []).append(float(r["pm25"]))     # store all readings first
    return {k: statistics.mean(v) for k, v in groups.items()}

def by_pandas(path):
    df = pd.read_csv(path)
    return df.groupby(["station", "date"])["pm25"].mean().to_dict()

def by_sql(path, con=None, load=True):
    con = con or sqlite3.connect(":memory:")
    if load:
        con.execute("CREATE TABLE aq (station TEXT, day TEXT, hour INTEGER, pm25 REAL)")
        with open(path, newline="") as f:
            rd = csv.reader(f); next(rd)
            con.executemany("INSERT INTO aq VALUES (?, ?, ?, ?)", ((s, d, int(h), float(p)) for s, d, h, p in rd))
    return {(s, d): m for s, d, m in con.execute("SELECT station, day, AVG(pm25) FROM aq GROUP BY station, day")}, con

def one_pass(path):
    total, count = {}, {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            k = (r["station"], r["date"])
            total[k] = total.get(k, 0.0) + float(r["pm25"]); count[k] = count.get(k, 0) + 1     # only a sum and a count per group
    return {k: total[k] / count[k] for k in total}

def same(a, b, tol=1e-9):
    return a.keys() == b.keys() and all(abs(a[k] - b[k]) < tol for k in a)

if __name__ == "__main__":
    tmp = "/tmp/b3"; os.makedirs(tmp, exist_ok=True)
    print("B3.1 correctness on small data: 3 stations, 7 days (504 readings)")
    make_csv(f"{tmp}/small.csv", 3, days=7)
    a, b, (c, _), d = by_loops(f"{tmp}/small.csv"), by_pandas(f"{tmp}/small.csv"), by_sql(f"{tmp}/small.csv"), one_pass(f"{tmp}/small.csv")
    print(f"   groups: loops {len(a)}, pandas {len(b)}, SQL {len(c)}, one-pass {len(d)} (3 stations x 7 days = 21)")
    print(f"   loops == pandas: {same(a, b)} | loops == SQL: {same(a, c)} | loops == one-pass: {same(a, d)}")
    k = ("S001", "2026-01-01"); rows = [float(r["pm25"]) for r in csv.DictReader(open(f"{tmp}/small.csv")) if (r["station"], r["date"]) == k]
    print(f"   hand check {k}: {len(rows)} readings, mean {sum(rows)/len(rows):.4f}; loops {a[k]:.4f}, pandas {b[k]:.4f}, SQL {c[k]:.4f}")
    assert same(a, b) and same(a, c) and same(a, d)

    print("\nB3.2 time (seconds, best of 3 for the smaller sizes, 1 run for 120 stations) - includes reading the CSV / loading the database")
    print(f"{'stations':>8} {'readings':>10} | {'loops+csv':>10} {'pandas':>8} {'SQL load':>9} {'SQL query':>10} {'SQL total':>10} {'one-pass':>9} | {'same results':>12}")
    for n_st in (1, 12, 120):
        path = f"{tmp}/s{n_st}.csv"; make_csv(path, n_st)
        n = n_st * 365 * 24; reps = 3 if n_st < 120 else 1
        def best(fn):
            t = 99
            for _ in range(reps):
                t0 = time.perf_counter(); r = fn(); t = min(t, time.perf_counter() - t0)
            return t, r
        tl, rl = best(lambda: by_loops(path)); tp, rp = best(lambda: by_pandas(path)); to, ro = best(lambda: one_pass(path))
        t0 = time.perf_counter(); _, con = by_sql(path, load=True); t_load = time.perf_counter() - t0
        t0 = time.perf_counter(); rs, _ = by_sql(path, con, load=False); t_q = time.perf_counter() - t0
        ok = same(rl, rp) and same(rl, rs) and same(rl, ro)
        print(f"{n_st:>8} {n:>10,} | {tl:>10.3f} {tp:>8.3f} {t_load:>9.3f} {t_q:>10.3f} {t_load + t_q:>10.3f} {to:>9.3f} | {str(ok):>12}")
    print("   (SQL load = insert every row; SQL query = the GROUP BY on data already in the database)")

    print("\nB3.3 cProfile of the plain-Python loops version on 120 stations (1,051,200 rows)")
    pr = cProfile.Profile(); pr.enable(); by_loops(f"{tmp}/s120.csv"); pr.disable()
    s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(8)
    text = s.getvalue(); print("\n".join(l for l in text.splitlines() if l.strip()))

    print("\nAlternative: memory of storing all readings first versus one pass (120 stations, tracemalloc peak)")
    for name, fn in (("store all readings, then statistics.mean", by_loops), ("one pass, running sum and count", one_pass)):
        tracemalloc.start(); r = fn(f"{tmp}/s120.csv"); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"   {name:<44}{peak/1e6:>9.1f} MB peak, {len(r):,} groups kept")
    print("   groups = stations x days = 120 x 365 = 43,800; readings n = 1,051,200")
