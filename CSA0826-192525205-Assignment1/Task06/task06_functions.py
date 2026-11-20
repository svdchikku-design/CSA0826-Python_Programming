"""Task 6 - functions, return vs print, scope, docstrings."""
BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STD_FAT, STD_SNF, STEP = 3.5, 8.5, 0.1

def rate_per_litre(fat, snf):
    """Return the price per litre (float, 2 decimals) for the given fat % and SNF %."""
    fat_steps = round((fat - STD_FAT) / STEP)
    snf_steps = round((snf - STD_SNF) / STEP)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)

def payout(litres, fat, snf):
    """Return the amount payable for one entry, rounded to 2 decimals."""
    return round(litres * rate_per_litre(fat, snf), 2)

def ten_day_total(entries):
    """Return the total of payout() over a list of (litres, fat, snf) tuples."""
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)

def show_payout(litres, fat, snf):
    """Print (do not return) one payment line."""
    print(f"  printed: {litres} L at {rate_per_litre(fat, snf)} = {payout(litres, fat, snf)}")

entries = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
print("rate_per_litre(4.2, 8.7) =", rate_per_litre(4.2, 8.7))
print("payout(8.5, 4.2, 8.7)    =", payout(8.5, 4.2, 8.7))
print("ten_day_total(entries)   =", ten_day_total(entries))

print("\n--- returning versus printing ---")
x = show_payout(10, 3.5, 8.5)
print("value returned by show_payout :", x, "(None - cannot be added or stored)")
y = payout(10, 3.5, 8.5)
print("value returned by payout      :", y, "-> y + 1 =", y + 1)

print("\n--- local and global names ---")
def local_copy():
    BASE_RATE = 99.0              # creates a NEW local name; the global is untouched
    return BASE_RATE
print("local_copy() returned", local_copy(), "| global BASE_RATE is still", BASE_RATE)
def broken_update():
    BASE_RATE = BASE_RATE + 1     # assignment makes BASE_RATE local, so reading it first fails
    return BASE_RATE
try:
    broken_update()
except UnboundLocalError as e:
    print("UnboundLocalError:", e)
print("reading a global inside a function is fine:", rate_per_litre(3.5, 8.5), "(uses BASE_RATE = 30.0)")
print("\n--- docstrings ---")
for f in (rate_per_litre, payout, ten_day_total):
    print(f"{f.__name__}: {f.__doc__}")
