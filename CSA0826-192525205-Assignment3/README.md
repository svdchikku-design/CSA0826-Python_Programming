# CSA08-192525205-Assignment3

- **Name:** Saai Vardhan D
- **Register number:** 192525205
- **Course:** CSA08 Python Programming - Assignment 3 (CO3: lists, tuples, dictionaries, sets, comprehensions)
- **Python version:** 3.13
- **Libraries:** Python standard library only (`requirements.txt` is empty). Charts/diagrams were drawn with matplotlib and Graphviz (needed only to redraw the .png files; no program depends on them for its results).

## How to run (from the repository root)

| Task | Command | Result in one line |
|---|---|---|
| Q1 | `python Q1/q1_rainfall.py` and `python Q1/q1_experiments.py` | Slicing, weekly totals, 7-day average; naive 6(n-6) additions vs running sum n-1 counted exactly (2154 vs 364 at n=365) |
| Q2 | `python Q2/q2_given.py`, `q2_experiments.py`, `q2_alternative.py` | TODO 1 done, output equals expected; `[[0]*c]*r` shares one row; list as dict key -> TypeError |
| Q3 | `python Q3/q3_given.py`, `q3_helpline.py`, `q3_experiments.py` | TODO 1-2 done, output equals expected; list.count about 14x slower than dict at 100,000 complaints |
| Q4 | `python Q4/q4_given.py`, `q4_tests.py`, `q4_venn.py`, `q4_experiments.py` | TODO 1 done with operators and methods, same result; set `&` beats nested loops by orders of magnitude |
| Q5 | `python Q5/q5_sensors.py`, `q5_experiments.py` | Loop, comprehension, map/filter identical; speeds within about 10 %, generator uses 0.4 KB instead of 8 MB |
| Q6 | `python Q6/q6_timetable.py`, `q6_experiments.py` | Nested timetable; station index is 51-81x faster per query at the cost of about 30 % extra memory |
| Q7 | `python Q7/q7_contacts.py`, `q7_experiments.py` | Dictionary + union-find merges 100,000 contacts in about 2.7 s with correct groups; pairwise would take about 6 minutes |

Each folder has `output*.txt` (captured output of the run) and, where relevant, `.png` charts/diagrams.
Timings vary from machine to machine and run to run; counts and results do not.

## Suggested commits (one per task)

```
git init && git add README.md && git commit -m "Add README"
git add Q1 && git commit -m "Q1: lists and slicing - rainfall"
git add Q2 && git commit -m "Q2: tuples, mutability and copying"
git add Q3 && git commit -m "Q3: dictionaries - helpline complaints"
git add Q4 && git commit -m "Q4: sets - elective clashes"
git add Q5 && git commit -m "Q5: list comprehension - sensor cleaning"
git add Q6 && git commit -m "Q6: nested data - railway timetable"
git add Q7 && git commit -m "Q7: contact merging design"
```
