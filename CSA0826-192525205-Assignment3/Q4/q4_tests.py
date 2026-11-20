"""Q4 - duplicates, tuples vs lists in sets, empty/identical electives, hand-verified small case."""
print("1. duplicates are removed by construction (a set holds each value once):")
raw = ["192311001", "192311004", "192311001", "192311009", "192311004", "192311001"]
print("   list with duplicates:", raw, "| set:", sorted(set(raw)), "| 6 entries -> ", len(set(raw)), "students")
print("   what is lost by the conversion: order and how often each appeared:", {r: raw.count(r) for r in set(raw)})

print("\n2. sets can hold tuples but not lists (an element must be hashable):")
print("   {(1, 2), (3, 4)} ->", {(1, 2), (3, 4)})
try:
    {[1, 2]}
except TypeError as e:
    print("   {[1, 2]} -> TypeError:", e)

print("\n3. empty and identical electives:")
A = {"1", "2", "3"}; E = set()
print("   A & empty =", A & E, "| A | empty =", sorted(A | E), "| A ^ empty =", sorted(A ^ E), "| A - empty =", sorted(A - E), "| empty - A =", E - A)
B = {"1", "2", "3"}
print("   identical A, B:  A & B =", sorted(A & B), "| A ^ B =", A ^ B, "(empty: nobody is in exactly one) | A | B =", sorted(A | B), "| A == B:", A == B)
print("   both empty: ", set() & set(), set() ^ set(), set() | set())
print("   note: {} is an empty DICT; an empty set must be written set():", type({}).__name__, type(set()).__name__)

print("\n4. small case verified by hand")
ai = {"S1", "S2", "S3", "S4"}; iot = {"S3", "S4", "S5"}; allst = {"S1", "S2", "S3", "S4", "S5", "S6", "S7"}
print("   AI = {S1,S2,S3,S4}  IoT = {S3,S4,S5}  all = {S1..S7}")
print("   by hand:  both = {S3,S4}; exactly one = {S1,S2,S5}; neither = {S6,S7}")
res = (sorted(ai & iot), sorted(ai ^ iot), sorted(allst - (ai | iot)))
print("   program: ", res)
assert res == (["S3", "S4"], ["S1", "S2", "S5"], ["S6", "S7"])
print("   matches the hand result: True")
