"""Reporting: write the output files."""

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

