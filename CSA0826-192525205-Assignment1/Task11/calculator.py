"""Ksheera Milk Co-operative - payment calculator (final design: Decimal, validated, rounded to the paisa)."""
import sys
from decimal import Decimal, ROUND_HALF_UP

# ---------------- rate card: the ONLY place a rate is written ----------------
BASE_RATE = Decimal("30.00")       # Rs/litre at 3.5 % fat and 8.5 % SNF
STD_FAT = Decimal("3.5")
STD_SNF = Decimal("8.5")
STEP = Decimal("0.1")              # one quality step = 0.1 %
FAT_STEP_VALUE = Decimal("0.40")   # Rs/litre per fat step
SNF_STEP_VALUE = Decimal("0.30")   # Rs/litre per SNF step
# ---------------- validation limits ----------------
FAT_MIN, FAT_MAX = Decimal("2.0"), Decimal("7.0")
SNF_MIN, SNF_MAX = Decimal("6.0"), Decimal("10.0")     # assumption (not given in the problem)
MAX_LITRES = Decimal("200")                            # assumption: one farmer, one shift
PAISE = Decimal("0.01")
SHIFTS = ("M", "E")


class EntryError(ValueError):
    """Raised when a clerk's entry breaks a rule."""


def is_number(text):
    """True if text is a plain decimal number such as 8.5, -3, .5 (checked with str methods)."""
    t = text.strip()
    if t.startswith("-"):
        t = t[1:]
    return t.isdigit() or (t.count(".") == 1 and t.replace(".", "", 1).isdigit())


def to_decimal(value, name):
    """Converts text/number to Decimal safely (via str, never via float arithmetic)."""
    text = str(value).strip()
    if not is_number(text):
        raise EntryError(f"{name}: {text!r} is not a valid number (digits and one '.' only)")
    return Decimal(text)


def money(x):
    """Rounds a Decimal to the paisa, halves rounded up."""
    return x.quantize(PAISE, rounding=ROUND_HALF_UP)


def parse_litres(value):
    v = to_decimal(value, "litres")
    if v <= 0:
        raise EntryError(f"litres: {v} must be greater than 0")
    if v > MAX_LITRES:
        raise EntryError(f"litres: {v} is above the limit of {MAX_LITRES}")
    if v.as_tuple().exponent < -2:
        raise EntryError("litres: at most 2 decimal places")
    return v


def parse_quality(value, name, low, high):
    v = to_decimal(value, name)
    if not low <= v <= high:
        raise EntryError(f"{name}: {v} is outside the allowed range {low} to {high}")
    if v.as_tuple().exponent < -1:
        raise EntryError(f"{name}: at most 1 decimal place")
    return v


def parse_shift(value):
    s = str(value).strip().upper()
    if s not in SHIFTS:
        raise EntryError(f"shift: {value!r} must be M or E")
    return s


def validate_entry(litres, fat, snf):
    """Returns (litres, fat, snf) as Decimals or raises EntryError."""
    return (parse_litres(litres), parse_quality(fat, "fat", FAT_MIN, FAT_MAX),
            parse_quality(snf, "snf", SNF_MIN, SNF_MAX))


def count_steps(value, standard):
    """Whole number of 0.1 % steps of value from standard (nearest step, exact in Decimal)."""
    return int(((value - standard) / STEP).to_integral_value(rounding=ROUND_HALF_UP))


def rate_per_litre(fat, snf):
    """Rate per litre in Decimal rupees, rounded to the paisa. fat and snf are Decimals."""
    return money(BASE_RATE + count_steps(fat, STD_FAT) * FAT_STEP_VALUE
                 + count_steps(snf, STD_SNF) * SNF_STEP_VALUE)


def payout(litres, fat, snf):
    """Amount payable for one entry (Decimals in, Decimal rupees out, rounded to the paisa)."""
    return money(litres * rate_per_litre(fat, snf))


def ten_day_total(entries):
    """Sum of the individually rounded payouts of (litres, fat, snf) entries (text or numbers)."""
    total = Decimal("0.00")
    for litres, fat, snf in entries:
        total += payout(*validate_entry(litres, fat, snf))
    return total


# ---------------- interactive program ----------------
def ask(prompt, parse):
    """Keeps asking until parse(text) succeeds."""
    while True:
        text = input(prompt)
        if not sys.stdin.isatty():
            print(text)                      # echo piped input so the transcript reads like a terminal
        try:
            return parse(text)
        except EntryError as err:
            print("   Error:", err)


def main():
    print("KSHEERA MILK CO-OPERATIVE - payment slip (type DONE as farmer ID to finish)")
    rows, total = [], Decimal("0.00")
    while True:
        fid = input("Farmer ID : ").strip()
        if not sys.stdin.isatty():
            print(fid)
        if fid.upper() == "DONE":
            break
        if not fid:
            print("   Error: farmer ID cannot be empty")
            continue
        shift = ask("Shift (M/E): ", parse_shift)
        litres = ask("Litres     : ", parse_litres)
        fat = ask("Fat %      : ", lambda t: parse_quality(t, "fat", FAT_MIN, FAT_MAX))
        snf = ask("SNF %      : ", lambda t: parse_quality(t, "snf", SNF_MIN, SNF_MAX))
        rate, pay = rate_per_litre(fat, snf), payout(litres, fat, snf)
        rows.append((fid, shift, litres, fat, snf, rate, pay))
        total += pay
    print(f"\n{'ID':<6}{'Shift':>6}{'Litres':>9}{'Fat':>6}{'SNF':>6}{'Rate':>8}{'Amount':>10}")
    for fid, shift, litres, fat, snf, rate, pay in rows:
        print(f"{fid:<6}{shift:>6}{litres:>9.2f}{fat:>6.1f}{snf:>6.1f}{rate:>8.2f}{pay:>10.2f}")
    print(f"{'TOTAL':<42}{total:>10.2f}")


if __name__ == "__main__":
    main()
