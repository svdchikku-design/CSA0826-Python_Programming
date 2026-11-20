"""B4.2: effect of an index on (station, day) at the new scale: 112 stations reporting every 15 minutes for a year (3.9 million rows)."""
import os, random, sqlite3, tempfile, time
from datetime import date, timedelta

STATIONS = 112
DAYS = 365
PER_DAY = 96                                           # one reading every 15 minutes
path = os.path.join(tempfile.mkdtemp(), "big.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE aq (station TEXT, day TEXT, slot INTEGER, pm25 REAL)")
rnd = random.Random(8); d0 = date(2026, 1, 1)
days = [(d0 + timedelta(days=k)).isoformat() for k in range(DAYS)]
def gen():
    for s in range(STATIONS):
        base = rnd.uniform(35, 100)
        for d in days:
            for slot in range(PER_DAY):
                yield (f"S{s+1:03d}", d, slot, round(base + rnd.gauss(0, 15), 1))
t0 = time.perf_counter(); con.executemany("INSERT INTO aq VALUES (?, ?, ?, ?)", gen()); con.commit()
t_load = time.perf_counter() - t0
n = con.execute("SELECT COUNT(*) FROM aq").fetchone()[0]
print(f"loaded {n:,} rows (112 stations x 365 days x 96 readings) in {t_load:.1f} s; database file {os.path.getsize(path)/1e6:.0f} MB\n")

QUERIES = [
    ("Q1 one station, one day (a lookup)", "SELECT AVG(pm25) FROM aq WHERE station = 'S057' AND day = '2026-06-15'"),
    ("Q2 one station, whole year by day", "SELECT day, AVG(pm25) FROM aq WHERE station = 'S057' GROUP BY day"),
    ("Q3 all stations, one day", "SELECT station, AVG(pm25) FROM aq WHERE day = '2026-06-15' GROUP BY station"),
    ("Q4 all stations, whole year", "SELECT station, AVG(pm25) FROM aq GROUP BY station"),
]
def timeit(sql, reps=3):
    best = 99
    for _ in range(reps):
        t0 = time.perf_counter(); rows = con.execute(sql).fetchall(); best = min(best, time.perf_counter() - t0)
    return best, rows
def plan(sql): return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql))

before = {}
print("BEFORE the index (best of 3)")
for name, sql in QUERIES:
    t, rows = timeit(sql); before[name] = (t, rows)
    print(f"  {name:<38}{t*1e3:>10.1f} ms   plan: {plan(sql)}")
slowest = max(before, key=lambda k: before[k][0])
print(f"  slowest overall: {slowest}")
t0 = time.perf_counter(); con.execute("CREATE INDEX idx_station_day ON aq (station, day)"); con.commit(); t_idx = time.perf_counter() - t0
print(f"\nCREATE INDEX idx_station_day ON aq (station, day): {t_idx:.2f} s; database file now {os.path.getsize(path)/1e6:.0f} MB")
print("\nAFTER the index (best of 3)")
print(f"  {'query':<38}{'before ms':>10}{'after ms':>10}{'speed-up':>10}   same result   plan")
for name, sql in QUERIES:
    t, rows = timeit(sql)
    same = sorted(rows) == sorted(before[name][1])
    print(f"  {name:<38}{before[name][0]*1e3:>10.1f}{t*1e3:>10.2f}{before[name][0]/t:>9.0f}x   {str(same):<11}   {plan(sql)}")

print("\nCost of the index when data arrive: insert 100,000 new readings with and without the index")
def ins(c):
    rows = [("S001", "2027-01-01", i % 96, 50.0) for i in range(100000)]
    t0 = time.perf_counter(); c.executemany("INSERT INTO aq VALUES (?, ?, ?, ?)", rows); c.commit(); return time.perf_counter() - t0
t_with = ins(con)
con.execute("DROP INDEX idx_station_day"); t_without = ins(con)
print(f"  with index: {t_with:.3f} s | without index: {t_without:.3f} s | the index makes inserts {t_with/t_without:.1f}x slower")
os.remove(path)
