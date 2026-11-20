import time

items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]

def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text

def build_join(parts):
    # TODO 1 (completed): build the same text using a single str.join() call
    return ";".join(parts) + ";"

start = time.perf_counter(); a = build_plus(items); t_plus = time.perf_counter() - start
start = time.perf_counter(); b = build_join(items); t_join = time.perf_counter() - start

print("same text:", a == b, "| length:", len(b))
print(f"+= time: {t_plus:.4f} s   join time: {t_join:.4f} s")
