import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
"""

def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative readings only."""
    rows = []
    # TODO 1: Read the text with csv.DictReader; skip rows whose pm25 is empty, 'NA' or
    # negative; convert pm25 to float
    for r in csv.DictReader(io.StringIO(text)):
        value = r["pm25"].strip()
        if value == "" or value.upper() == "NA":
            continue
        pm = float(value)
        if pm < 0:
            continue
        rows.append((r["station"], r["date"], pm))
    return rows

def min_max(values):
    # TODO 2: Scale each value to the range 0-1 using (v - min) / (max - min), rounded
    # to 3 decimals
    lo, hi = min(values), max(values)
    return [round((v - lo) / (hi - lo), 3) for v in values]

clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
