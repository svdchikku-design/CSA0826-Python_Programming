"""Q2 changed condition: two extra attempts if the security question is answered correctly (once)."""
OTP, SECURITY_ANSWER = "483920", "chennai"

def typing(entries):
    for e in entries:
        print(f"    customer types: {e!r}")
        yield e

# while: the allowed number can simply grow, the loop condition re-reads it every time
def verify_extended_while(typed, security_ok):
    allowed, attempts, extra_offered = 3, 0, False
    while True:
        while attempts < allowed:
            entry = next(typed).strip()
            if entry == "":
                continue
            attempts += 1
            if entry == OTP:
                return "VERIFIED"
            print(f"    wrong OTP ({attempts} of {allowed} used)")
        if not extra_offered:                         # first time the attempts run out: ask the security question
            extra_offered = True
            answer = security_ok()
            if answer:
                allowed += 2
                print("    security answer correct: 2 extra attempts granted")
                continue
            print("    security answer wrong")
        return "LOCKED"

# for: range(3) is fixed when the loop starts, so the design must change (range(5) plus a hand-made check)
def verify_extended_for(typed, security_ok):
    allowed, extra_offered, result = 3, False, "LOCKED"
    for attempt in range(1, 6):                       # worst case 5 attempts
        if attempt > allowed:                         # attempts used up
            if extra_offered or not security_ok():
                break                                 # lock - but break is now used for BOTH lock and success...
            extra_offered, allowed = True, 5
            print("    security answer correct: 2 extra attempts granted")
        while True:
            entry = next(typed).strip()
            if entry:
                break
        if entry == OTP:
            result = "VERIFIED"                       # ...so a result variable is needed and for-else cannot be used
            break
        print(f"    wrong OTP ({attempt} of {allowed} used)")
    return result

cases = [
    ("A: right at once", ["483920"], True, "VERIFIED"),
    ("B: 3 wrong, security OK, 4th correct", ["1", "2", "3", "483920"], True, "VERIFIED"),
    ("C: 3 wrong, security wrong", ["1", "2", "3"], False, "LOCKED"),
    ("D: 3 wrong, security OK, 2 more wrong -> locked, no second chance", ["1", "2", "3", "4", "5"], True, "LOCKED"),
    ("E: 3 wrong, security OK, correct on 5th", ["1", "2", "3", "4", "483920"], True, "VERIFIED"),
]
for name, entries, sec, exp in cases:
    print(f"\n=== {name} ===")
    asked = []
    def sec_fn(sec=sec, asked=asked):
        asked.append(1); print("    security question asked ->", "correct" if sec else "wrong"); return sec
    print("  while version:"); r1 = verify_extended_while(typing(entries), sec_fn)
    asked.clear()
    print("  for   version:"); r2 = verify_extended_for(typing(entries), sec_fn)
    print(f"  results: while={r1}, for={r2}, expected={exp}, match={r1 == r2 == exp}")
