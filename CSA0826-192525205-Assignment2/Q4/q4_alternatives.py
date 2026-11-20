"""Q4 alternative: write each line straight to a file, or build with io.StringIO, versus join."""
import io, os, time, tracemalloc, tempfile

N = 200_000
def lines():
    for i in range(N):
        yield f"Item{i}:Rs{i % 50};"

def with_join():
    return "".join(list(lines()))                  # holds the list of parts AND the final text

def with_stringio():
    buf = io.StringIO()
    for ln in lines():
        buf.write(ln)
    return buf.getvalue()

def with_file(path):
    with open(path, "w") as fh:                    # nothing is kept in memory except the write buffer
        for ln in lines():
            fh.write(ln)
    return os.path.getsize(path)

path = os.path.join(tempfile.gettempdir(), "statement_demo.txt")
rows = []
for name, fn in (("join of a list of parts", with_join), ("io.StringIO", with_stringio), ("write line by line to a file", lambda: with_file(path))):
    times = []
    for _ in range(3):
        t0 = time.perf_counter(); out = fn(); times.append(time.perf_counter() - t0)
    tracemalloc.start(); fn(); peak = tracemalloc.get_traced_memory()[1] / 1e6; tracemalloc.stop()
    size = len(out) if isinstance(out, str) else out
    rows.append((name, sum(times) / 3, peak, size))
print(f"{N} lines, average of 3 runs")
print(f"{'method':<30}{'time (s)':>10}{'peak memory (MB)':>20}{'output size (chars)':>22}")
for name, t, peak, size in rows:
    print(f"{name:<30}{t:>10.4f}{peak:>20.2f}{size:>22}")
with open(path) as fh:
    assert fh.read() == with_join()
print("file content identical to the joined text: True")
os.remove(path)
