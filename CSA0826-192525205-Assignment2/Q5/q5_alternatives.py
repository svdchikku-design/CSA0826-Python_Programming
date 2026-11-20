"""Q5 alternatives: caller always passes the order; or a closure keeps the order. Compare with default None."""
import time, tracemalloc, sys

def add_none(item, order=None):                 # chosen design: default None
    if order is None:
        order = []
    order.append(item)
    return order

def add_explicit(item, order):                  # the caller must create the list
    order.append(item)
    return order

def make_order():                               # closure: the list lives inside the inner function
    items = []
    def add(item):
        items.append(item)
        return items
    return add

# correctness: three customers each way
a = [add_none("Tea"), add_none("Vada")]
b1 = []; b2 = []; add_explicit("Tea", b1); add_explicit("Vada", b2)
c1, c2 = make_order(), make_order(); c1("Tea"); c2("Vada")
print("default None :", a)
print("explicit list:", [b1, b2])
print("closures     :", [c1.__closure__[0].cell_contents, c2.__closure__[0].cell_contents])

# time per item (O(1) each)
N = 300000
def per_item_us(run):
    t0 = time.perf_counter(); run(); return (time.perf_counter() - t0) / N * 1e6
def run_none():
    o = None
    for _ in range(N): o = add_none("Tea", o)
def run_explicit():
    o = []
    for _ in range(N): add_explicit("Tea", o)
def run_closure():
    add = make_order()
    for _ in range(N): add("Tea")
print(f"\nmicroseconds per item added ({N} items): default None {per_item_us(run_none):.3f} | explicit {per_item_us(run_explicit):.3f} | closure {per_item_us(run_closure):.3f}")

# space per customer: 100,000 customers x 5 items
CUST = 100_000
def space(build):
    tracemalloc.start(); keep = [build() for _ in range(CUST)]; cur = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    return cur / CUST
def customer_none():
    o = None
    for it in ("Tea", "Vada", "Dosa", "Tea", "Coffee"): o = add_none(it, o)
    return o
def customer_explicit():
    o = []
    for it in ("Tea", "Vada", "Dosa", "Tea", "Coffee"): add_explicit(it, o)
    return o
def customer_closure():
    add = make_order()
    for it in ("Tea", "Vada", "Dosa", "Tea", "Coffee"): add(it)
    return add
print(f"\nbytes per customer holding 5 items (average over {CUST} customers):")
print(f"  default None : {space(customer_none):.0f}  (a list of 5 references)")
print(f"  explicit list: {space(customer_explicit):.0f}  (the same list)")
print(f"  closure      : {space(customer_closure):.0f}  (list + function object + cell: constant extra overhead per customer)")
