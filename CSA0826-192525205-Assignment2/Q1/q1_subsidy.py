"""Q1 - electricity subsidy: predictions first, then separate ifs vs if-elif-else."""
FULL, PARTIAL, SENIOR, NONE = "FULL", "PARTIAL", "SENIOR", "NONE"

# ---------- PREDICTIONS (written BEFORE running any implementation) ----------
# (units, has ration card, has member above 80) -> predicted decision according to the rule
households = [
    (50,  True,  False),   # H1  <=100: full subsidy; the card must not give a second one
    (100, False, False),   # H2  boundary 100: full
    (100, True,  False),   # H3  boundary 100 with card: still only FULL
    (101, True,  False),   # H4  boundary 101 with card: partial
    (101, False, False),   # H5  boundary 101 without card: none
    (200, True,  True),    # H6  boundary 200 with card: partial (age does not matter here)
    (201, False, True),    # H7  boundary 201 with member above 80: senior subsidy
    (201, True,  False),   # H8  boundary 201, card does not help above 200: none
]
predicted = [FULL, FULL, FULL, PARTIAL, NONE, PARTIAL, SENIOR, NONE]

# ---------- Implementation A: the developer's separate if statements (a list collects every result) ----------
def decide_separate_buggy(units, card, senior):
    results = []
    if units <= 100:
        results.append(FULL)
    if units <= 200 and card:            # BUG: no lower bound, so units <= 100 with a card also matches
        results.append(PARTIAL)
    if units > 200 and senior:
        results.append(SENIOR)
    return results or [NONE]

# ---------- Implementation B: separate ifs, repaired with chained comparisons (mutually exclusive) ----------
def decide_separate_chained(units, card, senior):
    results = []
    if units <= 100:
        results.append(FULL)
    if 101 <= units <= 200 and card:
        results.append(PARTIAL)
    if units > 200 and senior:
        results.append(SENIOR)
    return results or [NONE]

# ---------- Implementation C: if-elif-else (exactly one branch can run) ----------
def decide_elif(units, card, senior):
    if units <= 100:
        return FULL
    elif 101 <= units <= 200:
        return PARTIAL if card else NONE
    elif senior:                         # units > 200
        return SENIOR
    else:
        return NONE

# ---------- Design decision: nested if vs combined Boolean conditions ----------
def decide_nested(units, card, senior):
    if units <= 100:
        return FULL
    else:
        if units <= 200:
            if card:
                return PARTIAL
            else:
                return NONE
        else:
            if senior:
                return SENIOR
            else:
                return NONE

def decide_combined(units, card, senior):
    if units <= 100:
        return FULL
    if 101 <= units <= 200 and card:
        return PARTIAL
    if units > 200 and senior:
        return SENIOR
    return NONE

print(f"{'H':<3}{'units':>6} {'card':>6} {'80+':>6} | {'predicted':<9} | {'separate (bug)':<16} {'separate chained':<17} {'if-elif-else':<13} {'nested':<8} {'combined':<9} | ok?")
all_ok = True
for i, ((u, c, s), p) in enumerate(zip(households, predicted), 1):
    a, b, e = decide_separate_buggy(u, c, s), decide_separate_chained(u, c, s), decide_elif(u, c, s)
    n, m = decide_nested(u, c, s), decide_combined(u, c, s)
    ok = (e == p) and (b == [p]) and (n == p) and (m == p)
    all_ok &= ok
    print(f"H{i:<2}{u:>6} {str(c):>6} {str(s):>6} | {p:<9} | {'+'.join(a):<16} {'+'.join(b):<17} {e:<13} {n:<8} {m:<9} | {'yes' if ok else 'NO'}")
print("\nall predictions confirmed by if-elif-else, chained separate ifs, nested and combined:", all_ok)
print("households receiving MORE THAN ONE decision from the buggy separate ifs:",
      [f"H{i}" for i, h in enumerate(households, 1) if len(decide_separate_buggy(*h)) > 1])

# ---------- every boundary, exhaustively (all card/senior combinations) ----------
print("\nBoundary table (units x card x senior), if-elif-else result:")
print(f"{'units':>6} | card=F,sen=F  card=F,sen=T  card=T,sen=F  card=T,sen=T")
for units in (0, 1, 99, 100, 101, 150, 200, 201, 500):
    print(f"{units:>6} | " + "  ".join(f"{decide_elif(units, c, s):<12}" for c in (False, True) for s in (False, True)))
# the two designs must agree everywhere
assert all(decide_nested(u, c, s) == decide_combined(u, c, s) == decide_elif(u, c, s) for u in range(0, 400) for c in (False, True) for s in (False, True))
print("\nnested, combined and if-elif-else agree on all 1600 test cases (units 0-399 x 4 flag combinations)")
