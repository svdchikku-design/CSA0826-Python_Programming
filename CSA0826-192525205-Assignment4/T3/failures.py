"""Task 3.1 / 3.3: provoke every failure and record the exception; complete try/except/else/finally and raise ... from ..."""
import os, stat, tempfile, shutil
from pathlib import Path

class InvalidRecord(Exception):
    """A line is not in the format register,date,P|A. Raised in parse_line, handled in process_file (one level up)."""

def parse_line(line):
    try:
        reg, date, status = line.strip().split(",")        # ValueError if not exactly 3 fields
    except ValueError as e:
        raise InvalidRecord(f"expected 3 fields: {line.strip()!r}") from e     # keeps the original cause
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status {status!r}")
    return reg, date, status

def process_file(path):
    """Complete try statement: try / except (specific) / else / finally."""
    present = absent = 0; bad = []; opened = False
    try:
        f = open(path, encoding="utf-8"); opened = True
        for n, line in enumerate(f, 1):
            if not line.strip(): continue
            try:
                _, _, status = parse_line(line)
            except InvalidRecord as e:
                bad.append((n, str(e), repr(e.__cause__)))
            else:
                if status == "P": present += 1
                else: absent += 1
    except FileNotFoundError: return "FileNotFoundError", None
    except PermissionError: return "PermissionError", None
    except IsADirectoryError: return "IsADirectoryError", None
    except UnicodeDecodeError as e: return f"UnicodeDecodeError ({e.reason})", None
    else:
        status_text = "empty file (no records)" if present + absent + len(bad) == 0 else "ok"
        return status_text, (present, absent, bad)
    finally:
        if opened: f.close()                               # runs on success AND on every error

tmp = tempfile.mkdtemp()
def mk(name, content, mode="w", **kw):
    p = os.path.join(tmp, name)
    with open(p, mode, **kw) as f: f.write(content)
    return p
cases = []
cases.append(("missing folder", lambda: list(Path(tmp, "no_folder").iterdir())))
cases.append(("missing file", lambda: process_file(os.path.join(tmp, "nofile.txt"))))
unreadable = mk("locked.txt", "1,2026-10-01,P\n"); os.chmod(unreadable, 0)
def simulated_denied():
    # this sandbox runs as the administrator (root), who can read a chmod 000 file, so the denial is SIMULATED
    from unittest import mock
    with mock.patch("builtins.open", side_effect=PermissionError(13, "Permission denied")):
        return process_file("locked.txt")
cases.append(("permission denied (SIMULATED with unittest.mock; real chmod 000 is readable by root)", simulated_denied))
latin = mk("latin1.txt", "192311001,2026-10-01,P\ncaf\xe9,2026-10-01,A\n".encode("latin-1"), "wb")
cases.append(("wrong encoding (file is Latin-1, read as UTF-8)", lambda: process_file(latin)))
cases.append(("path is a folder", lambda: process_file(tmp)))
cases.append(("empty file", lambda: process_file(mk("empty.txt", ""))))
cases.append(("damaged line (2 fields, bad status)", lambda: process_file(mk("bad.txt", "1,2026-10-01,P\n2,2026-10-01\n3,2026-10-01,L\n"))))
print(f"{'situation':<48} {'what happened'}")
for name, fn in cases:
    try:
        r = fn(); print(f"{name:<48} {r}")
    except Exception as e:
        print(f"{name:<48} raised {type(e).__name__}: {e}")
print("\nraise ... from ...: the damaged-line cause is kept ->")
try: parse_line("2,2026-10-01")
except InvalidRecord as e: print("  ", repr(e), "| __cause__ =", repr(e.__cause__))
print("\nraw built-in exceptions for a damaged line (without InvalidRecord):")
for raw in ("2,2026-10-01", "x,y,P,extra"):
    try: reg, date, st = raw.split(",")
    except ValueError as e: print(f"   {raw!r}: ValueError: {e}")
try: raw = "2,2026-10-01".split(",")[2]
except IndexError as e: print("   indexing parts[2] on a short line: IndexError:", e)
os.chmod(unreadable, 0o600); shutil.rmtree(tmp)
