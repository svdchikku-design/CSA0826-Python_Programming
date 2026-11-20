"""B4.1: scorer and summariser on 60 complaints compared with my own reading; speed at the new scale (50,000 complaints a month)."""
import sys, time, tracemalloc
sys.path.insert(0, "../common")
from sentiment import label, score
from summariser import sentences, summarise_frequency, summarise_first
from complaints import COMPLAINTS

print(f"{len(COMPLAINTS)} complaints written for this assignment, labelled by my own reading (positive/negative/neutral) and with the main sentence marked.\n")
print("1. SENTIMENT: lexicon + negation scorer (the TODO program's lexicon) against my labels")
agree = 0; conf = {}
wrong = []
for text, mine, key in COMPLAINTS:
    got = label(text); conf[(mine, got)] = conf.get((mine, got), 0) + 1
    if got == mine: agree += 1
    else: wrong.append((text, mine, got, score(text)))
print(f"   agreement: {agree} of {len(COMPLAINTS)} = {agree/len(COMPLAINTS):.0%}")
print(f"   {'my reading \\ program':<22}{'positive':>9}{'negative':>9}{'neutral':>9}{'total':>7}{'right':>7}")
for m in ("positive", "negative", "neutral"):
    row = [conf.get((m, g), 0) for g in ("positive", "negative", "neutral")]
    print(f"   {m:<22}{row[0]:>9}{row[1]:>9}{row[2]:>9}{sum(row):>7}{conf.get((m, m), 0):>7}")
print(f"\n   the {len(wrong)} disagreements:")
for text, mine, got, s in wrong:
    print(f"   [{mine} -> program says {got}, score {s:+d}] {text}")

print("\n2. SUMMARISER: top-1 sentence by word frequency versus first sentence, compared with the sentence I marked as the main point")
f_ok = sum(summarise_frequency(t, 1)[0] == sentences(t)[k] for t, _, k in COMPLAINTS)
s_ok = sum(summarise_first(t, 1)[0] == sentences(t)[k] for t, _, k in COMPLAINTS)
multi = [(t, m, k) for t, m, k in COMPLAINTS if len(sentences(t)) > 1]
print(f"   complaints with more than one sentence: {len(multi)}")
print(f"   frequency-based summariser picks my main sentence: {f_ok} of {len(COMPLAINTS)}")
print(f"   first-sentence summariser picks my main sentence:  {s_ok} of {len(COMPLAINTS)}")
print("   complaints where my main sentence is NOT the first one:", sum(k != 0 for _, _, k in COMPLAINTS))
print("   cases where the two summarisers differ (first sentence vs frequency):")
for t, m, k in COMPLAINTS:
    a, b = summarise_frequency(t, 1)[0], summarise_first(t, 1)[0]
    if a != b: print(f"     frequency: {a!r:<60} first: {b!r:<50} mine: {sentences(t)[k]!r}")
print("   example summaries (k=1):")
for i in (0, 4, 18, 28):
    t = COMPLAINTS[i][0]; print(f"     {t}\n       -> frequency: {summarise_frequency(t,1)[0]}\n       -> first:     {summarise_first(t,1)[0]}")

print("\n3. SPEED at the new scale: 50,000 complaints (the 60 repeated)")
big = [c[0] for c in COMPLAINTS] * 834
big = big[:50000]
for name, fn in (("sentiment label()", label), ("summariser by frequency", lambda t: summarise_frequency(t, 1)), ("summariser first sentence", lambda t: summarise_first(t, 1))):
    t0 = time.perf_counter(); out = [fn(t) for t in big]; dt = time.perf_counter() - t0
    tracemalloc.start(); [fn(t) for t in big[:1000]]; peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"   {name:<28}{dt:.3f} s for {len(big):,} complaints = {dt/len(big)*1e6:.1f} us each; peak memory for 1,000 complaints {peak/1e3:.0f} KB")
print("\n4. First-k time grows with the number of sentences kept, not the length: one long complaint (2,000 words) with k=1")
long_text = ("Smoke is bad near the school. " + "The road is dusty and the trucks pass at night. " * 300)
for name, fn in (("frequency", lambda: summarise_frequency(long_text, 1)), ("first sentence", lambda: summarise_first(long_text, 1))):
    t0 = time.perf_counter()
    for _ in range(200): fn()
    print(f"   {name:<16}{(time.perf_counter()-t0)/200*1e6:>9.1f} us per call on {len(long_text.split())} words")
