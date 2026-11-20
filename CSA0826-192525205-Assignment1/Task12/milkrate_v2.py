"""Ksheera co-operative - version 2: seasonal rate cards, two-decimal analyser readings, ten-day bonus.
Reused unchanged from calculator.py: to_decimal, money, parse_litres, EntryError, FAT/SNF limits.
"""
from datetime import date
from decimal import Decimal
from calculator import (to_decimal, money, parse_litres, EntryError, STD_FAT, STD_SNF, STEP,
                        SNF_STEP_VALUE, FAT_MIN, FAT_MAX, SNF_MIN, SNF_MAX)

# ---------------- rate cards: a revision edits this block only ----------------
RATE_CARDS = {
    "normal": {"base": Decimal("30.00"), "fat_step": Decimal("0.40")},
    "season": {"base": Decimal("32.00"), "fat_step": Decimal("0.45")},   # April - June
}
SEASON_MONTHS = (4, 5, 6)
BONUS_THRESHOLD_LITRES = Decimal("500")      # bonus only if MORE than this in ten days
BONUS_PER_LITRE = Decimal("0.50")


def season_of(day):
    """Return 'season' for April-June, otherwise 'normal'."""
    return "season" if day.month in SEASON_MONTHS else "normal"


def parse_reading(value, name, low, high):
    """Analyser reading: Decimal within [low, high] with at most 2 decimal places."""
    v = to_decimal(value, name)
    if not low <= v <= high:
        raise EntryError(f"{name}: {v} is outside the allowed range {low} to {high}")
    if v.as_tuple().exponent < -2:
        raise EntryError(f"{name}: at most 2 decimal places")
    return v


def rate_per_litre(fat, snf, day):
    """Rate per litre for readings on a given date: proportional steps (no step rounding), rounded to the paisa."""
    card = RATE_CARDS[season_of(day)]
    fat_units = (fat - STD_FAT) / STEP           # exact in Decimal, may be fractional (e.g. 0.7)
    snf_units = (snf - STD_SNF) / STEP
    return money(card["base"] + fat_units * card["fat_step"] + snf_units * SNF_STEP_VALUE)


def payout(litres, fat, snf, day):
    """Amount for one entry, rounded to the paisa."""
    return money(litres * rate_per_litre(fat, snf, day))


def bonus(total_litres):
    """Ten-day volume bonus: Rs 0.50 per litre on ALL litres if the total is more than 500 L, else 0."""
    if total_litres > BONUS_THRESHOLD_LITRES:
        return money(total_litres * BONUS_PER_LITRE)
    return Decimal("0.00")


def ten_day_settlement(entries):
    """entries: list of (date, litres, fat, snf) as text/numbers. Returns (litres, payments, bonus, total)."""
    litres_total, payments = Decimal("0"), Decimal("0.00")
    for day, litres, fat, snf in entries:
        l = parse_litres(litres)
        f = parse_reading(fat, "fat", FAT_MIN, FAT_MAX)
        s = parse_reading(snf, "snf", SNF_MIN, SNF_MAX)
        litres_total += l
        payments += payout(l, f, s, day)
    b = bonus(litres_total)
    return litres_total, payments, b, payments + b
