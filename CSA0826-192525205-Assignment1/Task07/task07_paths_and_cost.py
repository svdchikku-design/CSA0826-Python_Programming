"""Where Python looks for modules, and the one-time cost of importing."""
import sys, time
print("sys.path[0:3] =", [p if p else "<current folder>" for p in sys.path[:3]])
print("milkrate loaded yet?", "milkrate" in sys.modules)
t0 = time.perf_counter(); import milkrate; t1 = time.perf_counter()
print(f"first import  : {(t1 - t0) * 1e6:9.1f} microseconds (find file, compile, run)")
t0 = time.perf_counter()
for _ in range(1000):
    import milkrate
t1 = time.perf_counter()
print(f"repeat import : {(t1 - t0) / 1000 * 1e6:9.3f} microseconds each (dictionary lookup in sys.modules)")
print("milkrate loaded now?", "milkrate" in sys.modules, "| file =", milkrate.__file__.split('/')[-1])
try:
    import milkrate_missing
except ModuleNotFoundError as e:
    print("ModuleNotFoundError:", e)
# copy-paste alternative: the same function pasted here
def rate_per_litre_copy(fat, snf):
    return round(30.00 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)
print("copied function gives", rate_per_litre_copy(4.2, 8.7), "- identical today, but a revision must now be made in every script")
