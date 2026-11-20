"""Change Decimal(amount) to Decimal(float(amount)) and see what happens."""
from decimal import Decimal
payments = ["33.40"] * 1000 + ["0.10"] * 3
exact = sum(Decimal(a) for a in payments)
via_float = sum(Decimal(float(a)) for a in payments)
print("Decimal(amount)        :", exact)
print("Decimal(float(amount)) :", via_float)
print("Decimal(float('33.40')):", Decimal(float("33.40")))
print("difference             :", via_float - exact)
print("rounded to paise       :", via_float.quantize(Decimal("0.01")))
