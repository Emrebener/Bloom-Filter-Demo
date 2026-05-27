"""A Bloom filter, the smallest form that still demonstrates the idea.

This version supports k hash functions via the double-hashing trick
(Kirsch & Mitzenmacher, 2006): one cryptographic hash is split into
two halves, and the k indices are derived as `h1 + i*h2 mod m`. It
also exposes `for_capacity(n, p)` which computes the optimal m and k
for a given expected item count n and target false-positive rate p.
"""

import hashlib
import math


class BloomFilter:
    def __init__(self, m_bits: int, k: int):
        # m = size of the bit array (bits); k = number of hash positions per item.
        self.m = m_bits
        self.k = k
        self.bits = bytearray(m_bits // 8 + 1)

    @classmethod
    def for_capacity(cls, n: int, p: float) -> "BloomFilter":
        # Optimal bit count and hash count for n expected items and
        # target false-positive rate p:
        #   m = -(n * ln p) / (ln 2)^2
        #   k = (m / n) * ln 2
        m = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2))
        k = max(1, round((m / n) * math.log(2)))
        return cls(m, k)

    def _indices(self, item: str):
        # Double-hashing: derive k positions from two halves of one sha256 digest.
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:16], "big")
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, item: str) -> None:
        for i in self._indices(item):
            self.bits[i // 8] |= 1 << (i % 8)

    def contains(self, item: str) -> bool:
        return all(
            self.bits[i // 8] & (1 << (i % 8)) for i in self._indices(item)
        )
