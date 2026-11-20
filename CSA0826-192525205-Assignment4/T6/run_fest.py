"""Main script: python run_fest.py <input_folder> <output_folder>"""
import sys
from fest.processor import run

if __name__ == "__main__":
    src, dst = (sys.argv[1], sys.argv[2]) if len(sys.argv) >= 3 else ("data_demo", "out_demo")
    master, errors, stats, counts = run(src, dst)
    print(f"input '{src}' -> output '{dst}'")
    for k, v in stats.items(): print(f"  {k}: {v}")
    print("  participants per event:", dict(sorted(counts.items())))
    print(f"  {len(errors)} line(s) in errors.log")
