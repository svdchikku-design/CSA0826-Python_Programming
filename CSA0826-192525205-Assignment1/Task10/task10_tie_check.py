"""Which rule does float round() follow on half-paise ties? Compare with half-up and half-even (Decimal)."""
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from task10_experiments_helpers import make_text_entries
from task10_experiments_helpers import f_rate, f_pay
from calculator import validate_entry, rate_per_litre

n = 6000
text = make_text_entries(n)
ties = up_match = even_match = float_up = float_down = 0
for e in text:
    l, f, s = validate_entry(*e)
    raw = l * rate_per_litre(f, s)                       # exact unrounded Decimal payment
    if raw * 100 % 1 == Decimal("0.5"):                  # a true half-paisa tie
        ties += 1
        fp = Decimal(str(f_pay(float(e[0]), float(e[1]), float(e[2]))))
        up = raw.quantize(Decimal("0.01"), ROUND_HALF_UP)
        ev = raw.quantize(Decimal("0.01"), ROUND_HALF_EVEN)
        up_match += fp == up
        even_match += fp == ev
        float_up += fp > raw
        float_down += fp < raw
print(f"{n} entries: {ties} exact half-paisa ties")
print(f"float round() agrees with half-up  : {up_match}")
print(f"float round() agrees with half-even: {even_match}")
print(f"float rounded the tie UP {float_up} times and DOWN {float_down} times (direction depends on binary representation)")
