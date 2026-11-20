"""Statistics: counts and percentages."""

def percentage(present, absent):
    total = present + absent
    return 100.0 * present / total if total else 0.0

def attendance_table(records):
    counts = {}
    for reg, date, status in records:
        c = counts.setdefault(reg, [0, 0])
        c[0 if status == "P" else 1] += 1
    return {reg: (p, a, percentage(p, a)) for reg, (p, a) in sorted(counts.items())}

def below_threshold(table, limit=75.0):
    return [(reg, row[2]) for reg, row in table.items() if row[2] < limit]

