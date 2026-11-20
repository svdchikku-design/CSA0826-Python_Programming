"""Task 10 - float vs Decimal totals, timings, rounding policy, and the rate table (dictionary)."""
import random, time
from decimal import Decimal
from calculator import rate_per_litre, payout, validate_entry, money

# ---------- naive float pipeline (what the volunteer's program does) ----------
def f_rate(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)

def f_pay(litres, fat, snf):
    return round(litres * f_rate(fat, snf), 2)

def make_text_entries(n, seed=2026):
    """n entries as clerk text: litres with 2 decimals, fat 3.0-5.0, snf 8.0-9.0 (1 decimal)."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        k = rnd.randint(500, 6000)
        out.append((f"{k // 100}.{k % 100:02d}", f"{rnd.randint(30, 50) / 10:.1f}", f"{rnd.randint(80, 90) / 10:.1f}"))
    return out

