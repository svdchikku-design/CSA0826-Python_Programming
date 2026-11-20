"""Task 3 - named constants, dynamic typing, swapping, and the alternatives."""
import time

# ---------------- single block of named constants (the ONLY place to revise a rate) ----------------
BASE_RATE = 30.00
STD_FAT = 3.5
STD_SNF = 8.5
STEP = 0.1
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
FAT_MIN, FAT_MAX = 2.0, 7.0
SNF_MIN, SNF_MAX = 6.0, 10.0

def rate_per_litre(fat, snf):
    return round(BASE_RATE + round((fat - STD_FAT) / STEP) * FAT_STEP_VALUE
                 + round((snf - STD_SNF) / STEP) * SNF_STEP_VALUE, 2)

print("rate for fat 4.2, snf 8.7 :", rate_per_litre(4.2, 8.7))

print("\n--- Python has no true constants: the name can be re-bound ---")
BASE_RATE = 99.0
print("after BASE_RATE = 99.0 -> rate :", rate_per_litre(4.2, 8.7), "(nothing stopped us; UPPER_CASE is only a convention)")
BASE_RATE = 30.00

print("\n--- Dynamic typing: one name, different types ---")
x = 8
print(x, type(x).__name__)
x = "eight"
print(x, type(x).__name__)
x = 8.5
print(x, type(x).__name__)

print("\n--- Multiple assignment and swapping ---")
litres, fat, snf = 10.0, 3.5, 8.5
print("litres, fat, snf =", litres, fat, snf)
a, b = 3.5, 8.5
a, b = b, a
print("after a, b = b, a ->", a, b)
x = y = 0
print("chained x = y = 0 ->", x, y)

# ---------------- Alternative 1: magic numbers - the partial-revision bug of the volunteer ----------------
def rate_for_slip(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)
def rate_for_report(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)
import inspect
print("\n--- Magic numbers: how many places hold the fat step 0.40? ---")
print("copies of the literal 0.40 in two magic-number functions :", sum(inspect.getsource(f).count("0.40") for f in (rate_for_slip, rate_for_report)))
print("occurrences of FAT_STEP_VALUE assignment (constants)  : 1")
# simulate a revision to 0.45 applied to only one copy
def rate_for_slip_revised(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.45 + round((snf - 8.5) / 0.1) * 0.30, 2)
print("slip (revised)  :", rate_for_slip_revised(4.2, 8.7))
print("report (missed) :", rate_for_report(4.2, 8.7), " <- the two documents now disagree")

# ---------------- Alternative 2: dictionary RATE_CARD ----------------
RATE_CARD = {"base": 30.0, "fat": 0.40, "snf": 0.30}
def rate_dict(fat, snf):
    return round(RATE_CARD["base"] + round((fat - 3.5) / 0.1) * RATE_CARD["fat"]
                 + round((snf - 8.5) / 0.1) * RATE_CARD["snf"], 2)
assert rate_dict(4.2, 8.7) == rate_per_litre(4.2, 8.7) == 33.40
RATE_CARD["fat"] = 0.45        # one place; a typo such as RATE_CARD["fatt"] would only fail at run time
print("\ndictionary after revision to 0.45 :", rate_dict(4.2, 8.7))

# running time of the three styles
def t(fn, n=200000):
    t0 = time.perf_counter()
    for _ in range(n):
        fn(4.2, 8.7)
    return (time.perf_counter() - t0) / n * 1e6
BASE_RATE, FAT_STEP_VALUE = 30.0, 0.40
RATE_CARD["fat"] = 0.40
print("\nmicroseconds per call (200000 calls)")
print(f"  magic numbers    : {t(rate_for_slip):.3f}")
print(f"  named constants  : {t(rate_per_litre):.3f}")
print(f"  dictionary       : {t(rate_dict):.3f}")
