# CSA08 - Python Programming - Assignment 2 (CO2)
Control flow, strings, functions, recursion

- Name: Saai Vardhan D
- Register number: 192525205
- Repository name: CSA08-192525205-Assignment2
- Python version: 3.13 (write your own version if different; match-case needs 3.10+)
- Libraries: standard library only (io, re, time, tracemalloc, functools, decimal, bisect, collections). requirements.txt is empty.

## Run each program (from inside its folder)
| Q | Command | Result in one line |
|---|---|---|
| 1 | python q1_subsidy.py ; python q1_alternatives.py | Buggy separate ifs give two subsidies to H1 and H3; if-elif-else gives one |
| 2 | python q2_otp.py ; python q2_changed_condition.py ; python q2_recursive.py | while/for versions agree; recursion fails at 10,000 attempts |
| 3 | python q3_plate.py ; python q3_inquiry.py ; python q3_regex.py | 6 of 6 predictions correct; isalpha/isdigit accept Unicode, regex does not |
| 4 | python q4_given.py ; python q4_measure.py ; python q4_alternatives.py | join 3x faster than += at 200,000 lines; += on an attribute is quadratic |
| 5 | python q5_orders.py ; python q5_design.py ; python q5_alternatives.py | Default list is shared; None default gives independent orders |
| 6 | python q6_given.py ; python q6_analysis.py ; python q6_limit.py | naive 242,785 calls vs memo 26 at n=25; memo(1000) hits the recursion limit when cold |
| 7 | python q7_diagnose.py ; python q7_redesign.py ; python q7_extension.py | Bottom-up loop: 29 additions instead of 2,692,537 calls at n=30 |

## Commit progressively (one commit per question)
git init; git add Q1; git commit -m "Q1: subsidy rules" ... repeat for Q2 ... Q7, then README.md; git remote add origin <your link>; git push -u origin main
