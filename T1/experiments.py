"""Task 1 experiments: original vs repaired on the sample, memory of read()/readlines()/iteration at 50,000 lines, time."""
import time, tracemalloc, os, subprocess, sys, random
from mess_repaired import total_bills

print("=== A. Original script on the sample file ===")
print(subprocess.run([sys.executable, "poor_script.py", "mess_oct.txt"], capture_output=True, text=True).stdout)
print("=== B. Repaired script on the same file ===")
print(subprocess.run([sys.executable, "mess_repaired.py", "mess_oct.txt"], capture_output=True, text=True).stdout)
print("=== B2. Missing file ===")
print(subprocess.run([sys.executable, "mess_repaired.py", "nofile.txt"], capture_output=True, text=True).stdout)
print("Original script on a missing file ends with a traceback:",
      "FileNotFoundError" in subprocess.run([sys.executable, "poor_script.py", "nofile.txt"], capture_output=True, text=True).stderr)

# big file
rnd = random.Random(3)
with open("big_50000.txt", "w") as f:
    for i in range(50000):
        f.write(f"{192000000 + i},Student {i},{rnd.randint(900, 1800)}.{rnd.choice(['00','50','25'])}\n")
size = os.path.getsize("big_50000.txt")
print(f"\n=== C. 50,000-line file: size {size/1e6:.2f} MB ===")
def by_read():
    total = 0
    for line in open("big_50000.txt").read().split("\n"):
        if line: total += float(line.split(",")[2])
    return total
def by_readlines():
    total = 0
    for line in open("big_50000.txt").readlines():
        total += float(line.split(",")[2])
    return total
def by_iter():
    total = 0
    with open("big_50000.txt") as f:
        for line in f: total += float(line.split(",")[2])
    return total
print(f"{'method':<22}{'time (s)':>10}{'peak memory (MB)':>20}{'total':>16}")
for name, fn in (("f.read().split()", by_read), ("f.readlines()", by_readlines), ("iterate over f", by_iter)):
    t0 = time.perf_counter(); r = fn(); dt = time.perf_counter() - t0
    tracemalloc.start(); fn(); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"{name:<22}{dt:>10.4f}{peak/1e6:>20.2f}{r:>16.2f}")
t0 = time.perf_counter(); tot, rej, acc = total_bills("big_50000.txt"); print(f"repaired total_bills (Decimal, validation): {time.perf_counter()-t0:.3f} s, total {tot}, rejected {len(rej)}")
print("\n=== D. Why paise matter: int() vs float vs Decimal ===")
print("int('1250.50') ->", end=" ")
try: int("1250.50")
except ValueError as e: print("ValueError:", e, "(so the original silently DROPS every bill with paise)")
print("float: 0.1 + 0.2 =", 0.1 + 0.2, "| Decimal('0.1') + Decimal('0.2') =", __import__("decimal").Decimal("0.1") + __import__("decimal").Decimal("0.2"))
os.remove("big_50000.txt")
