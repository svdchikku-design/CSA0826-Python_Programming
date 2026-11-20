"""Task 2 - interactive-mode exploration (transcript produced by a real interpreter)."""
from session import run_session
run_session([
 'type(10)', 'type(10.0)', 'type("10")', 'type(True)', 'type([10, 8.5])',
 '7 / 2', '7 // 2', '7 % 2', '-7 // 2', '-7 % 2',
 '0.1 + 0.2', '0.1 + 0.2 == 0.3', 'abs((0.1 + 0.2) - 0.3) < 1e-9',
 'True + True', 'isinstance(True, int)',
 '"10" + 10', '"10" * 2', 'int("10") + 10',
 'sum([0.1] * 10)', 'total = 0.0', 'for _ in range(10): total += 0.1', '', 'total', 'total == 1.0',
 'round(2.675, 2)', 'round(0.125, 2)',
 'from decimal import Decimal',
 'Decimal("0.1") + Decimal("0.2")', 'Decimal(0.1)',
 'Decimal("33.40") * 3', '1000 * 33.40',
])
