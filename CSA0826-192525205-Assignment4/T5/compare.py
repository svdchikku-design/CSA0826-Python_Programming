"""Task 5.3 and alternative: import forms, naming conflicts, one-time import cost, memory, where to find a function."""
import subprocess, sys, os, time, textwrap, tempfile, shutil

PKG = "d_package"
print("=== 1. The three import forms (package attendance/) ===")
code = textwrap.dedent('''
    import sys
    import attendance.stats
    print("import attendance.stats       -> name bound: 'attendance' ->", "attendance" in dir(), "| 'stats' bound directly:", "stats" in dir(), "| call: attendance.stats.percentage(3,1) =", attendance.stats.percentage(3, 1))
    del attendance
    from attendance import stats
    print("from attendance import stats  -> name bound: 'stats'      ->", "stats" in dir(), "| call: stats.percentage(3,1) =", stats.percentage(3, 1))
    del stats
    from attendance.stats import percentage
    print("from attendance.stats import percentage -> bound: 'percentage' ->", "percentage" in dir(), "| call: percentage(3,1) =", percentage(3, 1))
    print("in every case the module is loaded ONCE:", [m for m in sys.modules if m.startswith("attendance")])
''')
print(subprocess.run([sys.executable, "-c", code], cwd=PKG, capture_output=True, text=True).stdout)

print("=== 2. Naming conflict: two different modules called 'stats' ===")
tmp = tempfile.mkdtemp()
os.makedirs(f"{tmp}/other"); open(f"{tmp}/other/stats.py", "w").write("def percentage(p, a):\n    return 'OTHER stats: ' + str(p + a)\n")
open(f"{tmp}/other/__init__.py", "w").close()
code = textwrap.dedent(f'''
    import sys
    sys.path.insert(0, "{tmp}/other"); sys.path.append("{os.path.abspath("c_modules")}")
    import stats                                    # plain module name: the FIRST folder on sys.path wins
    print("plain 'import stats' picks:", stats.percentage(3, 1), " <- ours (c_modules/stats.py) is hidden")
    sys.path.insert(0, "{os.path.abspath(PKG)}"); sys.path.insert(0, "{tmp}")
    import attendance.stats as ours, other.stats as theirs
    print("with packages both coexist:  attendance.stats ->", ours.percentage(3, 1), "| other.stats ->", theirs.percentage(3, 1))
''')
print(subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout)
shutil.rmtree(tmp)

print("=== 3. One-time import cost of the package, memory, and caching in sys.modules ===")
code = textwrap.dedent('''
    import time, tracemalloc, sys
    tracemalloc.start(); t0 = time.perf_counter()
    import attendance.reader, attendance.stats, attendance.report
    first = time.perf_counter() - t0; mem = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    t0 = time.perf_counter()
    for _ in range(1000):
        import attendance.reader, attendance.stats, attendance.report
    again = (time.perf_counter() - t0) / 1000
    print(f"first import of 3 modules + package: {first*1e3:.2f} ms, memory kept {mem/1024:.1f} KB")
    print(f"repeated 'import' statement (found in sys.modules): {again*1e6:.2f} us each")
    print("modules cached:", sorted(m for m in sys.modules if m.startswith("attendance")))
''')
for i in range(3):
    print(f"run {i+1}:", subprocess.run([sys.executable, "-B", "-c", code], cwd=PKG, capture_output=True, text=True).stdout.strip().replace("\n", "\n       "))
print("\n(-B: no .pyc cache, so the figures include compiling the source - the worst case; later runs with .pyc are faster)")
# whole-program startup: script vs package, no .pyc
def startup(cmd, cwd):
    best = 9
    for _ in range(5):
        t0 = time.perf_counter(); subprocess.run(cmd, cwd=cwd, capture_output=True); best = min(best, time.perf_counter() - t0)
    return best
print("\n=== 4. Whole-program run time (best of 5, python -B, includes interpreter start-up) ===")
print(f"  (a) one script          : {startup([sys.executable, '-B', 'attendance_all.py', '../data', '/tmp'], 'a_script')*1e3:.1f} ms")
print(f"  (b) one module + main   : {startup([sys.executable, '-B', 'main_b.py', '../data', '/tmp'], 'b_module')*1e3:.1f} ms")
print(f"  (c) three modules       : {startup([sys.executable, '-B', 'main_c.py', '../data', '/tmp'], 'c_modules')*1e3:.1f} ms")
print(f"  (d) package             : {startup([sys.executable, '-B', 'main_d.py', '../data', '/tmp'], 'd_package')*1e3:.1f} ms")
print(f"  interpreter alone       : {startup([sys.executable, '-B', '-c', 'pass'], '.')*1e3:.1f} ms")

print("\n=== 5. Effort to find and change one function (version 1) ===")
print(f"{'organisation':<12}{'files':>6}{'total lines':>13}{'file to open to change percentage()':>40}{'lines in that file':>20}")
for org, f in (("a_script", "attendance_all.py"), ("b_module", "attendance_lib.py"), ("c_modules", "stats.py"), ("d_package", "attendance/stats.py")):
    files = [os.path.join(r, x) for r, _, fs in os.walk(org) for x in fs if x.endswith(".py")]
    total = sum(sum(1 for _ in open(p)) for p in files)
    print(f"{org:<12}{len(files):>6}{total:>13}{f:>40}{sum(1 for _ in open(os.path.join(org, f))):>20}")
