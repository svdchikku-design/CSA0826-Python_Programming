"""Q7 F extension: the loop's '999 additions' hides that the numbers themselves grow - fast doubling for very large n."""
import time

def ways_loop(n):
    prev, cur = 1, 1
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
    return cur

def ways_doubling(n):
    """ways(n) = Fib(n+1) by fast doubling: Fib(2k) = F(k)(2F(k+1)-F(k)), Fib(2k+1) = F(k)^2 + F(k+1)^2. O(log n) big multiplications."""
    a, b = 0, 1                                   # Fib(0), Fib(1)
    for bit in bin(n + 1)[2:]:                    # bits of the index, most significant first
        c = a * (2 * b - a)                       # Fib(2k)
        d = a * a + b * b                         # Fib(2k+1)
        a, b = (d, c + d) if bit == "1" else (c, d)
    return a

assert all(ways_loop(n) == ways_doubling(n) for n in range(1, 500))
print("fast doubling equals the loop for n = 1..499: True")
print(f"{'n':>9} | {'loop (ms)':>11} {'fast doubling (ms)':>19} {'ratio':>8} | same answer?")
for n in (1000, 10_000, 100_000, 300_000):
    t0 = time.perf_counter(); a = ways_loop(n); tl = time.perf_counter() - t0
    t0 = time.perf_counter(); b = ways_doubling(n); td = time.perf_counter() - t0
    print(f"{n:>9} | {tl * 1e3:>11.3f} {td * 1e3:>19.3f} {tl / td:>7.1f}x | {a == b}")
t0 = time.perf_counter(); b = ways_doubling(1_000_000); td = time.perf_counter() - t0
print(f"{1_000_000:>9} | {'(not run)':>11} {td * 1e3:>19.3f}         | bit length of the answer: {b.bit_length()}")
