ai_elective = {"192311001", "192311004", "192311007", "192311009"}

iot_elective = {"192311002", "192311004", "192311009", "192311010"}

all_students = {f"1923110{i:02d}" for i in range(1, 11)}

# TODO 1 (completed) with set OPERATORS only
both = ai_elective & iot_elective                         # intersection: in both electives (the clash)
exactly_one = ai_elective ^ iot_elective                  # symmetric difference: in exactly one
neither = all_students - (ai_elective | iot_elective)     # difference from the union: registered in none

print("clash :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither :", sorted(neither))

# the same with set METHODS
both_m = ai_elective.intersection(iot_elective)
exactly_one_m = ai_elective.symmetric_difference(iot_elective)
neither_m = all_students.difference(ai_elective.union(iot_elective))
print("\nmethods give the same sets:", both == both_m, exactly_one == exactly_one_m, neither == neither_m)
print("only AI :", sorted(ai_elective - iot_elective), "| only IoT:", sorted(iot_elective - ai_elective))
print("union   :", sorted(ai_elective | iot_elective), "(", len(ai_elective | iot_elective), "students )")
print("counts check: |A| + |B| = |A∪B| + |A∩B| ->", len(ai_elective) + len(iot_elective), "=", len(ai_elective | iot_elective) + len(ai_elective & iot_elective))
