"""Task 3.4: replace the specific except clauses with `except Exception: pass`, add a typing error, and see what happens."""
import os, tempfile

def summarise_specific(path):
    present = absent = 0
    with open(path) as f:
        for line in f:
            try:
                reg, date, status = line.strip().split(",")
                if status == "P": present += 1
                elif status == "A": absent += 1
                else: raise ValueError("bad status")
            except ValueError:
                pass
    return present, absent

def summarise_misused(path):
    present = absent = 0
    with open(path) as f:
        for line in f:
            try:
                reg, date, status = line.strip().split(",")
                if status == "P": presnt += 1          # TYPING ERROR: 'presnt' instead of 'present'
                elif status == "A": absent += 1
                else: raise ValueError("bad status")
            except Exception:
                pass
    return present, absent

def summarise_typo_specific(path):
    present = absent = 0
    with open(path) as f:
        for line in f:
            try:
                reg, date, status = line.strip().split(",")
                if status == "P": presnt += 1          # same typing error, but only ValueError is caught
                elif status == "A": absent += 1
                else: raise ValueError("bad status")
            except ValueError:
                pass
    return present, absent

with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as t:
    t.write("1,d,P\n2,d,A\n3,d,P\n4,d,P\n5,d\n")
print("correct code, 3 present, 1 absent, 1 damaged line   ->", summarise_specific(t.name), "(expected (3, 1))")
print("typing error + except Exception: pass               ->", summarise_misused(t.name), "  <- WRONG, no message at all")
try: summarise_typo_specific(t.name)
except Exception as e: print("typing error + except ValueError (specific)         -> stops at once:", type(e).__name__ + ":", e)
print("\nWhy hidden: 'presnt += 1' raises UnboundLocalError (a NameError subclass). UnboundLocalError is an Exception, so")
print("'except Exception: pass' catches it and throws it away on every P line; present stays 0 and nobody is told.")
print("issubclass(UnboundLocalError, Exception) =", issubclass(UnboundLocalError, Exception), "| issubclass(UnboundLocalError, ValueError) =", issubclass(UnboundLocalError, ValueError))
os.remove(t.name)
