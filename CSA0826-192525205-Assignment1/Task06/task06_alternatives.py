"""Alternative: one long script (no functions) and lambda; function-call overhead for n entries."""
import random, time
BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = 30.00, 0.40, 0.30

def rate_per_litre(fat, snf):
    return round(BASE_RATE + round((fat - 3.5) / 0.1) * FAT_STEP_VALUE + round((snf - 8.5) / 0.1) * SNF_STEP_VALUE, 2)
def payout(litres, fat, snf):
    return round(litres * rate_per_litre(fat, snf), 2)
def ten_day_total(entries):
    total = 0.0
    for l, f, s in entries:
        total += payout(l, f, s)
    return round(total, 2)

rate_lambda = lambda fat, snf: round(BASE_RATE + round((fat - 3.5) / 0.1) * FAT_STEP_VALUE + round((snf - 8.5) / 0.1) * SNF_STEP_VALUE, 2)
pay_lambda = lambda l, f, s: round(l * rate_lambda(f, s), 2)

random.seed(7)
def make(n):
    return [(random.randint(50, 600) / 10, random.randint(30, 50) / 10, random.randint(80, 90) / 10) for _ in range(n)]

def one_long_script(entries):             # the same logic written inline, the rate expression repeated for every use
    total = 0.0
    for l, f, s in entries:
        total += round(l * round(BASE_RATE + round((f - 3.5) / 0.1) * FAT_STEP_VALUE + round((s - 8.5) / 0.1) * SNF_STEP_VALUE, 2), 2)
    return round(total, 2)

print(f"{'n':>8} {'functions (ms)':>15} {'inline (ms)':>12} {'lambda (ms)':>12} {'same total?':>12}  call overhead per entry (us)")
for n in (300, 6000, 150000):
    data = make(n)
    t0 = time.perf_counter(); a = ten_day_total(data); ta = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); b = one_long_script(data); tb = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); c = round(sum(pay_lambda(*e) for e in data), 2); tc = (time.perf_counter() - t0) * 1000
    print(f"{n:>8} {ta:>15.2f} {tb:>12.2f} {tc:>12.2f} {str(a == b == c):>12}  {(ta - tb) / n * 1000:>10.3f}")
print("\nrepeated copies of the rate expression: functions = 1, one long script = 1 per place it is needed (slip, report, bank file ...)")
