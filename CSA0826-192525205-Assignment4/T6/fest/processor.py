"""The processing flow: read -> validate -> remove duplicates -> write. It never stops because of a bad line or file."""
from pathlib import Path
from .reader import read_lines
from .validate import parse_registration, InvalidRegistration
from . import writer

EXPECTED = ["CSE", "ECE", "MECH", "CIVIL", "IT"]          # the five departments

def process_file(path, master, seen_at, errors, stats):
    """Process one department file. Returns normally even if the file is missing, unreadable or has bad lines."""
    try:
        for number, line in read_lines(path):
            stats["lines read"] += 1
            if "\ufffd" in line:                             # reader replaced an undecodable byte: keep the line, warn
                stats["encoding warnings"] += 1
                errors.append(("ENCODING", Path(path).name, number, "undecodable byte replaced with U+FFFD; check the name"))
            try:
                reg, name, dept, email, events = parse_registration(line)
            except InvalidRegistration as e:
                kind = "DAMAGED" if "fields" in str(e) else "INVALID"
                stats["damaged lines" if kind == "DAMAGED" else "invalid records"] += 1
                errors.append((kind, Path(path).name, number, str(e)))
                continue
            if reg in seen_at:                               # duplicate test: a set/dict lookup, O(1) on average
                first_file, first_line = seen_at[reg]
                before = len(master[reg][3])
                master[reg][3].update(events)               # keep one entry, merge the events chosen the second time
                stats["duplicates"] += 1
                errors.append(("DUPLICATE", Path(path).name, number,
                               f"{reg} already registered at {first_file} line {first_line}; {len(master[reg][3]) - before} new event(s) merged"))
            else:
                seen_at[reg] = (Path(path).name, number)
                master[reg] = (name, dept, email, set(events))
                stats["unique students"] += 1
    except FileNotFoundError as e:
        stats["missing files"] += 1
        errors.append(("MISSING", Path(path).name, 0, "department file not found"))
    except PermissionError as e:
        stats["unreadable files"] += 1
        errors.append(("UNREADABLE", Path(path).name, 0, "permission denied"))
    except OSError as e:                                     # folder instead of file, disk error, ... (PermissionError is handled above)
        stats["unreadable files"] += 1
        errors.append(("UNREADABLE", Path(path).name, 0, f"{type(e).__name__}: {e.strerror}"))
    else:
        stats["files read"] += 1

def run(input_dir, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    master, seen_at, errors = {}, {}, []
    stats = {"files read": 0, "missing files": 0, "unreadable files": 0, "lines read": 0,
             "unique students": 0, "duplicates": 0, "invalid records": 0, "damaged lines": 0, "encoding warnings": 0}
    for dept in EXPECTED:
        process_file(Path(input_dir) / f"{dept}.txt", master, seen_at, errors, stats)
    writer.write_master(master, Path(output_dir) / "master.csv")
    counts = writer.write_event_files(master, Path(output_dir) / "events")
    writer.write_errors(errors, Path(output_dir) / "errors.log")
    writer.write_summary(stats, counts, Path(output_dir) / "summary.txt")
    return master, errors, stats, counts
