"""Task 2: monthly attendance processor. Reads every daily file once, accumulates counts in a dictionary."""
import sys
from pathlib import Path

def process_month(folder, summary_out, below_out, log_out, threshold=75.0):
    counts = {}                                   # regno -> [present, absent]
    damaged = []                                  # (file name, line number, message)
    files = sorted(Path(folder).glob("*.txt"))    # pathlib lists the daily files in a fixed order
    for path in files:
        with open(path, "r", encoding="utf-8") as f:           # r: only reading; iteration: one line at a time
            for number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue                                    # blank line is not damage
                parts = line.split(",")
                if len(parts) != 3:
                    damaged.append((path.name, number, f"expected 3 fields, found {len(parts)}")); continue
                reg, date, status = (p.strip() for p in parts)
                if status not in ("P", "A"):
                    damaged.append((path.name, number, f"invalid status '{status}'")); continue
                rec = counts.setdefault(reg, [0, 0])
                rec[0 if status == "P" else 1] += 1
    rows = []
    for reg in sorted(counts):
        p, a = counts[reg]
        rows.append((reg, p, a, 100.0 * p / (p + a)))
    with open(summary_out, "w", encoding="utf-8") as out:      # w: report is rebuilt completely every run
        out.write("register_no,present,absent,percent\n")
        for reg, p, a, pct in rows:
            out.write(f"{reg},{p},{a},{pct:.1f}\n")
    with open(below_out, "w", encoding="utf-8") as out:
        for reg, p, a, pct in rows:
            if pct < threshold:
                out.write(f"{reg},{pct:.1f}\n")
    with open(log_out, "w", encoding="utf-8") as out:          # the log is per run; use "a" to keep history across runs
        for name, number, msg in damaged:
            out.write(f"{name},{number},{msg}\n")
    return rows, damaged, len(files)

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "data_oct_small"
    rows, damaged, nfiles = process_month(folder, "attendance_summary.csv", "below75.txt", "damaged.log")
    print(f"{nfiles} file(s) read, {len(rows)} students, {len(damaged)} damaged line(s)")
    for r in rows: print("  %s present=%d absent=%d  %.1f%%" % r)
    print("damaged:", damaged)
