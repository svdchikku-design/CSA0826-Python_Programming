"""Q5 - canteen orders: the default-parameter bug, the fix, parameters, multiple returns, scope."""
from decimal import Decimal, ROUND_HALF_UP

def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    # TODO 1 (completed): a new empty list when order is None, append the item, return the list
    if order is None:
        order = []
    order.append(item)
    return order

print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"), add_item("Vada"))
print("add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)
print("add_item.__defaults__       =", add_item.__defaults__)
print("-> the default list was created ONCE, when 'def' ran; every call without 'order' appends to that same list object.")
print("   id of the default list:", id(add_item_buggy.__defaults__[0]), "| id of the list returned by each call:",
      id(add_item_buggy("Dosa")), id(add_item_buggy("Idli")), "(identical)")
print("   after two more calls the default has grown to", add_item_buggy.__defaults__[0])
