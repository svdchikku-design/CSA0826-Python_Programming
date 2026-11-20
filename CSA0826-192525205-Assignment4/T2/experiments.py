"""Task 2 alternative: read every file once (dictionary) versus re-read all files for every student."""
import random, time, tempfile, os, shutil
from pathlib import Path
from attendance_month import process_month

def make_month(folder, students, files, lines_per_file, seed=2):
    rnd = random.Random(seed); os.makedirs(folder, exist_ok=True)
    regs = [str(192311000 + i) for i in range(students)]
    for d in range(files):
        with open(Path(folder) / f"2026-10-{d+1:02d}.txt", "w") as f:
            for _ in range(lines_per_file):
                f.write(f"{rnd.choice(regs)},2026-10-{d+1:02d},{rnd.choice('PPPA')}\n")
    return regs

def per_student_rescan(folder, regs):
    out = {}
    for reg in regs:                                     # for every student ...
        p = a = 0
        for path in sorted(Path(folder).glob("*.txt")):  # ... read EVERY file again
            with open(path) as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3 and parts[0] == reg:
                        if parts[2] == "P": p += 1
                        elif parts[2] == "A": a += 1
        out[reg] = (p, a)
    return out

tmp = tempfile.mkdtemp()
print("Derivation: one pass = O(f*l) line reads, memory O(s) counters. Re-scan per student = O(s*f*l) line reads, memory O(1) extra.\n")
print(f"{'s':>5} {'f':>3} {'l':>5} | {'lines read once f*l':>20} {'lines read re-scan s*f*l':>25} | {'one pass (s)':>13} {'re-scan (s)':>12} {'ratio':>7} | same answer")
for s, f, l in ((20, 10, 200), (40, 10, 200), (80, 10, 200), (160, 10, 200)):
    folder = os.path.join(tmp, f"m{s}"); regs = make_month(folder, s, f, l)
    t0 = time.perf_counter(); rows, _, _ = process_month(folder, os.path.join(tmp, "a.csv"), os.path.join(tmp, "b.txt"), os.path.join(tmp, "c.log")); t1 = time.perf_counter() - t0
    t0 = time.perf_counter(); alt = per_student_rescan(folder, regs); t2 = time.perf_counter() - t0
    same = all(alt.get(r, (0, 0)) == (p, a) for r, p, a, _ in rows)
    print(f"{s:>5} {f:>3} {l:>5} | {f*l:>20,} {s*f*l:>25,} | {t1:>13.4f} {t2:>12.4f} {t2/t1:>6.0f}x | {same}")
print("\nDoubling s doubled the re-scan time (x2) while the one-pass time barely moved: O(s*f*l) versus O(f*l).")
print("A realistic month: 30 files x 5,000 lines, 3,000 students: one pass 150,000 line reads; re-scan 450,000,000 line reads.")
shutil.rmtree(tmp)
