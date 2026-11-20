"""Q3 inquiry: immutability, upper() and the slices s[-4:] and s[4:-4]."""
s = "tn09ab1234"
print("s =", repr(s), "| id(s) =", id(s))
try:
    s[0] = "T"
except TypeError as e:
    print("s[0] = 'T'  ->  TypeError:", e)
u = s.upper()
print("s.upper() returned", repr(u), "| s is still", repr(s), "| different objects:", id(u) != id(s))
s = s.upper()
print("s = s.upper() re-binds the NAME to the new string: id(s) =", id(s))
print()
for label, plate in (("9 characters", "KA01M0007"), ("10 characters", "TN09AB1234")):
    print(f"{label}: {plate!r} len={len(plate)}")
    print(f"   plate[-4:]  = {plate[-4:]!r}    (last four characters: the digits)")
    print(f"   plate[4:-4] = {plate[4:-4]!r}   (from index 4 up to, not including, the 4th from the end: the series letters)")
    print(f"   plate[:2] = {plate[:2]!r}, plate[2:4] = {plate[2:4]!r}")
print("\nLimitations of isalpha()/isdigit() (they accept more than A-Z and 0-9):")
for odd in ("TN０９AB１２３４", "TN09ÄB1234", "TN09AB١٢٣٤"):
    print(f"   {odd!r:22} -> is_valid? ", end="")
    from q3_plate_funcs import is_valid
    print(is_valid(odd))
