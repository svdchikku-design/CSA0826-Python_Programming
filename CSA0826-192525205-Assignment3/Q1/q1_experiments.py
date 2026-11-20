"""Q1 experiments: counted additions, timings, cost of list operations, late reading, deque/dict alternatives."""
import time, bisect, tracemalloc, sys
from collections import deque
from q1_rainfall import make_readings, moving_average_naive, moving_average_running

W = 7
# ---------------- derived counts (instrumented, explicit additions) ----------------
def naive_counted(r):
    adds = 0
    for i in range(len(r) - W + 1):
        s = r[i]
        for j in range(1, W):
            s += r[i + j]; adds += 1          # 6 additions per window of 7 values
    return adds
def running_counted(r):
    adds = subs = 0
    s = r[0]
    for j in range(1, W):
        s += r[j]; adds += 1                  # first window: 6 additions
    for i in range(W, len(r)):
        s += r[i]; adds += 1                  # new day in
        s -= r[i - W]; subs += 1              # old day out
    return adds, subs
print("DERIVATION  (n days, window w = 7, n - 6 windows)")
print("  naive   : (n - 6) windows x 6 additions = 6(n - 6) additions   -> O(7n)")
print("  running : 6 additions for the first window + (n - 7) additions + (n - 7) subtractions = n - 1 additions, n - 7 subtractions -> O(n)")
print(f"{'n':>8} | {'naive adds (formula)':>21} {'counted':>9} | {'running adds (formula)':>23} {'counted':>9} | {'running subs (formula)':>23} {'counted':>8}")
for n in (365, 36500, 365000):
    r = make_readings(n)
    a, (b, c) = naive_counted(r), running_counted(r)
    print(f"{n:>8} | {6 * (n - 6):>21} {a:>9} | {n - 1:>23} {b:>9} | {n - 7:>23} {c:>8}")

# ---------------- timings ----------------
def best(f, r, reps):
    t = 1e9
    for _ in range(reps):
        t0 = time.perf_counter(); f(r); t = min(t, time.perf_counter() - t0)
    return t
def naive_py(r):                                # slice + explicit Python additions (7 per window, as in the derivation)
    out = []
    for i in range(len(r) - W + 1):
        s = 0.0
        for v in r[i:i + W]:
            s += v
        out.append(s / W)
    return out
print("\nTimings (best of 3, seconds)")
print(f"{'n':>8} | {'naive: sum(slice)':>18} {'naive: python adds':>19} {'running sum':>12} | ratio naive_py/running | predicted ratio 6(n-6)/(n-1+n-7)")
rows = []
for n in (365, 36500, 365000):
    r = make_readings(n)
    t1, t2, t3 = best(moving_average_naive, r, 3), best(naive_py, r, 3), best(moving_average_running, r, 3)
    rows.append((n, t1, t2, t3))
    print(f"{n:>8} | {t1:>18.6f} {t2:>19.6f} {t3:>12.6f} | {t2 / t3:>21.2f}x | {6 * (n - 6) / (2 * n - 8):>6.2f}x (ops)")
print("running-sum floating-point drift vs naive at n = 365000:", max(abs(a - b) for a, b in zip(moving_average_naive(r), moving_average_running(r))))

