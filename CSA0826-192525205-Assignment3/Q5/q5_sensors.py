"""Q5 - cold-storage temperatures: loop, comprehension, map/filter, enumerate, comprehensions of other kinds."""
import random

LOW_ERR, HIGH_ERR = -50, 50          # outside this range the sensor is faulty
SAFE_LOW, SAFE_HIGH = 2, 8           # vaccines must stay inside this range

def make_temps(n, error_rate=0.05, seed=5):
    rnd = random.Random(seed)
    return [round(rnd.uniform(60, 99), 1) if rnd.random() < error_rate else round(rnd.gauss(5, 2.5), 1) for _ in range(n)]

# ---- version 1: for loop with append ----
def clean_loop(readings):
    celsius, fahrenheit = [], []
    for c in readings:
        if LOW_ERR <= c <= HIGH_ERR:
            celsius.append(c)
            fahrenheit.append(round(c * 9 / 5 + 32, 2))
    return celsius, fahrenheit

# ---- version 2: list comprehensions with conditions ----
def clean_comp(readings):
    celsius = [c for c in readings if LOW_ERR <= c <= HIGH_ERR]
    fahrenheit = [round(c * 9 / 5 + 32, 2) for c in readings if LOW_ERR <= c <= HIGH_ERR]
    return celsius, fahrenheit

# ---- version 3: map() and filter() with lambda ----
def clean_map(readings):
    valid = list(filter(lambda c: LOW_ERR <= c <= HIGH_ERR, readings))
    return valid, list(map(lambda c: round(c * 9 / 5 + 32, 2), valid))

def alarms(readings):
    """Minutes (0-based index in the ORIGINAL log) of valid readings outside 2-8 C, using enumerate()."""
    return [minute for minute, c in enumerate(readings) if LOW_ERR <= c <= HIGH_ERR and not SAFE_LOW <= c <= SAFE_HIGH]

if __name__ == "__main__":
    sample = [4.5, 99.0, 7.9, 8.1, -60.0, 2.0, 1.9, 5.5, 50.0, -50.0, 3.3]
    print("sample readings:", sample)
    for name, f in (("for loop + append", clean_loop), ("list comprehension", clean_comp), ("map + filter + lambda", clean_map)):
        c, fa = f(sample)
        print(f"{name:<22} Celsius {c}\n{'':<22} Fahrenheit {fa}")
    assert clean_loop(sample) == clean_comp(sample) == clean_map(sample)
    print("the three versions are identical on the sample: True")
    print("alarm minutes (enumerate):", alarms(sample), "-> readings", [sample[m] for m in alarms(sample)])
    print("   (99.0 and -60.0 are sensor errors and are NOT alarms; 50.0 and -50.0 are valid, so they ARE alarms)")

    print("\nGeneral form:  [ expression  for item in iterable  if condition ]   ==   result = []; for item in iterable: if condition: result.append(expression)")
    print("\nOther comprehensions on the same data:")
    valid, _ = clean_comp(sample)
    print("  dict comprehension (minute -> Fahrenheit):", {m: round(c * 9 / 5 + 32, 1) for m, c in enumerate(sample) if LOW_ERR <= c <= HIGH_ERR})
    print("  set comprehension (distinct whole-degree values):", sorted({round(c) for c in valid}))
    print("  generator expression:", (c for c in valid), "-> sum of valid:", round(sum(c for c in valid), 1))
    print("  nested conditions in one comprehension (hard to read):", [("LOW" if c < SAFE_LOW else "HIGH") for c in sample if LOW_ERR <= c <= HIGH_ERR if not SAFE_LOW <= c <= SAFE_HIGH])

    print("\nTests:")
    allvalid, allbad = [3.0, 4.0, 5.0], [75.0, -80.0, 120.0]
    for label, data in (("all valid", allvalid), ("all invalid", allbad), ("empty", [])):
        print(f"  {label:<12} loop={clean_loop(data)} comp={clean_comp(data)} map={clean_map(data)} alarms={alarms(data)}")
        assert clean_loop(data) == clean_comp(data) == clean_map(data)
    big = make_temps(100000)
    assert clean_loop(big) == clean_comp(big) == clean_map(big)
    print("  100,000 random readings: the three versions give identical lists: True;", len(clean_loop(big)[0]), "valid,", len(alarms(big)), "alarm minutes")
