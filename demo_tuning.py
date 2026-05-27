"""Derive m and k from a target false-positive rate, then measure.

Pick the expected number of items (n) and the target false-positive
rate (p). The classmethod computes the optimal bit count and hash
count from the formulas in section 2 of the post. We then insert n
items, query a fresh batch of strangers, and compare the measured
rate against the theoretical `(1 - e^(-kn/m))^k`.
"""

import math

from bloom import BloomFilter

N = 10_000
P = 0.01
STRANGERS = 10_000


def main() -> None:
    bf = BloomFilter.for_capacity(N, P)
    print(f"target FPR p = {P}")
    print(f"derived m = {bf.m} bits ({bf.m / 8 / 1024:.2f} KB), k = {bf.k}")

    for i in range(N):
        bf.add(f"member-{i}")

    false_positives = sum(
        1 for j in range(STRANGERS) if bf.contains(f"stranger-{j}")
    )
    measured = false_positives / STRANGERS
    predicted = (1 - math.exp(-bf.k * N / bf.m)) ** bf.k

    print(f"measured FPR over {STRANGERS} strangers: {measured:.4%}")
    print(f"predicted FPR (1 - e^(-kn/m))^k:         {predicted:.4%}")


if __name__ == "__main__":
    main()
