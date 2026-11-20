"""Q3 experiments: dictionary vs list.count() vs Counter; lookup cost versus dictionary size."""
import random, time, tracemalloc
from collections import Counter
from q3_helpline import words_of, STOP

rnd = random.Random(11)
VOCAB = [f"word{i:03d}" for i in range(300)]
WEIGHTS = [1 / (i + 1) for i in range(300)]              # a few very common words and a long tail (Zipf-like)
def make_complaints(n, words_each=8):
    return [" ".join(rnd.choices(VOCAB, WEIGHTS, k=words_each)).capitalize() + "." for _ in range(n)]

def count_dict(texts):
    counts = {}
    for t in texts:
        for w in words_of(t):
            if w not in STOP:
                counts[w] = counts.get(w, 0) + 1
    return counts

def count_list_count(texts):
    words = [w for t in texts for w in words_of(t) if w not in STOP]
    return {w: words.count(w) for w in set(words)}        # one full pass over the list for EVERY distinct word

def count_counter(texts):
    return Counter(w for t in texts for w in words_of(t) if w not in STOP)

print(f"{'complaints':>11} {'words n':>9} {'distinct d':>11} | {'dict loop':>10} {'list.count':>11} {'Counter':>9} | list.count / dict | n*d comparisons")
data = {}
for n in (1000, 10000, 100000):
    texts = make_complaints(n)
    t0 = time.perf_counter(); a = count_dict(texts); t_a = time.perf_counter() - t0
    t0 = time.perf_counter(); b = count_list_count(texts); t_b = time.perf_counter() - t0
    t0 = time.perf_counter(); c = Counter(count_counter(texts)); t_c = time.perf_counter() - t0
    assert a == b == dict(c)
    words = sum(a.values())
    data[n] = (t_a, t_b, t_c)
    print(f"{n:>11} {words:>9} {len(a):>11} | {t_a:>9.4f}s {t_b:>10.4f}s {t_c:>8.4f}s | {t_b / t_a:>16.1f}x | {words * len(a):>14,}")

print("\nGrowth when the number of complaints grows 10x (the vocabulary d stays about 300):")
print(f"  dict loop  : x{data[10000][0] / data[1000][0]:.1f}, x{data[100000][0] / data[10000][0]:.1f}   (O(n): about x10)")
print(f"  list.count : x{data[10000][1] / data[1000][1]:.1f}, x{data[100000][1] / data[10000][1]:.1f}   (O(n*d): about x10 while d is constant - but with a large constant 300)")
print(f"  Counter    : x{data[10000][2] / data[1000][2]:.1f}, x{data[100000][2] / data[10000][2]:.1f}")

print("\nWhen the vocabulary grows too (d proportional to n) the O(n*d) method becomes quadratic:")
print(f"{'words n':>9} {'distinct d':>11} | {'dict loop':>10} {'list.count':>11}")
for n in (2000, 4000, 8000, 16000):
    words = [f"w{rnd.randrange(n // 2)}" for _ in range(n)]
    t0 = time.perf_counter(); d1 = {}
    for w in words: d1[w] = d1.get(w, 0) + 1
    ta = time.perf_counter() - t0
    t0 = time.perf_counter(); d2 = {w: words.count(w) for w in set(words)}; tb = time.perf_counter() - t0
    assert d1 == d2
    print(f"{n:>9} {len(d1):>11} | {ta:>9.5f}s {tb:>10.5f}s   (list.count doubled n -> time x{tb / prev:.1f})" if 'prev' in dir() else f"{n:>9} {len(d1):>11} | {ta:>9.5f}s {tb:>10.5f}s")
    prev = tb

print("\nMemory held by the counting structures for 100,000 complaints:")
texts = make_complaints(100000)
tracemalloc.start(); a = count_dict(texts); m1 = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
tracemalloc.start(); b = count_list_count(texts); m2 = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
tracemalloc.start(); c = count_counter(texts); m3 = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
print(f"  dict loop (peak): {m1 / 1e3:8.1f} KB   <- O(d)\n  list.count (peak): {m2 / 1e6:7.2f} MB   <- O(n): it first builds the whole list of words\n  Counter (peak)  : {m3 / 1e3:8.1f} KB   <- O(d)")

print("\nAverage dictionary lookup time versus the number of keys (hash lookup does not depend on size):")
for size in (1000, 100000, 1000000, 5000000):
    d = {i: i for i in range(size)}
    keys = [rnd.randrange(size) for _ in range(300000)]
    t0 = time.perf_counter()
    for k in keys: d[k]
    print(f"  {size:>8} keys: {(time.perf_counter() - t0) / len(keys) * 1e9:6.1f} ns per lookup")
    del d
print("\nTop 10 words for 100,000 complaints (sorted by count desc, then alphabetical):")
cnt = count_dict(texts)
print(" ", sorted(cnt.items(), key=lambda p: (-p[1], p[0]))[:10])
print("  most_common(10) from Counter:", Counter(cnt).most_common(10) == sorted(cnt.items(), key=lambda p: (-p[1], p[0]))[:10], "(ties may be ordered differently: Counter keeps first-seen order)")
