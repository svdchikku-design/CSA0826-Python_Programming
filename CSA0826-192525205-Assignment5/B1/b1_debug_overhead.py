"""A4 alternative measured: cost of thousands of print / logging calls, and how each is switched off."""
import io, logging, sys, time, contextlib
N = 100000
def work():                                            # one unit of 'real' work: clean one value
    return round(max(0.0, 53.7) * 1.0, 1)
def base():
    for i in range(N): work()
def with_print():
    for i in range(N):
        work(); print("DEBUG cleaned row", i, file=out)
def with_print_flag(DEBUG=False):
    for i in range(N):
        work()
        if DEBUG: print("DEBUG cleaned row", i, file=out)
def with_logging_off():
    for i in range(N):
        work(); log.debug("cleaned row %d", i)
def with_logging_on():
    for i in range(N):
        work(); log.debug("cleaned row %d", i)
out = io.StringIO()
log = logging.getLogger("clean"); log.propagate = False
def t(fn):
    best = 9
    for _ in range(3):
        out.seek(0); out.truncate(0); t0 = time.perf_counter(); fn(); best = min(best, time.perf_counter() - t0)
    return best
b = t(base)
log.setLevel(logging.WARNING)                                   # debug messages switched off: one setting
off = t(with_logging_off)
h = logging.StreamHandler(io.StringIO()); h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s")); log.addHandler(h); log.setLevel(logging.DEBUG)
on = t(with_logging_on)
log.removeHandler(h)
fh = logging.FileHandler("/tmp/debug_demo.log", mode="w"); fh.setFormatter(logging.Formatter("%(asctime)s %(message)s")); log.addHandler(fh)
tf = t(with_logging_on); log.removeHandler(fh); fh.close()
real = open("/tmp/print_demo.txt", "w")
def with_print_file():
    for i in range(N):
        work(); print("DEBUG cleaned row", i, file=real)
tp_file = t(with_print_file); real.close()
print(f"{N:,} calls added to a loop whose useful work takes {b*1e3:.1f} ms in total (best of 3)")
print(f"{'variant':<58}{'time (ms)':>10}{'extra vs no debugging':>24}")
for name, v in (("no debugging", b), ("print to an in-memory buffer", t(with_print)), ("print to a file", tp_file),
                ("print guarded by a DEBUG flag, flag False", t(with_print_flag)), ("logging.debug, level WARNING (switched off)", off),
                ("logging.debug, level DEBUG, formatted, in memory", on), ("logging.debug, level DEBUG, to a file", tf)):
    print(f"{name:<58}{v*1e3:>10.1f}{(v-b)*1e3:>21.1f} ms")
print("\nSwitching off: print needs every statement deleted or wrapped in an 'if DEBUG' test (easy to forget one); logging needs ONE line:")
print("   logging.getLogger().setLevel(logging.WARNING)   # or the command-line option --log-level; the debug calls stay in the code")
