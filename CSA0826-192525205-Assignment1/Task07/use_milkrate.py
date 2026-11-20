"""A second script that imports the module and calls payout()."""
import milkrate
import milkrate as mr
from milkrate import payout

print("import milkrate            ->", milkrate.payout(10, 3.5, 8.5))
print("import milkrate as mr      ->", mr.rate_per_litre(4.2, 8.7))
print("from milkrate import payout ->", payout(8.5, 4.2, 8.7))
print("__name__ inside milkrate   =", milkrate.__name__, "| __name__ here =", __name__)
