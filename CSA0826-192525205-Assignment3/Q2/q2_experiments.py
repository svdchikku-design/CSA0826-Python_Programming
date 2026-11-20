"""Q2 - tuples, mutability, copying, memory/time of tuple vs list, and the sparse-dictionary grid."""
import copy, sys, time, tracemalloc

print("=== 1. The bug and its correction with 'is' and id() ===")
bad = [[0] * 3] * 3
good = [[0] * 3 for _ in range(3)]
print("bad  ids of the 3 rows :", [id(r) for r in bad], "-> all identical:", bad[0] is bad[1] is bad[2])
print("good ids of the 3 rows :", [id(r) for r in good], "-> all different:", len({id(r) for r in good}) == 3)
bad[1][2] += 5
good[1][2] += 5
print("after row 1, col 2 += 5 ->  bad :", bad, "\n                            good:", good)

print("\n=== 2. Aliasing, shallow copy, deep copy ===")
orig = [[1, 2], [3, 4]]
alias = orig
shallow1 = orig[:]
shallow2 = copy.copy(orig)
deep = copy.deepcopy(orig)
print("alias   is orig:", alias is orig, "| shallow (slice) is orig:", shallow1 is orig, "| shallow (copy.copy) is orig:", shallow2 is orig, "| deep is orig:", deep is orig)
print("inner lists shared?  shallow1[0] is orig[0]:", shallow1[0] is orig[0], "| shallow2[0] is orig[0]:", shallow2[0] is orig[0], "| deep[0] is orig[0]:", deep[0] is orig[0])
orig.append([5, 6])                 # change the OUTER list
orig[0][0] = 99                     # change an INNER list
print("orig    :", orig)
print("alias   :", alias, " <- sees both changes (same object)")
print("shallow1:", shallow1, " <- no new row, but inner list changed (shared)")
print("shallow2:", shallow2, " <- same as shallow1")
print("deep    :", deep, " <- independent of both changes")
flat = [1, 2, 3]
flat_copy = flat[:]
flat[0] = 100
print("a list of immutable items: copy is enough ->", flat, flat_copy)

print("\n=== 3. A function that changes its list argument ===")
def add_stop(stops, name):
    stops.append(name)              # mutates the object the caller passed in
    return stops
def add_stop_safe(stops, name):
    return stops + [name]           # builds a new list; the caller's list is untouched
route = ["Central"]
add_stop(route, "T. Nagar")
print("after add_stop(route, ...)      route =", route, " (the parameter and 'route' are two names for ONE list)")
route2 = ["Central"]; new = add_stop_safe(route2, "T. Nagar")
print("after add_stop_safe(route2, ...) route2 =", route2, "| returned:", new)
def rebind(stops):
    stops = ["something else"]      # re-binding the local name does not touch the caller's list
rebind(route); print("rebinding the parameter inside a function leaves the caller's list:", route)

print("\n=== 4. Unpacking tuples in a for loop; tuples as dictionary keys ===")
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar", (13.0674, 80.2376): "Egmore"}
for (lat, lon), name in stops.items():
    print(f"  {name:<16} lat={lat:<8} lon={lon}")
for lat, lon in stops:
    pass
print("  lookup by tuple key:", stops[(13.0674, 80.2376)])

print("\n=== 5. A list stored inside a tuple ===")
t = ("route A", [1, 2, 3])
print("t =", t, "| id of the inner list:", id(t[1]))
t[1].append(4)
print("t[1].append(4) works  ->", t, "| same inner list:", id(t[1]))
try:
    t[1] = [9]
except TypeError as e:
    print("t[1] = [9] -> TypeError:", e)
try:
    t[1] += [5]
except TypeError as e:
    print("t[1] += [5] -> TypeError:", e)
print("   ...yet the list WAS changed before the error:", t)
try:
    hash(t)
except TypeError as e:
    print("hash(t) ->", e, "(a tuple is hashable only if everything inside it is hashable)")

print("\n=== 6. Memory and time: list versus tuple of 1,000,000 values ===")
N = 1_000_000
lst = list(range(N)); tup = tuple(lst)
print(f"sys.getsizeof(list)  = {sys.getsizeof(lst):>10,} bytes")
print(f"sys.getsizeof(tuple) = {sys.getsizeof(tup):>10,} bytes   (difference {sys.getsizeof(lst) - sys.getsizeof(tup):,} bytes: list(range()) is built to exact size; the list header holds an extra capacity field)")
grown = []
for v in range(N): grown.append(v)
print(f"a list grown by append() (spare capacity kept for future growth): {sys.getsizeof(grown):,} bytes")
print("(both only hold 8-byte references; the million int objects themselves are shared and not counted)")
def best(f, reps=5):
    b = 1e9
    for _ in range(reps):
        t0 = time.perf_counter(); f(); b = min(b, time.perf_counter() - t0)
    return b
t_list = best(lambda: list(range(N))); t_tup = best(lambda: tuple(range(N)))
idx = list(range(0, N, 997))
def index_all(seq):
    s = 0
    for i in idx: s += seq[i]
    return s
t_il, t_it = best(lambda: index_all(lst)), best(lambda: index_all(tup))
print(f"create from range({N:,}): list {t_list * 1e3:7.2f} ms | tuple {t_tup * 1e3:7.2f} ms")
print(f"index {len(idx)} positions     : list {t_il * 1e6:7.1f} us | tuple {t_it * 1e6:7.1f} us")
import timeit
print("create a small 5-item literal (1,000,000 times):  list", round(timeit.timeit("[1,2,3,4,5]", number=1000000), 3), "s | tuple", round(timeit.timeit("(1,2,3,4,5)", number=1000000), 3), "s (the tuple of constants is built once at compile time)")
