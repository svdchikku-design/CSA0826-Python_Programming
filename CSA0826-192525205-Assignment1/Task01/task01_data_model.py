"""Task 1 - data model of the Ksheera milk payment problem, and the 3-variables-per-farmer alternative."""
import time

# ---- named constants (never change during a run) ----
BASE_RATE = 30.00         # Rs/litre at standard quality
STD_FAT, STD_SNF = 3.5, 8.5
STEP = 0.1                # one quality step = 0.1 %
FAT_STEP_VALUE = 0.40     # Rs/litre per fat step
SNF_STEP_VALUE = 0.30     # Rs/litre per SNF step
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 6.0, 10.0
MAX_LITRES = 200.0        # assumption: one farmer, one shift
PAYMENT_DAYS = 10

print("=== Values, types and the reason for each ===")
rows = [
    ("farmer_id", "F001", "text: an identifier, no arithmetic"),
    ("litres", 10.5, "fractional: measured quantity"),
    ("fat", 3.5, "fractional: percentage"),
    ("snf", 8.5, "fractional: percentage"),
    ("shift", "M", "text: M = morning, E = evening"),
    ("PAYMENT_DAYS", PAYMENT_DAYS, "whole number: count of days"),
    ("BASE_RATE", BASE_RATE, "fractional: money (see Task 2 - will become Decimal)"),
]
for name, value, why in rows:
    print(f"{name:13} {value!r:8} {type(value).__name__:6} {why}")

print("\n=== One entry kept as ONE tuple, many entries in ONE list ===")
entries = [("F001", 10.0, 3.5, 8.5, "M"), ("F002", 8.5, 4.2, 8.7, "M"), ("F003", 12.0, 3.1, 8.3, "E")]
for e in entries:
    print(e)

# ---- Alternative: three separate variables per farmer (generated source for n farmers) ----
def variable_style_source(n):
    lines = ["total = 0.0"]
    for i in range(1, n + 1):
        lines.append(f"litres{i} = {10 + i % 5}.0")
        lines.append(f"fat{i} = 3.5")
        lines.append(f"snf{i} = 8.5")
        lines.append(f"total += litres{i} * (30.0 + round((fat{i} - 3.5) / 0.1) * 0.40 + round((snf{i} - 8.5) / 0.1) * 0.30)")
    return "\n".join(lines)

def list_style(n):
    data = [(10 + i % 5, 3.5, 8.5) for i in range(1, n + 1)]
    total = 0.0
    for litres, fat, snf in data:
        total += litres * (30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30)
    return total

print("\n=== Variable-per-value design vs list design ===")
print(f"{'n':>6} {'source lines (variables)':>26} {'source lines (list)':>20} {'t variables (ms)':>17} {'t list (ms)':>12}")
for n in (300, 3000):
    src = variable_style_source(n)
    code = compile(src, "<vars>", "exec")
    ns = {}
    t0 = time.perf_counter(); exec(code, ns); t_var = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); tot = list_style(n); t_list = (time.perf_counter() - t0) * 1000
    assert abs(ns["total"] - tot) < 1e-6
    print(f"{n:>6} {len(src.splitlines()):>26} {7:>20} {t_var:>17.3f} {t_list:>12.3f}")
print("variables created for n=3000 :", sum(1 for k in ns if k.startswith(("litres", "fat", "snf"))))