# ---------------- cost of list operations ----------------
print("\nCost of list operations (microseconds per operation)")
print(f"{'n':>9} | {'append':>8} {'pop()':>8} {'insert(0,x)':>12} {'pop(0)':>8} {'insert middle':>14} | {'sort random':>12} {'sort sorted':>12}")
import random
for n in (1000, 100000, 1000000):
    base = list(range(n)); k = 200
    t0 = time.perf_counter()
    for _ in range(k): base.append(1)
    ap = (time.perf_counter() - t0) / k * 1e6
    t0 = time.perf_counter()
    for _ in range(k): base.pop()
    pp = (time.perf_counter() - t0) / k * 1e6
    t0 = time.perf_counter()
    for _ in range(k): base.insert(0, 1)
    i0 = (time.perf_counter() - t0) / k * 1e6
    t0 = time.perf_counter()
    for _ in range(k): base.pop(0)
    p0 = (time.perf_counter() - t0) / k * 1e6
    t0 = time.perf_counter()
    for _ in range(k): base.insert(n // 2, 1)
    im = (time.perf_counter() - t0) / k * 1e6
    rnd = list(range(n)); random.Random(1).shuffle(rnd)
    t0 = time.perf_counter(); rnd.sort(); ts = (time.perf_counter() - t0) * 1e6
    t0 = time.perf_counter(); rnd.sort(); tss = (time.perf_counter() - t0) * 1e6
    print(f"{n:>9} | {ap:>8.3f} {pp:>8.3f} {i0:>12.3f} {p0:>8.3f} {im:>14.3f} | {ts:>10.0f}us {tss:>10.0f}us")

# ---------------- design question: a late reading ----------------
print("\nLate reading inserted at the correct date (list.insert in the middle):")
for n in (365, 365000):
    r = make_readings(n)
    k = 2000 if n == 365 else 200
    t0 = time.perf_counter()
    for _ in range(k): r.insert(n // 2, 5.0)
    t_ins = (time.perf_counter() - t0) / k * 1e6
    r2 = [None] * n
    t0 = time.perf_counter()
    for _ in range(k): r2[n // 2] = 5.0
    t_set = (time.perf_counter() - t0) / k * 1e6
    t0 = time.perf_counter()
    for _ in range(k): bisect.insort(r, 5.0)
    print(f"  n = {n:>7}: insert in the middle {t_ins:8.3f} us | assigning into a pre-sized slot {t_set:.3f} us")

# ---------------- alternative: deque(maxlen=7) and dictionary keyed by date ----------------
def ma_deque_resum(r):
    win, out = deque(maxlen=W), []
    for v in r:
        win.append(v)                             # the oldest value drops out automatically
        if len(win) == W:
            out.append(sum(win) / W)              # re-adds 7 values: O(7n)
    return out
def ma_deque_running(r):
    win, out, total = deque(maxlen=W), [], 0.0
    for v in r:
        if len(win) == W:
            total -= win[0]                       # value about to be pushed out
        win.append(v); total += v
        if len(win) == W:
            out.append(total / W)                 # O(1) per day: O(n)
    return out
from datetime import date, timedelta
def make_dict(r):
    d0 = date(2026, 1, 1)
    return {d0 + timedelta(days=i): v for i, v in enumerate(r)}
def ma_dict(d):
    days = sorted(d); out = []
    for i in range(W - 1, len(days)):
        out.append(sum(d[days[j]] for j in range(i - W + 1, i + 1)) / W)   # needs the dates in order
    return out
r = make_readings(36500)
assert all(abs(a - b) < 1e-9 for a, b in zip(moving_average_naive(r), ma_deque_resum(r))) and all(abs(a - b) < 1e-9 for a, b in zip(moving_average_naive(r), ma_deque_running(r)))
assert all(abs(a - b) < 1e-9 for a, b in zip(moving_average_naive(r), ma_dict(make_dict(r))))
print("\nAlternatives give the same averages (checked on 36,500 days).")
print(f"{'n':>8} | {'slice+sum':>10} {'running (list)':>15} {'deque re-sum':>13} {'deque running':>14} {'dict by date':>13}   (seconds)")
for n in (36500, 365000):
    r = make_readings(n); d = make_dict(r)
    print(f"{n:>8} | {best(moving_average_naive, r, 3):>10.4f} {best(moving_average_running, r, 3):>15.4f} {best(ma_deque_resum, r, 3):>13.4f} {best(ma_deque_running, r, 3):>14.4f} {best(lambda x: ma_dict(d), r, 1):>13.4f}")
print("\nMemory of the stored data (365,000 readings) and of the moving window")
r = make_readings(365000)
tracemalloc.start(); lst = make_readings(365000); m_list = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
tracemalloc.start(); dct = make_dict(lst); m_dict = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
print(f"  list of readings        : {m_list / 1e6:7.1f} MB (the floats) -> container itself {sys.getsizeof(lst) / 1e6:.1f} MB")
print(f"  dict keyed by date      : {m_dict / 1e6:7.1f} MB extra (date objects + hash table) on top of the float values already counted")
print(f"  deque(maxlen=7) window  : {sys.getsizeof(deque(maxlen=7))} bytes (constant, independent of n)")
print(f"  slice window            : a new 7-element list per day (about {sys.getsizeof(lst[:7])} bytes, freed at once)")
# chart
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.4))
ns = [x[0] for x in rows]
ax.plot(ns, [x[2] for x in rows], "o-", label="naive (Python additions)"); ax.plot(ns, [x[1] for x in rows], "s-", label="naive (sum of slice)"); ax.plot(ns, [x[3] for x in rows], "^-", label="running sum")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("days n"); ax.set_ylabel("time (s)"); ax.set_title("7-day moving average: measured time"); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("chart_moving_average.png", dpi=130)
