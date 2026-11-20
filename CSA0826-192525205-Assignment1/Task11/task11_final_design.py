"""Task 11 - evidence for the final design, and the alternative: rate card read from a JSON file."""
import json, os, time, tracemalloc, random
from decimal import Decimal, ROUND_HALF_UP
from calculator import validate_entry, payout, money, rate_per_litre

# ---------- final design evidence: district-union scale, streaming, running total ----------
def stream(n, seed=2026):
    rnd = random.Random(seed)
    for _ in range(n):
        k = rnd.randint(500, 6000)
        yield (f"{k // 100}.{k % 100:02d}", f"{rnd.randint(30, 50) / 10:.1f}", f"{rnd.randint(80, 90) / 10:.1f}")

print("FINAL DESIGN (calculator.py: Decimal, validated, per-payment rounding, running total)")
print(f"{'n':>8} {'total (Rs)':>18} {'time (s)':>10} {'peak memory (KB)':>18}")
for n in (300, 6000, 150000):
    tracemalloc.start(); t0 = time.perf_counter(); total = Decimal("0.00")
    for e in stream(n):
        total += payout(*validate_entry(*e))
    dt = time.perf_counter() - t0; peak = tracemalloc.get_traced_memory()[1] / 1024; tracemalloc.stop()
    print(f"{n:>8} {total:>18} {dt:>10.2f} {peak:>18.1f}")

# ---------- Alternative: rate card from JSON ----------
def load_rate_card(path):
    """Read the JSON rate card and return Decimal values."""
    with open(path) as fh:
        raw = json.load(fh)
    return {k: Decimal(v) for k, v in raw.items()}

def rate_from_card(card, fat, snf):
    steps_f = int(((fat - card["std_fat"]) / card["step"]).to_integral_value(rounding=ROUND_HALF_UP))
    steps_s = int(((snf - card["std_snf"]) / card["step"]).to_integral_value(rounding=ROUND_HALF_UP))
    return money(card["base_rate"] + steps_f * card["fat_step_value"] + steps_s * card["snf_step_value"])

card = load_rate_card("ratecard.json")
fat, snf, litres = Decimal("4.2"), Decimal("8.7"), Decimal("8.5")
print("\nJSON card rate for 4.2/8.7:", rate_from_card(card, fat, snf), "(module gives", rate_per_litre(fat, snf), ")")

# a revision = edit one text file, no change to the program
raw = json.load(open("ratecard.json")); raw["fat_step_value"] = "0.45"
json.dump(raw, open("ratecard_revised.json", "w"), indent=2)
card2 = load_rate_card("ratecard_revised.json")
print("after editing ratecard_revised.json (fat step 0.45): rate =", rate_from_card(card2, fat, snf),
      "amount =", money(litres * rate_from_card(card2, fat, snf)))

# start-up cost for t values
print(f"\n{'t values':>9} {'file size (bytes)':>18} {'load time (ms)':>15} {'memory (KB)':>12}")
for t in (6, 1000, 100000):
    data = {f"key{i}": f"{random.Random(i).randint(1, 9999) / 100:.2f}" for i in range(t)}
    path = f"synthetic_{t}.json"
    json.dump(data, open(path, "w"))
    tracemalloc.start(); t0 = time.perf_counter()
    loaded = {k: Decimal(v) for k, v in json.load(open(path)).items()}
    dt = (time.perf_counter() - t0) * 1000; mem = tracemalloc.get_traced_memory()[1] / 1024; tracemalloc.stop()
    print(f"{t:>9} {os.path.getsize(path):>18} {dt:>15.3f} {mem:>12.1f}")
    os.remove(path)
os.remove("ratecard_revised.json")

# a typo in the JSON is only found when the program starts
try:
    json.loads('{"base_rate": "30.00", "fat_step_value": 0.40,}')
except json.JSONDecodeError as e:
    print("\nmalformed JSON ->", type(e).__name__ + ":", e)
