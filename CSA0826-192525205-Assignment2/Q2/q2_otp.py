"""Q2 - OTP verification with three attempts: while, for/range(3), loop-else, break, continue, pass."""
OTP = "483920"

def typing(entries):
    """Simulates the customer typing; echoes each entry like a terminal."""
    for e in entries:
        print(f"    customer types: {e!r}")
        yield e

# ------------------------------------------------------------------ design 1: while
def verify_while(typed, correct=OTP):
    attempts = 0
    while attempts < 3:
        entry = next(typed).strip()
        if entry == "":
            print("    blank entry - ignored, attempt NOT counted")
            continue                                  # continue: back to the test, skipping the counting code
        if entry.upper() == "RESEND":
            pass                                      # pass: placeholder for a future 'resend OTP' feature; falls through
        attempts += 1                                 # the counter changes only for a real (non-blank) entry
        if entry == correct:
            print(f"    OTP correct on attempt {attempts}")
            break                                     # break: leave the loop early; the else clause is skipped
        print(f"    wrong OTP ({attempts} of 3 used)")
    else:                                             # runs only if the loop ended WITHOUT break
        print("    3 wrong attempts: account LOCKED for 30 minutes")
        return "LOCKED"
    return "VERIFIED"

# ------------------------------------------------------------------ design 2: for with range(3)
def verify_for(typed, correct=OTP):
    for attempt in range(1, 4):
        while True:                                   # a blank entry must not use up one of the three iterations
            entry = next(typed).strip()
            if entry:
                break
            print("    blank entry - ignored, attempt NOT counted")
        if entry == correct:
            print(f"    OTP correct on attempt {attempt}")
            break
        print(f"    wrong OTP ({attempt} of 3 used)")
    else:
        print("    3 wrong attempts: account LOCKED for 30 minutes")
        return "LOCKED"
    return "VERIFIED"

scenarios = {
    "S1 correct at once": ["483920"],
    "S2 wrong, then correct": ["111111", "483920"],
    "S3 blanks do not count": ["", "", "483920"],
    "S4 three wrong -> lock": ["1", "2", "3"],
    "S5 blank, 2 wrong, blank, 1 wrong -> lock": ["", "1", "", "2", "3"],
}
expected = {"S1 correct at once": "VERIFIED", "S2 wrong, then correct": "VERIFIED", "S3 blanks do not count": "VERIFIED",
            "S4 three wrong -> lock": "LOCKED", "S5 blank, 2 wrong, blank, 1 wrong -> lock": "LOCKED"}
for name, entries in scenarios.items():
    print(f"\n=== {name} ===")
    print("  while version:"); r1 = verify_while(typing(entries))
    print("  for   version:"); r2 = verify_for(typing(entries))
    print(f"  results: while={r1}, for={r2}, expected={expected[name]}, match={r1 == r2 == expected[name]}")

# ------------------------------------------------------------------ the counter in the wrong place
print("\n=== BUG 1: counter updated BEFORE the blank test ===")
def verify_bug_early_counter(typed, correct=OTP):
    attempts = 0
    while attempts < 3:
        attempts += 1                                 # wrong place: a blank entry now uses an attempt
        entry = next(typed).strip()
        if entry == "":
            continue
        if entry == correct:
            return "VERIFIED"
    return "LOCKED"
print("  customer enters: blank, blank, '1', '483920' (only ONE wrong try)")
print("  buggy result:", verify_bug_early_counter(iter(["", "", "1", "483920"])), "  (correct design gives VERIFIED:",
      verify_while(iter(["", "", "1", "483920"])), ")")

print("\n=== BUG 2: counter at the END of the loop body, but 'continue' skips it ===")
def verify_bug_late_counter(typed, correct=OTP, safety=8):
    attempts, loops = 0, 0
    while attempts < 3 and loops < safety:            # 'loops' is only a safety net so the demo stops
        loops += 1
        entry = next(typed).strip()
        if entry != correct:
            continue                                  # skips the increment below: attempts never grows
        attempts += 1
    return f"attempts={attempts}, loop ran {loops} times (would never lock: infinite loop without the safety net)"
print(" ", verify_bug_late_counter(iter(["1", "2", "3", "4", "5", "6", "7", "8", "9"])))
