import os
import tempfile

class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""

def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    # TODO 1: Raise InvalidRecord if there are not exactly 3 fields or the status is
    # not P or A; otherwise return the 3 fields as a tuple
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    if parts[2] not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{parts[2]}'")
    return tuple(parts)

def summarise(path):
    present, absent, errors = 0, 0, []
    # TODO 2: Open the file with a with statement, parse each line inside try/except
    # InvalidRecord, count P and A, and record (line number, message) for bad lines
    try:
        with open(path, encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                try:
                    reg, date, status = parse_line(line)
                except InvalidRecord as e:
                    errors.append((number, str(e)))
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
    except FileNotFoundError:                 # extra exercise: a missing file is reported, not a crash
        errors.append((0, f"file not found: {path}"))
    return present, absent, errors

data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
"192311003,2026-10-08\n192311004,2026-10-08,L\n")
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
encoding="utf-8") as tmp:
    tmp.write(data)
print(summarise(tmp.name))
os.remove(tmp.name)
print(summarise("no_such_file.csv"))      # the exercise: a name that does not exist
