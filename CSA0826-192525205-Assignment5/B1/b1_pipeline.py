"""B1.3: clean all 12 station files, store in SQLite with executemany, answer the three board questions with SQL."""
import csv, glob, os, sqlite3, sys, time
sys.path.insert(0, "../common")
from cleaning import clean_file, FAHRENHEIT_STATIONS

DB = "air_quality.db"
if os.path.exists(DB): os.remove(DB)
stats, all_rows = {}, []
t0 = time.perf_counter()
files = sorted(glob.glob("raw_data/*.csv"))
for path in files:
    all_rows += clean_file(path, stats)
t_clean = time.perf_counter() - t0
print(f"cleaned {len(files)} files in {t_clean:.2f} s -> {len(all_rows)} rows")
print("cleaning report for the whole network:")
for k in sorted(stats): print(f"  {k:<36}{stats[k]:>7}")
raw_lines = stats["rows read"]
print(f"  check: rows read {raw_lines} - duplicates {stats['duplicate rows removed']} - dropped {stats.get('rows dropped: bad date or hour', 0)} = {raw_lines - stats['duplicate rows removed'] - stats.get('rows dropped: bad date or hour', 0)} (rows stored: {len(all_rows)})")

con = sqlite3.connect(DB)
con.executescript(open("schema.sql").read())
names = sorted({r["station"] for r in all_rows})
con.executemany("INSERT INTO stations(name, temp_unit) VALUES (?, ?)", [(n, "F" if n in FAHRENHEIT_STATIONS else "C") for n in names])
ids = {name: sid for sid, name in con.execute("SELECT station_id, name FROM stations")}
t0 = time.perf_counter()
con.executemany("INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?, ?)",
                [(ids[r["station"]], r["date"], r["hour"], r["pm25"], r["pm10"], r["no2"], r["temp"]) for r in all_rows])
con.commit()
print(f"\nexecutemany stored {con.execute('SELECT COUNT(*) FROM readings').fetchone()[0]} readings in {time.perf_counter()-t0:.3f} s;",
      f"stations: {con.execute('SELECT COUNT(*) FROM stations').fetchone()[0]}; rows with NULL pm25 (could not be filled): {con.execute('SELECT COUNT(*) FROM readings WHERE pm25 IS NULL').fetchone()[0]}")

print("\nQ1. Average PM2.5 of Adyar in October 2026")
q1 = """SELECT ROUND(AVG(r.pm25), 2) FROM readings r JOIN stations s USING (station_id)
        WHERE s.name = ? AND r.date BETWEEN '2026-10-01' AND '2026-10-31'"""
print("   SQL:", " ".join(q1.split())); print("   ->", con.execute(q1, ("Adyar",)).fetchone()[0])
print("\nQ2. Stations ranked by their monthly mean PM2.5 (worst first)")
q2 = """SELECT s.name, ROUND(AVG(r.pm25), 1) AS mean_pm25, COUNT(r.pm25) AS valid_readings
        FROM readings r JOIN stations s USING (station_id) GROUP BY s.name ORDER BY mean_pm25 DESC"""
print("   SQL:", " ".join(q2.split()))
for row in con.execute(q2): print("   ", row)
print("\nQ3. Which hours of the day have the worst air? (city-wide mean PM2.5 per hour, top 5)")
q3 = "SELECT hour, ROUND(AVG(pm25), 1) AS mean_pm25 FROM readings GROUP BY hour ORDER BY mean_pm25 DESC LIMIT 5"
print("   SQL:", q3)
for row in con.execute(q3): print("   ", row)

# the same three questions answered from the CSV files with Python (A1.3 comparison)
def csv_q1():
    total = n = 0
    for path in files:
        with open(path, newline="") as f:
            for r in csv.DictReader(f):
                if r["station"].strip().title() == "Adyar" and r["date"].startswith("2026-10"):
                    try: total += float(r["pm25"]); n += 1
                    except ValueError: pass
    return round(total / n, 2)
print("\nA1.3 comparison - Q1 from the RAW csv files with a loop (no cleaning, no fill): ", csv_q1(), "| from the cleaned database:", con.execute(q1, ("Adyar",)).fetchone()[0])
def timeit(fn, n=5):
    best = 9
    for _ in range(n):
        t0 = time.perf_counter(); fn(); best = min(best, time.perf_counter() - t0)
    return best
print(f"time for Q1: CSV loop over 12 files {timeit(csv_q1)*1e3:.1f} ms | SQL {timeit(lambda: con.execute(q1, ('Adyar',)).fetchone())*1e3:.2f} ms")
con.close()
print("database file size:", os.path.getsize(DB) // 1024, "KB;", "raw csv size:", sum(os.path.getsize(p) for p in files) // 1024, "KB")
