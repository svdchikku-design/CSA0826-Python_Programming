"""Q7: merge duplicate contacts. Dictionary (key -> first contact) + union-find, O(n) expected."""
import re

TITLES = {"dr", "mr", "mrs", "ms", "prof", "sri", "smt"}

def norm_phone(raw):
    """Keep digits only, then the last 10 digits (drops +91, 0 prefix, spaces, dashes). Fewer than 7 digits -> None."""
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) < 7:
        return None
    return digits[-10:]

def norm_email(raw):
    raw = (raw or "").strip().lower()
    return raw if "@" in raw and not raw.startswith("@") and not raw.endswith("@") else None

def norm_name(raw):
    words = re.sub(r"[.,]", " ", (raw or "").lower()).split()
    return " ".join(w for w in words if w not in TITLES)

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]          # path halving
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra

def merge_contacts(contacts):
    """contacts: list of dicts {name, phones, emails}. Returns list of merged dicts (names, phones, emails sets)."""
    n = len(contacts)
    dsu = DSU(n)
    owner = {}                                       # normalised key -> index of first contact that had it
    keys_of = []
    for i, c in enumerate(contacts):
        keys = {("p", p) for p in map(norm_phone, c.get("phones") or []) if p}
        keys |= {("e", e) for e in map(norm_email, c.get("emails") or []) if e}
        keys_of.append(keys)
        for k in keys:
            if k in owner:
                dsu.union(owner[k], i)               # shared key -> same person
            else:
                owner[k] = i
    groups = {}
    for i, c in enumerate(contacts):
        g = groups.setdefault(dsu.find(i), {"names": set(), "phones": set(), "emails": set(), "ids": []})
        nm = norm_name(c.get("name"))
        if nm: g["names"].add(nm)
        g["phones"] |= {k[1] for k in keys_of[i] if k[0] == "p"}
        g["emails"] |= {k[1] for k in keys_of[i] if k[0] == "e"}
        g["ids"].append(i)
    return list(groups.values())

def merge_pairwise(contacts):
    """Alternative: compare every pair of contacts for a shared key, then union. O(n^2)."""
    n = len(contacts); dsu = DSU(n)
    keys_of = []
    for c in contacts:
        keys = {("p", p) for p in map(norm_phone, c.get("phones") or []) if p}
        keys |= {("e", e) for e in map(norm_email, c.get("emails") or []) if e}
        keys_of.append(keys)
    for i in range(n):
        for j in range(i + 1, n):
            if keys_of[i] & keys_of[j]:
                dsu.union(i, j)
    groups = {}
    for i in range(n):
        groups.setdefault(dsu.find(i), []).append(i)
    return list(groups.values())

if __name__ == "__main__":
    contacts = [
        {"name": "Priya Sharma",     "phones": ["+91 98765-43210"], "emails": ["Priya.S@Mail.com"]},          # 0
        {"name": "Dr. Priya Sharma", "phones": ["098765 43210", "044 2345 6789"], "emails": []},                # 1  shares phone with 0
        {"name": "P. Sharma",        "phones": [], "emails": ["priya.s@mail.com ", "priya@work.in"]},         # 2  shares email with 0
        {"name": "Ravi Kumar",       "phones": ["9123456780"], "emails": []},                                   # 3
        {"name": "Ravi Kumar",       "phones": ["9000011111"], "emails": ["ravi.k@mail.com"]},                 # 4  same name, different person
        {"name": "Anita",            "phones": ["12345"], "emails": ["not-an-email"]},                          # 5  invalid data only
        {"name": "Anita D",          "phones": None, "emails": None},                                          # 6  missing fields
        {"name": "Office Landline",  "phones": ["(044) 2345 6789"], "emails": []},                             # 7  shares landline with 1
    ]
    print("INPUT (8 contacts):")
    for i, c in enumerate(contacts): print(f"  {i}: {c}")
    print("\nNormalisation examples:")
    for raw in ("+91 98765-43210", "098765 43210", "(044) 2345 6789", "12345", ""):
        print(f"  norm_phone({raw!r}) -> {norm_phone(raw)!r}")
    print(f"  norm_email('Priya.S@Mail.com ') -> {norm_email('Priya.S@Mail.com ')!r};  norm_email('not-an-email') -> {norm_email('not-an-email')!r}")
    print(f"  norm_name('Dr. Priya Sharma') -> {norm_name('Dr. Priya Sharma')!r}")
    print("\nMERGED OUTPUT:")
    res = merge_contacts(contacts)
    for g in sorted(res, key=lambda g: g["ids"][0]):
        print(f"  contacts {g['ids']}: names={sorted(g['names'])} phones={sorted(g['phones'])} emails={sorted(g['emails'])}")
    print(f"\n{len(contacts)} contacts -> {len(res)} merged people")
    print("Hand-derived expected: {0,1,2,7} one person (0-1 phone, 0-2 email, 1-7 landline), {3}, {4}, {5}, {6} => 5 groups")
    assert sorted(sorted(g["ids"]) for g in res) == [[0, 1, 2, 7], [3], [4], [5], [6]]
    assert sorted(sorted(g) for g in merge_pairwise(contacts)) == sorted(sorted(g["ids"]) for g in res)
    print("assertions passed; pairwise version gives identical groups: True")
    print("\nKnown limitation shown: the shared office landline (contact 7) pulled 'Office Landline' into Priya's group.")
