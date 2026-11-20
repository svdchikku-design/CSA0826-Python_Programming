"""Q3 alternative: re.fullmatch instead of slicing and string methods."""
import re, time, random, string
from q3_plate_funcs import normalise, is_valid

PATTERN = re.compile(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}")
def is_valid_regex(reg):
    return PATTERN.fullmatch(reg) is not None

battery = ["TN09AB1234", "KA01M0007", "TN9AB1234", "TN221234AB", "TN09ABC1234", "T9AB1234", "", "TN09AB123",
           "TN09AB12345", "TN０９AB１２３４", "TN09ÄB1234", "TN09AB١٢٣٤"]
print(f"{'registration':<16}{'string methods':<16}{'regex':<8}same?")
for reg in battery:
    a, b = is_valid(reg), is_valid_regex(reg)
    print(f"{reg!r:<16}{str(a):<16}{str(b):<8}{'yes' if a == b else '<-- DIFFERENT'}")

random.seed(5)
def random_plate(L):
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for _ in range(2)) + f"{random.randint(0, 99):02d}" + \
           "".join(random.choice(letters) for _ in range(L - 8)) + f"{random.randint(0, 9999):04d}"
plates = [random_plate(random.choice((9, 10))) for _ in range(20000)]
assert all(is_valid(p) == is_valid_regex(p) for p in plates)
print("\nagree on 20,000 random valid-format plates:", True)

def timeit(fn, data, reps=5):
    best = 1e9
    for _ in range(reps):
        t0 = time.perf_counter()
        for p in data:
            fn(p)
        best = min(best, time.perf_counter() - t0)
    return best / len(data) * 1e6
print(f"\nmicroseconds per validation (best of 5 over 20,000 plates):")
print(f"  slicing + isalpha/isdigit : {timeit(is_valid, plates):.3f}")
print(f"  re.fullmatch (compiled)   : {timeit(is_valid_regex, plates):.3f}")
print(f"  re.fullmatch (uncompiled) : {timeit(lambda p: re.fullmatch(r'[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}', p) is not None, plates):.3f}")
print("\nTime versus the length L of the typed text (spaces inserted so normalise() must scan all of it):")
print(f"{'L':>8} | {'normalise + validate (string methods)':>38} | {'normalise + validate (regex)':>29}")
for L in (10, 1000, 100000, 1000000):
    s = "TN" + " " * (L - 10) + "09AB1234"
    reps = max(5, 2000000 // L)
    t0 = time.perf_counter()
    for _ in range(reps): is_valid(normalise(s))
    t1 = (time.perf_counter() - t0) / reps * 1e6
    t0 = time.perf_counter()
    for _ in range(reps): is_valid_regex(normalise(s))
    t2 = (time.perf_counter() - t0) / reps * 1e6
    print(f"{L:>8} | {t1:>35.2f} us | {t2:>26.2f} us")
print("both grow linearly with L because normalise() has to read every character; the validation step itself is O(1) after the length guard")
