# CSA08-192525205-Assignment4

- **Name:** Saai Vardhan D
- **Register number:** 192525205
- **Course:** 0826 Python Programming - Assignment 4 (CO4: files, exceptions, modules and packages)
- **Python version:** 3.13
- **Libraries:** standard library only (`requirements.txt` is empty). Graphviz was used only to draw the diagram in the report.

## How to run (from the repository root)

| Task | Command | Result in one line |
|---|---|---|
| 1 | `cd T1 && python experiments.py` (also `python poor_script.py mess_oct.txt`, `python mess_repaired.py mess_oct.txt`) | Original total 3750 silently drops 1250.50 and 3 bad lines; repaired total 5200.50 with 3 rejected lines reported; line-by-line uses 0.02 MB vs 5.6 MB for read() at 50,000 lines |
| 2 | `cd T2 && python attendance_month.py data_oct_small` and `python experiments.py` | Monthly percentages, below-75% list and damaged-line log; one pass vs re-scan per student gives the same answer, 35x faster at 160 students |
| 3 | `cd T3 && python given_completed.py`, `failures.py`, `misuse.py`, `eafp_lbyl.py` | Complete-the-code output equals expected; failure table; `except Exception: pass` hides a typing error; raise/catch is 1.2x-3x slower than if-checks |
| 4 | `cd T4 && python test_evidence.py`, `python repaired.py`, `python alt_tryfinally.py` | Three defects demonstrated; repaired program keeps all days; original leaks 100 files for 100 errors, with/try-finally leak 0 |
| 5 | `cd T5 && python compare.py`; to see the change effort first run `python make_v2.py` (it copies the four organisations into `v2/` and adds the new report); each organisation: `cd <folder> && mkdir -p ../out && python <main> ../data ../out` | Four organisations give identical files; adding the new report changed 1, 2, 3 and 3 files |
| 6 | `cd T6 && python run_fest.py data_demo out_demo`, `python test_fest.py`, `python experiments.py` | Master list of 7 students, 8 log lines, never stops on bad lines or the missing IT.txt; list search 1131x slower than a set at 32,000 registrations |

Each folder has `output*.txt` with the captured output of the runs.
Timings vary between runs and machines; counts and results do not.

## Suggested commits (one per task)

```
git init && git add README.md requirements.txt && git commit -m "Add README"
git add T1 && git commit -m "Task 1: diagnose and repair mess-bill script"
git add T2 && git commit -m "Task 2: attendance file-processing design"
git add T3 && git commit -m "Task 3: exception handling"
git add T4 && git commit -m "Task 4: library log forensics"
git add T5 && git commit -m "Task 5: four code organisations"
git add T6 && git commit -m "Task 6: fest registration package"
```
