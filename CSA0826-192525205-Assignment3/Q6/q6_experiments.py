"""Q6 experiments: station queries with and without an index, memory of the index, and the flat-list alternative."""
import random, time, tracemalloc, sys
from q6_timetable import DAYS, trains_at, timetable as small

STATIONS = [f"Station{i:03d}" for i in range(500)]
def make_timetable(n_trains, seed=4):
    rnd = random.Random(seed); tt = {}
    for i in range(n_trains):
        k = rnd.randint(8, 16)
        names = rnd.sample(STATIONS, k)
        h = rnd.randrange(24); stops = []
        for j, s in enumerate(names):
            h = (h + rnd.randint(0, 1)) % 24; m = rnd.randrange(60)
            stops.append((s, "-" if j == 0 else f"{h:02d}:{m:02d}", "-" if j == k - 1 else f"{h:02d}:{(m + 2) % 60:02d}"))
        tt[10000 + i] = {"name": f"Train {i}", "stops": stops, "days": set(rnd.sample(DAYS, rnd.randint(3, 7)))}
    return tt

def build_index(tt):
    """station -> list of (train number, arrival, departure)."""
    idx = {}
    for number, info in tt.items():
        for st, arr, dep in info["stops"]:
            idx.setdefault(st, []).append((number, arr, dep))
    return idx

def trains_at_indexed(tt, idx, station, day):
    out = []
    for number, arr, dep in idx.get(station, []):          # unknown station -> empty list, no KeyError
        if day in tt[number]["days"]:
            out.append((dep if dep != "-" else arr, number))
    return out

# correctness on the 6-train table
sidx = build_index(small)
for stn in ("Katpadi", "Chennai Central", "Atlantis"):
    for d in DAYS:
        assert sorted(trains_at(small, stn, d)) == sorted(trains_at_indexed(small, sidx, stn, d))
print("indexed and scanning queries agree for every station and day of the 6-train timetable: True\n")

print("Derivation: without an index one query examines all S = total stops (about 12 per train) -> O(S) = O(12 T); with an index only the m trains that stop at the station -> O(m)")
print(f"{'trains T':>9} {'total stops S':>14} {'avg trains/station m':>21} | {'scan (ms/query)':>16} {'index (us/query)':>17} {'speed-up':>9} | {'build index':>12} | {'timetable':>10} {'index extra':>12}")
for T in (100, 1000, 10000):
    tt = make_timetable(T); S = sum(len(v["stops"]) for v in tt.values())
    rnd = random.Random(9); queries = [(rnd.choice(STATIONS), rnd.choice(DAYS)) for _ in range(300)]
    t0 = time.perf_counter(); idx = build_index(tt); t_build = time.perf_counter() - t0
    t0 = time.perf_counter()
    for s, d in queries: a = trains_at(tt, s, d)
    t_scan = (time.perf_counter() - t0) / len(queries)
    t0 = time.perf_counter()
    for _ in range(10):
        for s, d in queries: b = trains_at_indexed(tt, idx, s, d)
    t_idx = (time.perf_counter() - t0) / (10 * len(queries))
    assert all(sorted(trains_at(tt, s, d)) == sorted(trains_at_indexed(tt, idx, s, d)) for s, d in queries[:50])
    m = S / len(STATIONS)
    tracemalloc.start(); tt2 = make_timetable(T); mem_tt = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    tracemalloc.start(); idx2 = build_index(tt2); mem_idx = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    print(f"{T:>9} {S:>14} {m:>21.1f} | {t_scan * 1e3:>16.3f} {t_idx * 1e6:>17.2f} {t_scan / t_idx:>8.0f}x | {t_build * 1e3:>10.2f}ms | {mem_tt / 1e6:>8.2f}MB {mem_idx / 1e6:>10.2f}MB")

print("\nSpecial queries on the 10,000-train timetable:")
tt = make_timetable(10000); idx = build_index(tt)
print("  unknown station 'Atlantis':", trains_at(tt, "Atlantis", "Mon"), trains_at_indexed(tt, idx, "Atlantis", "Mon"))
n_only = next(n for n, v in tt.items() if len(v["days"]) == 3); st0 = tt[n_only]["stops"][0][0]; off = next(d for d in DAYS if d not in tt[n_only]["days"])
print(f"  train {n_only} runs only on {sorted(tt[n_only]['days'])}; at its first station {st0} on {off} it must be absent:",
      n_only not in [n for _, n in trains_at(tt, st0, off)], n_only not in [n for _, n in trains_at_indexed(tt, idx, st0, off)])
run_day = sorted(tt[n_only]["days"])[0]
print(f"  on {run_day} it is present: ", n_only in [n for _, n in trains_at_indexed(tt, idx, st0, run_day)])

print("\nAlternative: one flat list of (train, station, arrival, departure, days) tuples scanned for every query")
def flatten(tt):
    return [(n, st, arr, dep, info["days"]) for n, info in tt.items() for st, arr, dep in info["stops"]]
def query_flat(flat, station, day):
    return [(dep if dep != "-" else arr, n) for n, st, arr, dep, days in flat if st == station and day in days]
print(f"{'trains T':>9} {'rows S':>9} | {'flat scan (ms/query)':>21} {'nested scan (ms)':>17} {'index (us)':>11} | {'flat list memory':>17} {'nested+index memory':>20}")
for T in (100, 1000, 10000):
    tt = make_timetable(T); flat = flatten(tt); idx = build_index(tt)
    rnd = random.Random(9); queries = [(rnd.choice(STATIONS), rnd.choice(DAYS)) for _ in range(100)]
    t0 = time.perf_counter()
    for s, d in queries: query_flat(flat, s, d)
    tf = (time.perf_counter() - t0) / len(queries)
    t0 = time.perf_counter()
    for s, d in queries: trains_at(tt, s, d)
    tn = (time.perf_counter() - t0) / len(queries)
    t0 = time.perf_counter()
    for _ in range(20):
        for s, d in queries: trains_at_indexed(tt, idx, s, d)
    ti = (time.perf_counter() - t0) / (20 * len(queries))
    assert all(sorted(query_flat(flat, s, d)) == sorted(trains_at(tt, s, d)) for s, d in queries[:30])
    tracemalloc.start(); flat2 = flatten(make_timetable(T)); mem_flat = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    tracemalloc.start(); t2 = make_timetable(T); i2 = build_index(t2); mem_nest = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    print(f"{T:>9} {len(flat):>9} | {tf * 1e3:>21.3f} {tn * 1e3:>17.3f} {ti * 1e6:>11.2f} | {mem_flat / 1e6:>15.2f}MB {mem_nest / 1e6:>18.2f}MB")
