"""Q7 measurements: ground-truth synthetic contacts, dictionary+DSU (O(n)) vs pairwise (O(n^2))."""
import random, time, tracemalloc
from q7_contacts import merge_contacts, merge_pairwise

def make_contacts(n_people, seed=1):
    rnd = random.Random(seed); used = set(); contacts = []; truth = []
    def phone():
        while True:
            p = str(rnd.randrange(6_000_000_000, 10_000_000_000))
            if p not in used: used.add(p); return p
    def fmt(p):
        return rnd.choice([p, "+91 " + p[:5] + "-" + p[5:], "0" + p[:5] + " " + p[5:], "+91" + p])
    for pid in range(n_people):
        k = rnd.randint(1, 3)                                   # number of entries for this person
        keys = [("p", phone()) for _ in range(k)] + [("e", f"user{pid}.{rnd.randrange(10**6)}@mail.com")]
        keys = keys[:k + 1]
        base = f"person{pid} surname"
        for j in range(k):                                      # entry j holds keys j and j+1 -> chain: connected
            ph = [fmt(v) for t, v in keys[j:j + 2] if t == "p"]
            em = [v.upper() if rnd.random() < .5 else v for t, v in keys[j:j + 2] if t == "e"]
            contacts.append({"name": rnd.choice([base, "Dr. " + base, base.upper()]), "phones": ph, "emails": em})
            truth.append(pid)
    order = list(range(len(contacts))); rnd.shuffle(order)
    return [contacts[i] for i in order], [truth[i] for i in order]

def correct(groups, truth, n_people):
    gids = [{truth[i] for i in g} for g in groups]
    return len(groups) == n_people and all(len(s) == 1 for s in gids)

print("A. Correctness against ground truth (shuffled input, mixed formats)")
print(f"{'people':>8} {'contacts n':>11} {'groups found':>13} {'every group is one person':>26}")
for P in (100, 1000, 10000):
    c, t = make_contacts(P)
    g = [x["ids"] for x in merge_contacts(c)]
    print(f"{P:>8} {len(c):>11} {len(g):>13} {str(correct(g, t, P)):>26}")

print("\nB. Dictionary + union-find: time and memory")
print(f"{'contacts n':>11} {'time (s)':>9} {'us per contact':>15} {'peak memory (MB)':>17} {'correct':>8}")
rows = {}
for P in (500, 5000, 50000):
    c, t = make_contacts(P)
    t0 = time.perf_counter(); g = merge_contacts(c); dt = time.perf_counter() - t0
    tracemalloc.start(); merge_contacts(c); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    rows[len(c)] = dt
    print(f"{len(c):>11} {dt:>9.3f} {dt / len(c) * 1e6:>15.2f} {peak / 1e6:>17.2f} {str(correct([x['ids'] for x in g], t, P)):>8}")

print("\nC. The two required sizes: about 1,000 and 100,000 contacts")
c1, t1 = make_contacts(500, seed=2)
c2, t2 = make_contacts(50000, seed=3)
print(f"  n = {len(c1)} contacts (target 1,000)")
t0 = time.perf_counter(); g1 = merge_contacts(c1); a1 = time.perf_counter() - t0
t0 = time.perf_counter(); p1 = merge_pairwise(c1); b1 = time.perf_counter() - t0
ok = sorted(sorted(x["ids"]) for x in g1) == sorted(sorted(x) for x in p1)
print(f"    dictionary+DSU {a1 * 1e3:.2f} ms | pairwise {b1 * 1e3:.1f} ms | pairwise/dict = {b1 / a1:.0f}x | same groups: {ok}")
print(f"  n = {len(c2)} contacts (target 100,000)")
t0 = time.perf_counter(); g2 = merge_contacts(c2); a2 = time.perf_counter() - t0
print(f"    dictionary+DSU {a2:.3f} s ({a2 / len(c2) * 1e6:.2f} us per contact) groups={len(g2)} correct={correct([x['ids'] for x in g2], t2, 50000)}")

print("\nD. Pairwise measured at small n, then extrapolated with n^2")
print(f"{'n':>7} {'pairs n(n-1)/2':>15} {'pairwise (s)':>13} {'ns per pair':>12} {'dict+DSU (ms)':>14}")
ns_pair = []
for P in (250, 500, 1000, 2000):
    c, t = make_contacts(P, seed=5)
    n = len(c)
    t0 = time.perf_counter(); merge_pairwise(c); b = time.perf_counter() - t0
    t0 = time.perf_counter(); merge_contacts(c); a = time.perf_counter() - t0
    pairs = n * (n - 1) // 2; ns_pair.append(b / pairs * 1e9)
    print(f"{n:>7} {pairs:>15} {b:>13.3f} {b / pairs * 1e9:>12.1f} {a * 1e3:>14.2f}")
avg = sum(ns_pair[-2:]) / 2
for n in (1000, 100000, 1000000):
    pairs = n * (n - 1) // 2; sec = pairs * avg * 1e-9
    print(f"  extrapolated pairwise at n={n:>9,}: {pairs:>16,} pairs x {avg:.0f} ns = {sec:,.1f} s = {sec / 3600:,.2f} h")
t100k = a2 * 2  # a2 was for ~100k contacts
print(f"  measured dictionary+DSU at n={len(c2):,}: {a2:.2f} s -> extrapolated pairwise is about {n * 0 + (100000*99999//2*avg*1e-9) / a2:,.0f}x slower")
