"""B2: a station name containing a quote - SQL built with + (or an f-string) versus a ? placeholder."""
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
con.execute("CREATE TABLE secret (note TEXT)"); con.execute("INSERT INTO secret VALUES ('board password: s3cr3t')")
con.executemany("INSERT INTO aq VALUES (?, ?, ?)", [("Adyar", "2026-10-01", 48.0), ("Guindy", "2026-10-01", 95.0), ("Guindy", "2026-10-03", 121.0),
                                                    ("Adyar", "2026-10-04", 60.0), ("St. Mary's Church", "2026-10-01", 70.0)])
def concat_avg(name):
    return con.execute("SELECT AVG(pm25) FROM aq WHERE station = '" + name + "'").fetchone()[0]
def fstring_avg(name):
    return con.execute(f"SELECT AVG(pm25) FROM aq WHERE station = '{name}'").fetchone()[0]
def param_avg(name):
    return con.execute("SELECT AVG(pm25) FROM aq WHERE station = ?", (name,)).fetchone()[0]

def attempt(fn, name):
    try: return fn(name)
    except Exception as e: return f"{type(e).__name__}: {e}"

print("A. an honest station name with an apostrophe: St. Mary's Church (true value 70.0)")
print("   built with +        :", attempt(concat_avg, "St. Mary's Church"))
print("   built with f-string :", attempt(fstring_avg, "St. Mary's Church"))
print("   ? placeholder       :", attempt(param_avg, "St. Mary's Church"))
print("\nB. the injection text  Adyar' OR '1'='1   (true average of all five rows would be 78.8; Adyar alone is 54.0)")
inj = "Adyar' OR '1'='1"
print("   statement the + version really sends :  SELECT AVG(pm25) FROM aq WHERE station = '" + inj + "'")
print("   built with +        :", attempt(concat_avg, inj), "  <- the condition '1'='1' is always true: every row is averaged")
print("   ? placeholder       :", attempt(param_avg, inj), "  <- looks for a station whose NAME is that whole text: none exists")
print("\nC. a worse input: read another table with UNION")
union = "x' UNION SELECT note FROM secret --"
print("   statement sent      :  SELECT station FROM aq WHERE station = '" + union + "'")
rows = con.execute("SELECT station FROM aq WHERE station = '" + union.replace("--", "--") + "'").fetchall()
print("   a query returning names (SELECT station ... WHERE station = '<input>') leaks:", rows)
print("   same input with ? placeholder:", con.execute("SELECT station FROM aq WHERE station = ?", (union,)).fetchall())
print("\nD. can execute() run a second statement (DROP TABLE)?")
try: con.execute("SELECT AVG(pm25) FROM aq WHERE station = 'x'; DROP TABLE aq --")
except Exception as e: print("   sqlite3.execute refuses multiple statements:", type(e).__name__, "-", e, "| table aq still exists:", bool(con.execute("SELECT name FROM sqlite_master WHERE name='aq'").fetchall()))
print("   (executescript() would run them - it must never receive user text; other database drivers may allow stacked statements)")
