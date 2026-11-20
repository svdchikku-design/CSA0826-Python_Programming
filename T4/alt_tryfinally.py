"""Task 4 alternative: manual open/close in try/finally versus with. Same complexity; compare open files after errors."""
import os, tempfile, time
os.chdir(tempfile.mkdtemp())

def write_manual(path, items, fail_at=None):
    f = open(path, "a")
    try:
        for i, b in enumerate(items):
            if i == fail_at: raise OSError("simulated failure")
            f.write(b + "\n")
    finally:
        f.close()                      # must be remembered by the programmer

def write_with(path, items, fail_at=None):
    with open(path, "a") as f:
        for i, b in enumerate(items):
            if i == fail_at: raise OSError("simulated failure")
            f.write(b + "\n")

def write_original(path, items, fail_at=None, keep=[]):
    f = open(path, "w"); keep.append(f)   # original style: close() only on the success path (kept in a list so it is not garbage-collected)
    for i, b in enumerate(items):
        if i == fail_at: raise OSError("simulated failure")
        f.write(b)
    f.close()

def fds(): return len(os.listdir("/proc/self/fd"))
items = ["book"] * 5
print(f"{'version':<26}{'errors':>8}{'open files before':>19}{'open files after':>18}{'still open (leaked)':>21}")
for name, fn in (("original (no with/finally)", write_original), ("manual try/finally", write_manual), ("with statement", write_with)):
    b = fds()
    for _ in range(100):
        try: fn("x.log", items, fail_at=2)
        except OSError: pass
    a = fds(); print(f"{name:<26}{100:>8}{b:>19}{a:>18}{a-b:>21}")
print("\nTime for 20,000 successful calls of 5 lines (the complexity is the same, O(lines) per call):")
for name, fn in (("manual try/finally", write_manual), ("with statement", write_with)):
    t0 = time.perf_counter()
    for _ in range(20000): fn("y.log", items)
    print(f"  {name:<22}{time.perf_counter()-t0:.3f} s")
print("\nSpace: both hold exactly one file object and one buffer at a time: O(1) extra. The difference is correctness, not Big-O:")
print("one error in the original leaks 1 open file; with 'with' or a correct try/finally 0 files remain open.")
print("If the programmer forgets close() inside finally, or opens the second file before the try, one file can still leak per error.")
