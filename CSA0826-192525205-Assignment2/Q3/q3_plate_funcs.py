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

