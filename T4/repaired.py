"""Task 4.3: repaired library program - append mode, newline per title, with statements, error log."""
import logging, sys, tempfile, os
from datetime import datetime

def setup_error_log(path="errors.log"):
    logging.basicConfig(filename=path, level=logging.ERROR, format="%(asctime)s %(message)s", force=True)

def save_returns(books, log_path="returns.log", day=None):
    with open(log_path, "a", encoding="utf-8") as log:          # a: earlier days are kept; with: always closed
        for b in books:
            log.write(f"{day or ''},{b}\n")                    # one title per line, with its day

def process(day_file, log_path="returns.log"):
    try:
        with open(day_file, encoding="utf-8") as f:
            books = [line.strip() for line in f if line.strip()]
        save_returns(books, log_path, day=os.path.splitext(os.path.basename(day_file))[0])
        return True
    except FileNotFoundError:
        logging.error("%s: file not found", day_file)
    except PermissionError:
        logging.error("%s: permission denied", day_file)
    except OSError as e:                                         # disk full, etc.: recorded with the file name
        logging.exception("%s: OS error %s", day_file, e)
    return False

if __name__ == "__main__":
    os.chdir(tempfile.mkdtemp()); setup_error_log()
    def day(name, books): open(name, "w").write("\n".join(books))
    day("mon.txt", ["Python Crash Course", "Algorithms Unlocked"]); day("tue.txt", ["Data Structures in C", "Clean Code", "SICP"]); day("wed.txt", ["Operating System Concepts"])
    results = [process(d) for d in ("mon.txt", "tue.txt", "thu_missing.txt", "wed.txt")]
    print("processed:", results)
    print("--- returns.log (all days kept, one title per line)"); print(open("returns.log").read())
    print("--- errors.log"); print(open("errors.log").read())
