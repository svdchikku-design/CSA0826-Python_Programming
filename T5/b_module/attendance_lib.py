"""Organisation (b): one module of functions."""
from pathlib import Path

def read_month(folder):
    records, damaged = [], []
    for path in sorted(Path(folder).glob("*.txt")):
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    damaged.append((path.name, n, f"expected 3 fields, found {len(parts)}"))
                elif parts[2] not in ("P", "A"):
                    damaged.append((path.name, n, f"invalid status {parts[2]!r}"))
                else:
                    records.append(tuple(parts))
    return records, damaged


def percentage(present, absent):
    total = present + absent
    return 100.0 * present / total if total else 0.0

def attendance_table(records):
    counts = {}
    for reg, date, status in records:
        c = counts.setdefault(reg, [0, 0])
        c[0 if status == "P" else 1] += 1
    return {reg: (p, a, percentage(p, a)) for reg, (p, a) in sorted(counts.items())}

def below_threshold(table, limit=75.0):
    return [(reg, row[2]) for reg, row in table.items() if row[2] < limit]


def write_summary(table, path):
    with open(path, "w", encoding="utf-8") as out:
        out.write("register_no,present,absent,percent\n")
        for reg, (p, a, pct) in table.items():
            out.write(f"{reg},{p},{a},{pct:.1f}\n")

def write_below(rows, path):
    with open(path, "w", encoding="utf-8") as out:
        for reg, pct in rows:
            out.write(f"{reg},{pct:.1f}\n")

def write_damaged(damaged, path):
    with open(path, "w", encoding="utf-8") as out:
        for name, n, msg in damaged:
            out.write(f"{name},{n},{msg}\n")

