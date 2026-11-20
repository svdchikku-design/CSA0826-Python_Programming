"""Writing: master list, event-wise files, summary report and error log."""
from pathlib import Path

def write_master(master, path):
    with open(path, "w", encoding="utf-8") as out:
        out.write("register_no,name,department,email,events\n")
        for reg in sorted(master):
            name, dept, email, events = master[reg]
            out.write(f"{reg},{name},{dept},{email},{';'.join(sorted(events))}\n")

def write_event_files(master, folder):
    by_event = {}
    for reg, (name, dept, email, events) in master.items():
        for ev in events:
            by_event.setdefault(ev, []).append((reg, name))
    Path(folder).mkdir(parents=True, exist_ok=True)
    for ev, people in by_event.items():
        with open(Path(folder) / f"{ev.replace(' ', '_')}.txt", "w", encoding="utf-8") as out:
            for reg, name in sorted(people):
                out.write(f"{reg},{name}\n")
    return {ev: len(p) for ev, p in by_event.items()}

def write_errors(errors, path):
    with open(path, "w", encoding="utf-8") as out:
        for kind, source, number, message in errors:
            out.write(f"{kind}\t{source}\tline {number}\t{message}\n")

def write_summary(stats, event_counts, path):
    with open(path, "w", encoding="utf-8") as out:
        for key, value in stats.items():
            out.write(f"{key}: {value}\n")
        out.write("participants per event:\n")
        for ev in sorted(event_counts):
            out.write(f"  {ev}: {event_counts[ev]}\n")
