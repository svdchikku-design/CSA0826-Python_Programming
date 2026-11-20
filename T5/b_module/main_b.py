"""Organisation (b): main script that imports the module."""
import sys
import attendance_lib as lib

def main(folder="data", out="."):
    records, damaged = lib.read_month(folder)
    table = lib.attendance_table(records)
    lib.write_summary(table, f"{out}/summary.csv")
    lib.write_below(lib.below_threshold(table), f"{out}/below75.txt")
    lib.write_damaged(damaged, f"{out}/damaged.log")
    print(f"{len(records)} records, {len(table)} students, {len(damaged)} damaged")

if __name__ == "__main__":
    main(*sys.argv[1:3])
