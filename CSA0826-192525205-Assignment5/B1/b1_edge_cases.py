"""Edge cases for the completed functions (not part of the given program)."""
import sys, io
sys.path.insert(0, ".")
src = open("given_b1_completed.py").read().split("clean = load_clean(RAW)")[0]
ns = {}; exec(src, ns)
for label, values in (("all equal", [50.0, 50.0]), ("one value", [7.0]), ("empty", [])):
    try: print(f"min_max({label}: {values}) ->", ns["min_max"](values))
    except Exception as e: print(f"min_max({label}: {values}) -> {type(e).__name__}: {e}")
print("load_clean('') ->", end=" ")
try: print(ns["load_clean"](""))
except Exception as e: print(type(e).__name__, e)
print("load_clean with junk 'abc' ->", end=" ")
try: print(ns["load_clean"]("station,date,pm25\nA,2026-10-01,abc\n"))
except Exception as e: print(f"{type(e).__name__}: {e}  (the given TODO converts with float(); common/cleaning.py handles this with to_number())")
