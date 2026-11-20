"""B2: the cleaning pipeline given adversarial files. First the naive loader (common/cleaning.clean_file), then a defensive loader."""
import csv, io, os, sys
sys.path.insert(0, "../common")
from cleaning import clean_file, clean_rows

REQUIRED = ["station", "date", "hour", "pm25", "pm10", "no2", "temp"]

class BadFile(Exception):
    """A whole file cannot be used. Handled once per file by the caller, which logs it and goes on to the next file."""

def read_text(path):
    raw = open(path, "rb").read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16"), "utf-16 (byte-order mark)"
    try:
        return raw.decode("utf-8-sig"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("cp1252"), "cp1252 (fallback: not valid UTF-8; check names)"

def safe_load(path, stats=None):
    text, enc = read_text(path)
    if not text.strip():
        raise BadFile("file is empty")
    header = text.splitlines()[0]
    delim = max(",;\t|", key=header.count)                    # the most frequent candidate delimiter in the header line
    if header.count(delim) == 0:
        raise BadFile("cannot find a delimiter in the header line")
    rows = list(csv.DictReader(io.StringIO(text), delimiter=delim))
    missing = [c for c in REQUIRED if c not in (rows[0].keys() if rows else header.split(delim))]
    if missing:
        raise BadFile(f"missing column(s): {', '.join(missing)}")
    if not rows:
        raise BadFile("header only, no data rows")
    return clean_rows(rows, stats), enc, delim

print(f"{'file':<22}{'NAIVE loader (clean_file)':<52}DEFENSIVE loader (safe_load)")
for name in ("good.csv", "missing_column.csv", "wrong_delimiter.csv", "latin1_encoding.csv", "utf16_encoding.csv", "empty.csv", "header_only.csv"):
    path = os.path.join("bad_files", name)
    try: naive = f"{len(clean_file(path))} row(s) cleaned"
    except Exception as e: naive = f"{type(e).__name__}: {e}"[:50]
    try:
        rows, enc, delim = safe_load(path)
        defensive = f"{len(rows)} row(s); encoding {enc}; delimiter {delim!r}" + (f"; station {rows[0]['station']!r}" if rows else "")
    except BadFile as e: defensive = f"BadFile: {e} -> logged, file skipped"
    print(f"{name:<22}{naive:<52}{defensive}")
