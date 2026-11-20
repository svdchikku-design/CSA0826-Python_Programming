# CSA08 - Python Programming - Assignment 1 (CO1)
Milk co-operative payment calculator

- Name: Saai Vardhan D
- Register number: 192525205
- Repository name: CSA08-192525205-Assignment1
- Python version: 3.13 (write your own version if different)
- Libraries: standard library only (decimal, json, time, tracemalloc, random, sys, math). requirements.txt is empty.

## Run each program (from inside its folder)
| Task | Command | Result in one line |
|---|---|---|
| 1 | python task01_data_model.py | Values/types table; variable-per-farmer design needs 1201 lines for 300 farmers vs 7 |
| 2 | python task02_session.py ; python task02_complete.py ; python task02_float_decimal.py ; python task02_alternatives.py | float 33400.30000000061 vs Decimal 33400.30 |
| 3 | python task03_constants.py | One constants block; magic numbers cause partial revisions |
| 4 | python task04_expressions.py | Surprises: 7.000000000000002, int() steps wrong, -2**2 = -4 |
| 5 | python task05_input.py < input_session.txt ; python task05_tryexcept.py | Invalid input refused with messages |
| 6 | python task06_functions.py ; python task06_alternatives.py | Functions add ~0.05 us per entry |
| 7 | python milkrate.py ; python use_milkrate.py ; python use_noguard.py | __name__ guard demonstrated |
| 8 | python task08_algorithm.py | Hand trace total 917.50; running total uses 0.9 KB vs 63 MB |
| 9 | python calculator.py < input_session.txt ; python test_calculator.py | 21 of 21 tests pass; 5-entry hand total 1464.75 |
| 10 | python task10_experiments.py ; python task10_tie_check.py | float short by Rs 74.93 at 150,000 payments |
| 11 | python task11_final_design.py | Decimal + per-payment rounding recommended; JSON card alternative |
| 12 | python test_v2.py ; python evaluate_old_design.py | 27 of 27 tests pass; design MODIFIED |

## Commit progressively (one commit per task)
git init; git add Task01; git commit -m "Task 1: problem analysis" ... repeat for Task02 ... Task12, then README.md; git remote add origin <your link>; git push -u origin main
