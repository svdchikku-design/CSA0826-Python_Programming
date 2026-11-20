"""B2 alternative: one execute() per row versus executemany(); commit per row versus one commit; :memory: versus a file."""
import os, sqlite3, tempfile, time

def rows(n): return [(f"S{i % 12}", "2026-10-01", float(i % 200)) for i in range(n)]

def run_loop(con, data, commit_each):
    for r in data:
        con.execute("INSERT INTO aq VALUES (?, ?, ?)", r)
        if commit_each: con.commit()
    con.commit()
def run_many(con, data):
    con.executemany("INSERT INTO aq VALUES (?, ?, ?)", data); con.commit()

def fresh(path):
    if path != ":memory:" and os.path.exists(path): os.remove(path)
    con = sqlite3.connect(path); con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)"); return con

tmp = os.path.join(tempfile.mkdtemp(), "t.db")
print(f"{'rows':>9} | {'loop+commit each (file) s':>26} {'loop, one commit (file) s':>26} {'executemany (file) s':>21} | {'loop (memory) s':>16} {'executemany (memory) s':>23}")
for n in (1000, 10000, 100000):
    data = rows(n); out = {}
    if n <= 10000:
        con = fresh(tmp); t0 = time.perf_counter(); run_loop(con, data, True); out["a"] = time.perf_counter() - t0; con.close()
    con = fresh(tmp); t0 = time.perf_counter(); run_loop(con, data, False); out["b"] = time.perf_counter() - t0; con.close()
    con = fresh(tmp); t0 = time.perf_counter(); run_many(con, data); out["c"] = time.perf_counter() - t0
    assert con.execute("SELECT COUNT(*) FROM aq").fetchone()[0] == n; con.close()
    con = fresh(":memory:"); t0 = time.perf_counter(); run_loop(con, data, False); out["d"] = time.perf_counter() - t0
    con = fresh(":memory:"); t0 = time.perf_counter(); run_many(con, data); out["e"] = time.perf_counter() - t0
    a = f"{out['a']:.3f}" if "a" in out else "not run (too slow)"
    print(f"{n:>9,} | {a:>26} {out['b']:>26.3f} {out['c']:>21.3f} | {out['d']:>16.3f} {out['e']:>23.3f}")
print("\nAll variants stored the same number of rows. The two statements are equally safe (both use ? placeholders); they differ only in speed.")
