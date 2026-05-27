"""Put the filter under a real load: a one-million-URL blocklist.

Synthesize 1,000,000 distinct URLs as the "blocked" set, build a
Bloom filter sized for a 1% false-positive rate, and measure two
things:

  1. The actual false-positive rate over 100k URLs the filter has
     never seen, compared to the theoretical prediction.
  2. The memory cost of the filter compared to a plain Python set
     holding the same URLs.

The URLs are synthetic on purpose so the numbers are reproducible
across machines. Swap in a real blocklist by replacing `blocked_url`
and `stranger_url` with your data source.
"""

import math
import sys
import time

from bloom import BloomFilter

N_BLOCKED = 1_000_000
N_STRANGERS = 100_000
P_TARGET = 0.01


def blocked_url(i: int) -> str:
    return f"https://malicious-{i}.example/path/{i * 7919}"


def stranger_url(j: int) -> str:
    return f"https://safe-{j}.example/path/{j * 104729}"


def measure_set_bytes(urls: list[str]) -> int:
    s = set(urls)
    # Approximate: hash-table overhead plus the strings themselves.
    return sys.getsizeof(s) + sum(sys.getsizeof(u) for u in urls)


def main() -> None:
    print(f"building bloom filter for n={N_BLOCKED:,}, target p={P_TARGET}")
    bf = BloomFilter.for_capacity(N_BLOCKED, P_TARGET)
    print(
        f"  derived m = {bf.m:,} bits ({len(bf.bits) / 1024 / 1024:.2f} MB), "
        f"k = {bf.k}"
    )

    t0 = time.perf_counter()
    for i in range(N_BLOCKED):
        bf.add(blocked_url(i))
    print(f"  inserts: {time.perf_counter() - t0:.2f}s")

    t0 = time.perf_counter()
    false_positives = sum(
        1 for j in range(N_STRANGERS) if bf.contains(stranger_url(j))
    )
    print(f"  lookups: {time.perf_counter() - t0:.2f}s")

    measured = false_positives / N_STRANGERS
    predicted = (1 - math.exp(-bf.k * N_BLOCKED / bf.m)) ** bf.k
    print()
    print(f"false positives: {false_positives} / {N_STRANGERS:,}")
    print(f"  measured FPR:  {measured:.4%}")
    print(f"  predicted FPR: {predicted:.4%}")

    print()
    print("memory cost of holding the same URLs:")
    set_bytes = measure_set_bytes([blocked_url(i) for i in range(N_BLOCKED)])
    print(f"  python set:    {set_bytes / 1024 / 1024:.2f} MB")
    print(f"  bloom filter:  {len(bf.bits) / 1024 / 1024:.2f} MB")
    print(f"  ratio:         {set_bytes / len(bf.bits):.0f}x")


if __name__ == "__main__":
    main()
