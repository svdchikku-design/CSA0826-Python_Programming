"""Cleaning pipeline (plain Python + csv module). Rules follow the Part A design.
   1. Standardise station name, date (ISO), hour (0-23 integer).
   2. Convert every reading to a number; blank, 'NA', text or out-of-range values become None (= missing).
   3. Fahrenheit stations: convert temperature to Celsius.
   4. Remove duplicate (station, date, hour) rows, keeping the first.
   5. Forward-fill gaps of at most MAX_FILL consecutive hours within one station; longer gaps stay missing."""
import csv
from datetime import datetime

LIMITS = {"pm25": (0, 999), "pm10": (0, 1999), "no2": (0, 999), "temp": (-10, 55)}    # valid range after conversion (Celsius)
FAHRENHEIT_STATIONS = {"Manali", "Ennore"}
MAX_FILL = 3
COLUMNS = ["pm25", "pm10", "no2", "temp"]

def clean_station_name(text):
    return " ".join(text.strip().split()).title()

def clean_date(text):
    text = text.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    return None

def to_number(text):
    try:
        return float(str(text).strip())
    except ValueError:                      # '', 'NA', '--', 'err'
        return None

def clean_rows(raw_rows, stats=None, fahrenheit=FAHRENHEIT_STATIONS, max_fill=MAX_FILL, fill="ffill"):
    """raw_rows: iterable of dicts (csv.DictReader). Returns list of cleaned dicts sorted by station, date, hour.
       fill: 'ffill' (default), 'none' (leave gaps missing) ."""
    stats = stats if stats is not None else {}
    def bump(k): stats[k] = stats.get(k, 0) + 1
    seen, out = set(), []
    for r in raw_rows:
        bump("rows read")
        station = clean_station_name(r["station"])
        day = clean_date(r["date"])
        hour = to_number(r["hour"])
        if day is None or hour is None or not (0 <= hour <= 23):
            bump("rows dropped: bad date or hour"); continue
        key = (station, day, int(hour))
        if key in seen:
            bump("duplicate rows removed"); continue
        seen.add(key)
        rec = {"station": station, "date": day, "hour": int(hour)}
        for col in COLUMNS:
            v = to_number(r[col])
            if v is None:
                bump(f"{col} missing/non-numeric -> missing")
            else:
                if col == "temp" and station in fahrenheit:
                    v = round((v - 32) * 5 / 9, 1); bump("temperatures converted F -> C")
                lo, hi = LIMITS[col]
                if not (lo <= v <= hi):
                    bump(f"{col} out of range -> missing"); v = None
            rec[col] = v
        out.append(rec)
    out.sort(key=lambda x: (x["station"], x["date"], x["hour"]))
    if fill == "ffill":
        last, gap, prev_key = {}, {}, None
        for rec in out:
            st = rec["station"]
            if st != prev_key:
                last, gap, prev_key = {}, {}, st
            for col in COLUMNS:
                if rec[col] is None:
                    if col in last and gap.get(col, 0) < max_fill:
                        rec[col] = last[col]; gap[col] = gap.get(col, 0) + 1; bump(f"{col} forward-filled")
                    else:
                        bump(f"{col} left missing")
                else:
                    last[col] = rec[col]; gap[col] = 0
    return out

def clean_file(path, stats=None, **kw):
    with open(path, newline="", encoding="utf-8") as f:
        return clean_rows(csv.DictReader(f), stats, **kw)

def min_max(values):
    if not values: return []
    lo, hi = min(values), max(values)
    if hi == lo: return [0.0] * len(values)          # all equal: no spread to scale (found by my own edge-case test)
    return [round((v - lo) / (hi - lo), 3) for v in values]

def z_scores(values):
    if not values: return []
    n = len(values); mean = sum(values) / n
    sd = (sum((v - mean) ** 2 for v in values) / n) ** 0.5
    if sd == 0: return [0.0] * n
    return [round((v - mean) / sd, 3) for v in values]
