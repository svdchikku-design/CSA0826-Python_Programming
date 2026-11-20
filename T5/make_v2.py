"""Applies the 'absent three consecutive days' change to each organisation (copy of v1 -> v2)."""
import shutil, os
for d in ("v2",): shutil.rmtree(d, ignore_errors=True)
os.mkdir("v2")
for org in ("a_script", "b_module", "c_modules", "d_package"):
    shutil.copytree(org, f"v2/{org}", ignore=shutil.ignore_patterns("__pycache__"))
NEWSTATS = '''
def absent_three_days(records):
    """Register numbers absent on 3 or more consecutive calendar days."""
    from datetime import date, timedelta
    days = {}
    for reg, d, status in records:
        if status == "A":
            days.setdefault(reg, set()).add(date.fromisoformat(d))
    result = []
    for reg, ds in sorted(days.items()):
        for d in ds:
            if d + timedelta(1) in ds and d + timedelta(2) in ds:
                result.append(reg)
                break
    return result
'''
NEWREPORT = '''
def write_absent3(regs, path):
    with open(path, "w", encoding="utf-8") as out:
        for reg in regs:
            out.write(reg + "\\n")
'''
def append(p, text): open(p, "a").write(text)
def callline(p, after, new):
    s = open(p).read(); s = s.replace(after, after + new); open(p, "w").write(s)
# (a) one script: insert before main
p = "v2/a_script/attendance_all.py"; s = open(p).read()
s = s.replace("\ndef main(", NEWSTATS + NEWREPORT + "\ndef main(")
s = s.replace('    write_damaged(damaged, f"{out}/damaged.log")\n', '    write_damaged(damaged, f"{out}/damaged.log")\n    write_absent3(absent_three_days(records), f"{out}/absent3.txt")\n')
open(p, "w").write(s)
# (b)
append("v2/b_module/attendance_lib.py", NEWSTATS + NEWREPORT)
callline("v2/b_module/main_b.py", '    lib.write_damaged(damaged, f"{out}/damaged.log")\n', '    lib.write_absent3(lib.absent_three_days(records), f"{out}/absent3.txt")\n')
# (c)
append("v2/c_modules/stats.py", NEWSTATS); append("v2/c_modules/report.py", NEWREPORT)
callline("v2/c_modules/main_c.py", '    report.write_damaged(damaged, f"{out}/damaged.log")\n', '    report.write_absent3(stats.absent_three_days(records), f"{out}/absent3.txt")\n')
# (d)
append("v2/d_package/attendance/stats.py", NEWSTATS); append("v2/d_package/attendance/report.py", NEWREPORT)
callline("v2/d_package/main_d.py", '    report.write_damaged(damaged, f"{out}/damaged.log")\n', '    report.write_absent3(stats.absent_three_days(records), f"{out}/absent3.txt")\n')
