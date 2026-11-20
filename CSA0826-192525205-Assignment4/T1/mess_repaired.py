"""Task 1.2 - repaired mess-bill totaller: with statement, line-by-line, specific exceptions, rejected-line list, file name as parameter."""
import sys
from decimal import Decimal, InvalidOperation

def total_bills(filename):
    """Return (total as Decimal, list of (line number, text, reason) for rejected lines, accepted rows)."""
    total = Decimal("0")
    rejected, accepted = [], []
    with open(filename, encoding="utf-8") as f:        # closed automatically, even after an error
        for number, line in enumerate(f, start=1):      # one line in memory at a time
            line = line.strip()
            if not line:                                # blank line (e.g. last empty line) is skipped, not an error
                continue
            parts = [p.strip() for p in line.split(",")]
            try:
                reg, name, amount_text = parts          # ValueError if not exactly 3 fields
                amount = Decimal(amount_text)           # InvalidOperation if not a number
                if amount < 0:
                    raise ValueError("negative amount")
            except ValueError as e:
                reason = f"expected 3 fields, found {len(parts)}" if len(parts) != 3 else str(e)
                rejected.append((number, line, reason))
            except InvalidOperation:
                rejected.append((number, line, f"amount '{amount_text}' is not a number"))
            else:
                total += amount
                accepted.append((reg, name, amount))
    return total, rejected, accepted

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "mess_oct.txt"
    try:
        total, rejected, accepted = total_bills(path)
    except FileNotFoundError:
        print(f"File not found: {path}"); sys.exit(1)
    except PermissionError:
        print(f"No permission to read: {path}"); sys.exit(1)
    report = "\n".join(f"{name} {amount}" for _, name, amount in accepted)      # join, not repeated +
    print(report)
    print("Total", total)
    print(f"Rejected {len(rejected)} line(s):")
    for n, text, why in rejected:
        print(f"  line {n}: {text!r} -> {why}")
