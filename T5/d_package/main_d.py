"""Organisation (d): main script using the package attendance/."""
import sys
from attendance import reader, stats, report

def main(folder="data", out="."):
    records, damaged = reader.read_month(folder)
    table = stats.attendance_table(records)
    report.write_summary(table, f"{out}/summary.csv")
    report.write_below(stats.below_threshold(table), f"{out}/below75.txt")
    report.write_damaged(damaged, f"{out}/damaged.log")
    print(f"{len(records)} records, {len(table)} students, {len(damaged)} damaged")

if __name__ == "__main__":
    main(*sys.argv[1:3])
