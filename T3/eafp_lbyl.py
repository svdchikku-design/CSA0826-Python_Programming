"""Task 3 alternative: EAFP (raise and catch InvalidRecord) versus LBYL (check with if before use). Time per line for rare and common bad lines."""
import time, random

class InvalidRecord(Exception): pass

def parse_eafp(line):
    parts = line.split(",")
    if len(parts) != 3: raise InvalidRecord("fields")
    if parts[2] not in ("P", "A"): raise InvalidRecord("status")
    return parts

def run_eafp(lines):
    ok = bad = 0
    for line in lines:
        try: parse_eafp(line)
        except InvalidRecord: bad += 1
        else: ok += 1
    return ok, bad

def run_lbyl(lines):
    ok = bad = 0
    for line in lines:
        parts = line.split(",")
        if len(parts) == 3 and parts[2] in ("P", "A"): ok += 1
        else: bad += 1
    return ok, bad

N = 300000
print("Both styles are O(n) in the number of lines; what differs is the constant cost of a bad line.")
print(f"{'bad lines':>10} | {'EAFP (raise/catch) ns/line':>27} {'LBYL (if) ns/line':>19} | EAFP/LBYL | same counts")
for frac in (0.0, 0.001, 0.01, 0.10, 0.50, 1.0):
    rnd = random.Random(1)
    lines = ["192311001,2026-10-08,P" if rnd.random() >= frac else "192311001,2026-10-08" for _ in range(N)]
    best = {}
    for name, fn in (("e", run_eafp), ("l", run_lbyl)):
        ts = []
        for _ in range(3):
            t0 = time.perf_counter(); r = fn(lines); ts.append(time.perf_counter() - t0)
        best[name] = (min(ts) / N * 1e9, r)
    print(f"{frac*100:>9.1f}% | {best['e'][0]:>27.0f} {best['l'][0]:>19.0f} | {best['e'][0]/best['l'][0]:>8.2f}x | {best['e'][1] == best['l'][1]}")
