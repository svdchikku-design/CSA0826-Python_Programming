"""The hostel office's ORIGINAL script, unchanged except that the path comes from the command line so it can run here."""
import sys
f = open(sys.argv[1])
data = f.read()
total = 0
report = ""
for line in data.split("\n"):
    try:
        parts = line.split(",")
        total = total + int(parts[2])
        report = report + parts[1] + " " + parts[2] + "\n"
    except:
        pass
print(report)
print("Total", total)
