"""Task 5 - read clerk entries, check with str methods, convert, print aligned results."""
import sys
from milkrate import rate_per_litre, payout

FAT_MIN, FAT_MAX, SNF_MIN, SNF_MAX, MAX_LITRES = 2.0, 7.0, 6.0, 10.0, 200.0

def is_number(text):
    """str-method check: optional minus, digits, at most one '.'."""
    t = text.strip()
    if t.startswith("-"):
        t = t[1:]
    return t.isdigit() or (t.count(".") == 1 and t.replace(".", "", 1).isdigit())

def read_number(prompt, low, high):
    """Asks until the clerk types a valid number inside [low, high]; returns float."""
    while True:
        text = input(prompt)
        if not sys.stdin.isatty():
            print(text)
        if not is_number(text):
            print(f"   {text!r} is not a number - use digits and a dot, e.g. 8.5")
            continue
        value = float(text)                      # safe: the text was checked first
        if not low <= value <= high:
            print(f"   {value} is outside {low} to {high}")
            continue
        return value

print("input() always returns str:", type(" 8.5 ").__name__, "-> float('8.5') =", float("8.5"), "| int('8') =", int("8"))
for bad in ("8,5", "eight"):
    try:
        float(bad)
    except ValueError as e:
        print(f"float({bad!r}) -> ValueError: {e}")
print()
rows = []
while True:
    fid = input("Farmer ID (DONE to stop): ").strip()
    if not sys.stdin.isatty():
        print(fid)
    if fid.upper() == "DONE":
        break
    litres = read_number("  Litres : ", 0.01, MAX_LITRES)
    fat = read_number("  Fat %  : ", FAT_MIN, FAT_MAX)
    snf = read_number("  SNF %  : ", SNF_MIN, SNF_MAX)
    rows.append((fid, litres, fat, snf))

print(f"\n{'ID':<6}{'Litres':>8}{'Fat':>6}{'SNF':>6}{'Rate':>8}{'Amount':>10}")
total = 0.0
for fid, litres, fat, snf in rows:
    amount = payout(litres, fat, snf)
    total += amount
    print(f"{fid:<6}{litres:>8.2f}{fat:>6.1f}{snf:>6.1f}{rate_per_litre(fat, snf):>8.2f}{amount:>10.2f}")
print(f"{'TOTAL':<34}{total:>10.2f}")
