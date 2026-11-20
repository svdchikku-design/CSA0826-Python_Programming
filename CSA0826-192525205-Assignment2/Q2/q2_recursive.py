"""Q2 alternative: the attempt loop written recursively; time, depth and stack limit versus while."""
import sys, time
OTP = "483920"

def verify_rec(typed, attempt=1, limit=3, depth=1):
    """Returns (result, depth reached). One stack frame per attempt."""
    if attempt > limit:
        return "LOCKED", depth
    entry = next(typed).strip()
    if entry == "":
        return verify_rec(typed, attempt, limit, depth + 1)       # blank: same attempt number, but another frame
    if entry == OTP:
        return "VERIFIED", depth
    return verify_rec(typed, attempt + 1, limit, depth + 1)

def verify_loop(typed, limit=3):
    attempt = 0
    while attempt < limit:
        entry = next(typed).strip()
        if entry == "":
            continue
        attempt += 1
        if entry == OTP:
            return "VERIFIED", 1
    return "LOCKED", 1

print("3-attempt behaviour is identical:")
for entries in (["483920"], ["1", "483920"], ["", "1", "2", "3"], ["1", "2", "3"]):
    print(f"  {str(entries):<28} recursive={verify_rec(iter(entries))[0]:<9} loop={verify_loop(iter(entries))[0]}")

print(f"\nrecursion limit = {sys.getrecursionlimit()}")
print(f"{'attempts a':>11} | {'loop time':>10} {'loop depth':>11} | {'recursive time':>15} {'recursive depth':>16}")
for a in (3, 100, 900, 10_000, 1_000_000):
    wrong = iter(["x"] * a)
    t0 = time.perf_counter(); r, d = verify_loop(wrong, a); tl = time.perf_counter() - t0
    try:
        wrong = iter(["x"] * a)
        t0 = time.perf_counter(); r2, d2 = verify_rec(wrong, 1, a); tr = time.perf_counter() - t0
        rec = f"{tr * 1e6:>13.1f}us {d2:>16}"
    except RecursionError:
        rec = f"{'RecursionError':>15} {'> limit':>16}"
    print(f"{a:>11} | {tl * 1e6:>8.1f}us {d:>11} | {rec}")
