"""Alternative: try float(text) / except ValueError - compared with the str-method check."""
import time

def is_number(text):
    t = text.strip()
    if t.startswith("-"):
        t = t[1:]
    return t.isdigit() or (t.count(".") == 1 and t.replace(".", "", 1).isdigit())

def read_try(text):
    try:
        return float(text)
    except ValueError:
        return None

samples = ["8.5", " 8.5 ", "8,5", "eight", "-4", "", "1e3", "nan", "inf", "8_5", "٣.٥"]
print(f"{'input':<10}{'str-method check':<20}{'try/except float()':<22}")
for s in samples:
    a = is_number(s)
    b = read_try(s)
    print(f"{s!r:<10}{('accept' if a else 'reject'):<20}{('accept -> ' + repr(b)) if b is not None else 'reject':<22}")

def timeit(fn, text, n=300000):
    t0 = time.perf_counter()
    for _ in range(n):
        fn(text)
    return (time.perf_counter() - t0) / n * 1e6

print("\nmicroseconds per entry (300000 repeats)")
print(f"{'input':<10}{'str check + float':>20}{'try/except':>14}")
for s in ("8.5", "8,5", "eight"):
    t1 = timeit(lambda x: float(x) if is_number(x) else None, s)
    t2 = timeit(read_try, s)
    print(f"{s!r:<10}{t1:>20.3f}{t2:>14.3f}")
