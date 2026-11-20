"""Synthetic raw data for the 12-station air-quality network (fixed random seed -> the same files every run).
The data are generated, not real measurements; the faults are injected on purpose so the cleaning rules can be tested."""
import csv, math, random
from datetime import date, timedelta

STATIONS = ["Adyar", "Guindy", "Velachery", "Manali", "T. Nagar", "Anna Nagar",
            "Alandur", "Perungudi", "Kodungaiyur", "Royapuram", "Ennore", "Tondiarpet"]
BASE_PM25 = [38, 52, 41, 88, 47, 44, 55, 49, 83, 72, 95, 68]        # typical level of each station
FAHRENHEIT_STATIONS = {"Manali", "Ennore"}                           # these two report temperature in Fahrenheit
HEADER = ["station", "date", "hour", "pm25", "pm10", "no2", "temp"]

def true_reading(rnd, base, d, hour):
    """A fault-free reading: daily rush-hour peaks, mild monthly trend, noise; temperature has a day/night cycle."""
    diurnal = 1 + 0.35 * math.exp(-((hour - 9) ** 2) / 8) + 0.45 * math.exp(-((hour - 21) ** 2) / 10) - 0.15 * math.exp(-((hour - 15) ** 2) / 12)
    trend = 1 + 0.004 * (d.day - 15)
    pm25 = max(3.0, base * diurnal * trend + rnd.gauss(0, 5))
    pm10 = pm25 * rnd.uniform(1.4, 1.9)
    no2 = 18 + 0.35 * pm25 + rnd.gauss(0, 4)
    temp_c = 29 + 4 * math.sin((hour - 9) / 24 * 2 * math.pi) - 0.01 * (pm25 - base) + rnd.gauss(0, 0.6)
    return round(pm25, 1), round(pm10, 1), round(no2, 1), round(temp_c, 1)

def make_station_rows(station, base, year=2026, month=10, days=31, seed=0, faults=True):
    """Return list of raw CSV rows (all strings) for one station-month, with injected faults if faults=True."""
    rnd = random.Random(seed)
    rows = []
    d0 = date(year, month, 1)
    for k in range(days):
        d = d0 + timedelta(days=k)
        for hour in range(24):
            pm25, pm10, no2, temp_c = true_reading(rnd, base, d, hour)
            temp = round(temp_c * 9 / 5 + 32, 1) if station in FAHRENHEIT_STATIONS else temp_c
            row = [station, d.isoformat(), f"{hour:02d}", pm25, pm10, no2, temp]
            if faults:
                r = rnd.random()
                col = rnd.choice([3, 4, 5, 6])
                if r < 0.030:   row[col] = rnd.choice(["", "NA", "NA", " "])             # missing
                elif r < 0.040: row[3] = rnd.choice([-5.0, -99.0, -1.0])                   # negative sensor fault
                elif r < 0.046: row[3] = rnd.choice([9999, 1500.0, 32767])                 # impossibly large
                elif r < 0.050: row[col] = rnd.choice(["--", "err", "n/a?"])               # non-numeric junk
                elif r < 0.060: row[1] = d.strftime("%d/%m/%Y")                            # different date format
                elif r < 0.066: row[0] = rnd.choice([station.upper(), station.lower() + " ", " " + station])   # station name spelling
            rows.append(row)
            if faults and rnd.random() < 0.012:
                rows.append(list(row))                                                      # exact duplicate row (resent)
    return rows

def write_network(folder, seed=42):
    import os
    os.makedirs(folder, exist_ok=True)
    total = 0
    for i, (name, base) in enumerate(zip(STATIONS, BASE_PM25)):
        rows = make_station_rows(name, base, seed=seed + i)
        with open(os.path.join(folder, f"station_{i+1:02d}_{name.replace(' ', '_').replace('.', '')}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(HEADER); w.writerows(rows)
        total += len(rows)
    return total

if __name__ == "__main__":
    n = write_network("raw_data")
    print(f"wrote 12 station files, {n} data lines, into raw_data/")
