import time
def calls_per_second():
    calls = 0
    def f(n):
        nonlocal calls
        calls += 1
        if n <= 1: return 1
        return f(n - 1) + f(n - 2)
    t0 = time.perf_counter(); f(27); dt = time.perf_counter() - t0
    return calls / dt
