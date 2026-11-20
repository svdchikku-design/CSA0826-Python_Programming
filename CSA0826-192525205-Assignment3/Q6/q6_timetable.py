"""Q6 - railway timetable: dictionary of dictionaries holding a list of tuples and a set."""
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
ALL = set(DAYS)

timetable = {
    12621: {"name": "Tamil Nadu Express",
            "stops": [("Chennai Central", "-", "22:00"), ("Gudur", "23:18", "23:20"), ("Vijayawada", "02:45", "02:50"), ("Nagpur", "12:00", "12:10"), ("New Delhi", "07:05", "-")],
            "days": ALL},
    12433: {"name": "Chennai Rajdhani",
            "stops": [("Chennai Central", "-", "06:10"), ("Gudur", "07:45", "07:47"), ("Vijayawada", "10:40", "10:45"), ("Nizamuddin", "05:50", "-")],
            "days": {"Mon", "Wed", "Fri"}},
    12007: {"name": "Shatabdi Express",
            "stops": [("Chennai Central", "-", "06:00"), ("Katpadi", "07:43", "07:45"), ("Bengaluru", "11:30", "-")],
            "days": ALL - {"Wed"}},
    12695: {"name": "Trivandrum Express",
            "stops": [("Chennai Central", "-", "19:10"), ("Katpadi", "21:03", "21:05"), ("Coimbatore", "02:30", "02:35"), ("Thiruvananthapuram", "11:45", "-")],
            "days": {"Tue", "Thu", "Sat", "Sun"}},
    12163: {"name": "Dadar Express",
            "stops": [("Chennai Egmore", "-", "20:10"), ("Katpadi", "22:03", "22:05"), ("Pune", "13:00", "13:10"), ("Dadar", "17:20", "-")],
            "days": {"Mon", "Tue", "Fri", "Sat"}},
    12609: {"name": "Mysuru Express",
            "stops": [("Chennai Central", "-", "13:30"), ("Katpadi", "15:13", "15:15"), ("Bengaluru", "18:50", "18:55"), ("Mysuru", "21:20", "-")],
            "days": ALL},
}

def trains_at(timetable, station, day):
    """List of (departure time, train number) for trains stopping at station on day; no index: scans everything."""
    found = []
    for number, info in timetable.items():
        if day not in info["days"]:
            continue
        for st, arr, dep in info["stops"]:              # tuple unpacking in the loop
            if st == station:
                found.append((dep if dep != "-" else arr, number)); break
    return found

def sorted_by_departure(timetable, station, day):
    """Trains sorted by their time at the station using sorted(key=lambda ...)."""
    return sorted(trains_at(timetable, station, day), key=lambda pair: pair[0])

def print_timetable(timetable):
    for number, info in sorted(timetable.items()):
        print(f"{number}  {info['name']:<20} runs: {','.join(d for d in DAYS if d in info['days'])}")
        print(f"        {'Station':<22}{'Arr':>7}{'Dep':>7}")
        for st, arr, dep in info["stops"]:
            print(f"        {st:<22}{arr:>7}{dep:>7}")

if __name__ == "__main__":
    print_timetable(timetable)
    print("\nDeparture time of the third station of train 12621:  timetable[12621]['stops'][2][2] =", timetable[12621]["stops"][2][2],
          "| its name:", timetable[12621]["stops"][2][0])
    print("Days of train 12433:", sorted(timetable[12433]["days"]), "| does 12433 run on Tue?", "Tue" in timetable[12433]["days"])

    print("\nQuery: trains stopping at Katpadi on Tuesday, sorted by time (time, number):")
    q = sorted_by_departure(timetable, "Katpadi", "Tue")
    print("  ", q, "->", [(t, timetable[n]["name"]) for t, n in q])
    print("Query: Chennai Central on Wednesday:", sorted_by_departure(timetable, "Chennai Central", "Wed"), "(12007 Shatabdi does not run on Wednesday, so it is absent)")
    print("Query: unknown station 'Atlantis' on Mon:", sorted_by_departure(timetable, "Atlantis", "Mon"))
    print("Query: Chennai Egmore on Wed (12163 does not run on Wed):", sorted_by_departure(timetable, "Chennai Egmore", "Wed"))
    print("Query: Chennai Egmore on Mon:", sorted_by_departure(timetable, "Chennai Egmore", "Mon"))
