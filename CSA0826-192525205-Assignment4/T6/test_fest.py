"""Task 6 Stage 5: automated demonstration of each required case, plus extra failure cases."""
import os, tempfile, shutil
from unittest import mock
from fest.validate import is_valid_email, parse_registration, InvalidRegistration
from fest.processor import run, process_file

print("1. E-mail validation with string methods")
cases = {"arun@simats.edu.in": True, "a@b.co": True, "bala@simats": False, "gokul@@x.in": False, "kavin simats.edu.in": False,
         "@x.in": False, "a@.in": False, "a@x.": False, "a@x..in": False, "a@x.c": False, "": False}
bad = 0
for e, expect in cases.items():
    got = is_valid_email(e); bad += got != expect
    print(f"   {e!r:<24} -> {got!s:<5} (expected {expect}) {'OK' if got == expect else 'WRONG'}")
assert bad == 0

print("\n2. Single-line parsing")
print("   ", parse_registration("192300005,Elango,cse,ELANGO@simats.edu.in,mime ; quiz;MIME"))
for line in ("1,2,3", "192300001,,CSE,a@b.in,Quiz", "192300001,X,,a@b.in,Quiz", "192300001,X,CSE,a@b.in, ; "):
    try: parse_registration(line)
    except InvalidRegistration as e: print(f"    {line!r:<34} -> InvalidRegistration: {e}")

print("\n3. Whole-program cases (data_demo/)")
out = tempfile.mkdtemp()
master, errors, stats, counts = run("data_demo", out)
kinds = [k for k, *_ in errors]
checks = {
  "clean lines accepted (7 unique students)": stats["unique students"] == 7,
  "duplicate registration kept once, events merged": kinds.count("DUPLICATE") == 1 and master["192300001"][3] == {"Dance", "Quiz", "Drama"},
  "invalid e-mail rejected and logged with file and line": ("INVALID", "CSE.txt", 2, "invalid e-mail 'bala@simats'") in errors,
  "damaged line (3 fields) logged": ("DAMAGED", "CSE.txt", 4, "expected 5 fields, found 3") in errors,
  "missing department file (IT.txt) logged, run completed": ("MISSING", "IT.txt", 0, "department file not found") in errors and stats["files read"] == 4,
  "blank line skipped, not an error": all(not (f == "CSE.txt" and n == 5) for _, f, n, _ in errors),
  "no rejected student in the master list": not any(r in master for r in ("192300002", "192300007", "192300011")),
}
for name, ok in checks.items(): print(f"   [{'PASS' if ok else 'FAIL'}] {name}"); assert ok

print("\n4. Extra failure cases the program must survive")
tmp = tempfile.mkdtemp()
open(os.path.join(tmp, "CSE.txt"), "wb").write(b"192300001,Arun,CSE,arun@simats.edu.in,Quiz\n192300002,Caf\xe9,CSE,c@simats.edu.in,Quiz\n")
m, e, s, c = run(tmp, os.path.join(tmp, "o"))
print("   Latin-1 byte in CSE.txt  ->", [x for x in e if x[1] == "CSE.txt"], "| students kept:", s["unique students"])
assert s["unique students"] == 2
os.makedirs(os.path.join(tmp, "ECE.txt"))
m, e, s, c = run(tmp, os.path.join(tmp, "o2"))
print("   a folder named ECE.txt   ->", [x for x in e if x[1] == "ECE.txt"][:1] or "no entry")
with mock.patch("builtins.open", side_effect=PermissionError(13, "denied")):
    st = {"files read": 0, "missing files": 0, "unreadable files": 0, "lines read": 0, "unique students": 0, "duplicates": 0, "invalid records": 0, "damaged lines": 0, "encoding warnings": 0}
    ee = []; process_file("CSE.txt", {}, {}, ee, st)
print("   permission denied (simulated; sandbox runs as root) ->", ee)
m, e, s, c = run(os.path.join(tmp, "no_such_folder"), os.path.join(tmp, "o3"))
print("   whole input folder missing -> run completed, missing files:", s["missing files"], "| master written:", os.path.exists(os.path.join(tmp, "o3", "master.csv")))
shutil.rmtree(tmp); shutil.rmtree(out)
print("\nAll checks passed.")
