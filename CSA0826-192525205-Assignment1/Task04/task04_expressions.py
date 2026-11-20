"""Task 4 - expressions, precedence, rounding surprises, and int()/floor alternatives."""
import math

STD_FAT, STD_SNF, STEP = 3.5, 8.5, 0.1
BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = 30.00, 0.40, 0.30

def show(label, value):
    print(f"{label:<42} -> {value!r}")

print("=== Surprising results ===")
show("(4.2 - 3.5) / 0.1", (4.2 - 3.5) / 0.1)                 # surprise 1
show("round((4.2 - 3.5) / 0.1)", round((4.2 - 3.5) / 0.1))
show("(3.5 - 3.1) / 0.1", (3.5 - 3.1) / 0.1)                 # surprise 2
show("int((3.5 - 3.1) / 0.1)", int((3.5 - 3.1) / 0.1))
show("-2 ** 2", -2 ** 2)                                     # surprise 3
show("(-2) ** 2", (-2) ** 2)
show("2 ** 3 ** 2", 2 ** 3 ** 2)                             # right-associative
show("2 ** -1", 2 ** -1)
show("round(2.5), round(3.5), round(0.5)", (round(2.5), round(3.5), round(0.5)))   # surprise 4
show("10 - 4 - 3  (left to right)", 10 - 4 - 3)
show("100 / 10 / 5", 100 / 10 / 5)

print("\n=== round() vs int() vs math.floor() on negative values ===")
for v in (-3.5, -3.9, -0.4, 3.9):
    print(f"value {v:5}: round={round(v):3}  int={int(v):3}  floor={math.floor(v):3}")

print("\n=== Comparison chaining and Boolean operators ===")
for fat in (1.9, 2.0, 4.2, 7.0, 7.1):
    chained = 2.0 <= fat <= 7.0
    long_form = fat >= 2.0 and fat <= 7.0
    print(f"fat={fat}: 2.0 <= fat <= 7.0 -> {chained}; same as 'and' form -> {long_form}; invalid = {not chained}")
show("1 < 2 < 3 and 3 > 2 > 5", 1 < 2 < 3 and 3 > 2 > 5)
show("True or 1/0   (short-circuit)", True or 1 / 0)

print("\n=== The four expressions of the calculator ===")
def rate_per_litre(fat, snf, how=round):
    fat_steps = how((fat - STD_FAT) / STEP)
    snf_steps = how((snf - STD_SNF) / STEP)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
fat, snf, litres = 4.2, 8.7, 8.5
fat_steps = round((fat - STD_FAT) / STEP)
snf_steps = round((snf - STD_SNF) / STEP)
rate = round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
amount = round(litres * rate, 2)
print(f"fat_steps={fat_steps}  snf_steps={snf_steps}  rate={rate}  amount={amount}")

print("\n=== Alternative: int() or math.floor() instead of round() (snf fixed at 8.5) ===")
print(f"{'fat':>5} {'raw steps':>20} | {'round':>6} {'int':>6} {'floor':>6} | rate(round) rate(int) rate(floor)")
for fat in (4.2, 3.1, 3.8):
    raw = (fat - STD_FAT) / STEP
    r = [rate_per_litre(fat, 8.5, how) for how in (round, int, math.floor)]
    s = [round(raw), int(raw), math.floor(raw)]
    print(f"{fat:>5} {raw:>20.16f} | {s[0]:>6} {s[1]:>6} {s[2]:>6} | {r[0]:>11} {r[1]:>8} {r[2]:>10}")
print("correct rate for fat 3.1 = 30.00 - 4 * 0.40 = 28.40 ; for fat 4.2 = 30.00 + 7 * 0.40 = 32.80 ; for fat 3.8 = 30.00 + 3 * 0.40 = 31.20")
