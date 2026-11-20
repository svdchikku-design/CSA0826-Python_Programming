"""Task 4.2: run process() for three days and show every defect."""
import os, tempfile, gc, importlib
os.chdir(tempfile.mkdtemp())                       # work in a scratch folder
import sys; sys.path.insert(0, "/home/claude/csa08_a4/T4")
import defective

def day(name, books): open(name, "w").write("\n".join(books))
day("mon.txt", ["Python Crash Course", "Algorithms Unlocked"])
day("tue.txt", ["Data Structures in C", "Clean Code", "SICP"])
day("wed.txt", ["Operating System Concepts"])
print("=== Defect 1 and 2: three days processed, then the log is printed ===")
for d in ("mon.txt", "tue.txt", "wed.txt"):
    defective.process(d)
print(repr(open("returns.log").read()))
print("-> only Wednesday's book survives (mode 'w' truncates the file on every open) -> Monday and Tuesday are lost")
day("tue.txt", ["Data Structures in C", "Clean Code", "SICP"])
defective.process("tue.txt")
print("Tuesday alone:", repr(open("returns.log").read()), " -> titles run together: write(b) adds no newline")

print("\n=== Defect 3: a write() fails while the log is open ===")
def fds(): return len(os.listdir("/proc/self/fd"))
before = fds()
real_open = open
def failing_open(path, mode="r", *a, **k):
    f = real_open(path, mode, *a, **k)
    if path == "returns.log":
        orig = f.write; calls = []
        def w(s):
            calls.append(1)
            if len(calls) == 2: raise OSError("disk full (simulated)")
            return orig(s)
        class Wrap:                                  # file object that fails on the 2nd write
            write = staticmethod(w); close = staticmethod(f.close)
        wr = Wrap(); wr._f = f; defective_files.append(f); return wr
    return f
defective_files = []
import builtins; builtins.open = failing_open
day("thu.txt", ["Book A", "Book B", "Book C"])
try: defective.process("thu.txt")
except OSError as e: print("   process() let the error escape (only FileNotFoundError is caught):", e)
builtins.open = real_open
f = defective_files[0]
print("   log file still open after the error:", not f.closed, "| open descriptors", before, "->", fds())
print("   data written before the failure may still be in the buffer, not on disk; the traceback was not saved anywhere")
print("   missing file is reported with only the word 'missing':", end=" "); defective.process("nofile.txt")
print("   (no file name, no date, nothing written to a log - the office cannot tell which day failed)")
f.close()
