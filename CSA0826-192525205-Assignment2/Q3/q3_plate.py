"""Q3 - vehicle registration numbers using only string operations (no regular expressions)."""

def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    # TODO 1 (completed): remove spaces and hyphens, convert to upper case
    return text.replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    # TODO 2 (completed): length 9 or 10, then check every part with slicing, isalpha() and isdigit()
    if len(reg) not in (9, 10):
        return False
    return (reg[:2].isalpha() and reg[2:4].isdigit()
            and reg[4:-4].isalpha() and reg[-4:].isdigit())

def format_receipt(reg):
    """'TN09AB1234' -> 'TN 09 AB 1234' (the number must already be normalised and valid)."""
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])

for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
    reg = normalise(raw)
    print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

# ---------------- my six predictions (written before running) and the observed results ----------------
print("\nPredictions versus observed:")
tests = [   # raw input, predicted normalised form, predicted validity
    ("tn 09 ab 1234", "TN09AB1234", True),
    ("TN-09-AB-1234", "TN09AB1234", True),
    ("Tn09Ab1234",    "TN09AB1234", True),
    ("  ka-01-m-0007 ", "KA01M0007", True),
    ("TN09ABC1234",   "TN09ABC1234", False),    # three series letters
    ("T9AB1234",      "T9AB1234",   False),     # one state letter, 8 characters
]
ok_all = True
print(f"{'input':<18}{'predicted':<14}{'observed':<14}{'valid? pred/obs':<17}{'receipt format':<16}ok")
for raw, p_norm, p_valid in tests:
    reg = normalise(raw.strip())
    v = is_valid(reg)
    ok = reg == p_norm and v == p_valid
    ok_all &= ok
    print(f"{raw!r:<18}{p_norm:<14}{reg:<14}{str(p_valid) + '/' + str(v):<17}{(format_receipt(reg) if v else '-'):<16}{'yes' if ok else 'NO'}")
print("all six predictions correct:", ok_all)
