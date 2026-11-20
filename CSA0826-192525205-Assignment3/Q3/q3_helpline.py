"""Q3 - Kisan call centre: word counts, grouping by district and crop, stop words, text clean-up, views and order."""
import string
from collections import Counter

STOP = {"not", "high", "the", "is", "a", "to", "of", "and", "for", "in", "no", "my", "have", "has"}
_TABLE = str.maketrans("", "", string.punctuation)

def words_of(text):
    """lower case, punctuation removed, split on whitespace; '' gives []."""
    return text.lower().translate(_TABLE).split()

def frequencies_get(texts, stop=STOP):
    counts = {}
    for text in texts:
        for w in words_of(text):
            if w not in stop:
                counts[w] = counts.get(w, 0) + 1                 # get(): default 0 when the word is new
    return counts

def frequencies_setdefault(texts, stop=STOP):
    counts = {}
    for text in texts:
        for w in words_of(text):
            if w not in stop:
                counts.setdefault(w, 0)                          # setdefault(): insert 0 only if the key is missing
                counts[w] += 1
    return counts

def top_k(counts, k):
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:k]

if __name__ == "__main__":
    records = [   # (district, crop, complaint)
        ("Thanjavur", "paddy", "Seeds not received, seeds delayed!"),
        ("Madurai", "cotton", "Fertiliser price HIGH."),
        ("Thanjavur", "paddy", "Seeds price high; subsidy not received"),
        ("Salem", "maize", "Pest attack - no pesticide available"),
        ("Madurai", "cotton", "Seeds delayed, price is high"),
        ("Salem", "paddy", ""),
        ("Thanjavur", "cotton", "Pesticide price high and subsidy delayed"),
    ]
    texts = [r[2] for r in records]

    print("1. word frequencies (stop words removed, lower case, punctuation removed):")
    f1, f2 = frequencies_get(texts), frequencies_setdefault(texts)
    print("   get()        :", f1)
    print("   setdefault() :", f2, "| identical:", f1 == f2)
    print("   top 5        :", top_k(f1, 5))

    print("\n2. complaints per district, with a dictionary of lists (setdefault creates the list the first time):")
    by_district = {}
    for district, crop, text in records:
        by_district.setdefault(district, []).append(text)
    for d, lst in by_district.items():
        print(f"   {d:<10} {len(lst)} complaint(s): {lst}")

    print("\n3. complaints for each crop (empty text kept as a complaint with no words):")
    by_crop = {}
    for district, crop, text in records:
        by_crop.setdefault(crop, []).append((district, text))
    for c, lst in sorted(by_crop.items()):
        print(f"   {c:<7} {lst}")

    print("\n4. text tests:")
    for label, t in (("empty text", ""), ("only punctuation", "!!! ... ???"), ("upper/lower case", "SEEDS Seeds seeds"), ("punctuation", "seeds, seeds. seeds!")):
        print(f"   {label:<17} {t!r:<24} -> {frequencies_get([t])}")

    print("\n5. order of keys in Python 3.7+ is the order of first insertion (not alphabetical, not by count):")
    d = {}
    for w in ["zebra", "apple", "mango", "apple", "zebra", "kiwi"]:
        d[w] = d.get(w, 0) + 1
    print("   ", d, "-> keys:", list(d))

    print("\n6. views are live windows on the dictionary, not copies:")
    ks, vs, its = d.keys(), d.values(), d.items()
    print("   keys()  :", ks, "\n   values():", vs, "\n   items() :", its)
    d["banana"] = 9
    print("   after d['banana'] = 9 the SAME view objects now show:", list(ks), list(vs)[-1], list(its)[-1])
    print("   membership in keys() is a hash lookup:", "kiwi" in ks, "| value 9 in values() is a scan:", 9 in vs)
