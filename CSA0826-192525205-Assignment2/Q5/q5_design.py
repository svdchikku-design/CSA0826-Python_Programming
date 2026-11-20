"""Q5 design: independent orders, parameter kinds, returning several values, and scope."""
from decimal import Decimal, ROUND_HALF_UP

MENU = {"Tea": Decimal("10"), "Vada": Decimal("12"), "Dosa": Decimal("40"), "Coffee": Decimal("15")}
GST_RATE = Decimal("0.05")                      # a global CONSTANT: read-only inside functions

def add_item(item, order=None, quantity=1):
    """Add `quantity` of `item` to `order` (a new order is started when none is given); returns the order dict."""
    if order is None:
        order = {}
    order[item] = order.get(item, 0) + quantity
    return order

def bill(order, gst_rate=GST_RATE):
    """Return (subtotal, gst, total) as one tuple, so the caller can unpack three values."""
    subtotal = sum((MENU[i] * q for i, q in order.items()), Decimal("0"))
    gst = (subtotal * gst_rate).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return subtotal, gst, subtotal + gst

print("=== positional, keyword and default parameters ===")
o = add_item("Tea")                              # positional; order and quantity use their defaults
o = add_item("Vada", o, 2)                       # all positional
o = add_item("Dosa", quantity=1, order=o)        # keyword arguments: order does not matter, meaning is clear
print("order:", o)
print("bill(o) positional  :", bill(o))
print("bill(o, gst_rate=Decimal('0.18')) keyword override:", bill(o, gst_rate=Decimal("0.18")))
subtotal, gst, total = bill(o)                   # unpacking a returned tuple
print(f"unpacked: subtotal={subtotal}  gst={gst}  total={total}")

print("\n=== three customers in sequence: each order is independent ===")
customers = {"Customer 1": [("Tea", 1), ("Vada", 2)], "Customer 2": [("Coffee", 2)], "Customer 3": [("Dosa", 1), ("Tea", 3)]}
orders = {}
for name, lines in customers.items():
    order = None
    for item, qty in lines:
        order = add_item(item, order, qty)
    orders[name] = order
    print(f"{name}: {order}  -> subtotal/gst/total = {bill(order)}")
assert orders["Customer 1"] == {"Tea": 1, "Vada": 2} and orders["Customer 2"] == {"Coffee": 2} and orders["Customer 3"] == {"Dosa": 1, "Tea": 3}
assert len({id(o) for o in orders.values()}) == 3
print("three different objects, no item leaked from one customer to the next: True")

print("\n=== local, global and nonlocal ===")
counter = 0                                      # global
def bad_increment():
    try:
        counter = counter + 1                    # assignment makes 'counter' local -> read before assignment fails
    except UnboundLocalError as e:
        print("  without 'global':", type(e).__name__ + ":", e)
def global_increment():
    global counter                               # explicit permission to re-bind the module-level name
    counter += 1
bad_increment(); global_increment(); global_increment()
print("  with 'global', counter =", counter)

def make_counter():
    count = 0                                    # local to make_counter, but enclosing for inner
    def inner():
        nonlocal count                           # re-bind the enclosing function's variable
        count += 1
        return count
    return inner
c1, c2 = make_counter(), make_counter()
print("  nonlocal: c1() c1() c2() ->", c1(), c1(), c2(), "(each closure keeps its own count)")
def local_demo():
    x = "local"                                  # a local name hides a global of the same name
    return x
x = "global"
print("  local hides global:", local_demo(), "| global x still", x)
print("  why globals are avoided: any function may change 'counter' (now", counter, "), so a bug can come from anywhere and tests cannot isolate a function.")
