"""Reading: daily files -> records and damaged lines."""
from pathlib import Path

def read_month(folder):
    records, damaged = [], []
    for path in sorted(Path(folder).glob("*.txt")):
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    damaged.append((path.name, n, f"expected 3 fields, found {len(parts)}"))
                elif parts[2] not in ("P", "A"):
                    damaged.append((path.name, n, f"invalid status {parts[2]!r}"))
                else:
                    records.append(tuple(parts))
    return records, damaged

