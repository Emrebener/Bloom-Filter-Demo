"""A Bloom filter, the smallest form that still demonstrates the idea.

This first version uses a single hash function so we can watch the
false-positive rate climb as soon as a few items collide. Section 2 of
the companion post adds k hashes and the tuning math; section 3 puts it
under a million-URL load.
"""

import hashlib


class BloomFilter:
    def __init__(self, m_bits: int):
        # m is the size of the bit array, in bits. Memory cost is m/8 bytes.
        self.m = m_bits
        self.bits = bytearray(m_bits // 8 + 1)

    def _index(self, item: str) -> int:
        # Single hash for now: take sha256 of the item, treat the first
        # eight bytes as a 64-bit integer, fold into [0, m) with modulo.
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h = int.from_bytes(digest[:8], "big")
        return h % self.m

    def add(self, item: str) -> None:
        i = self._index(item)
        self.bits[i // 8] |= 1 << (i % 8)

    def contains(self, item: str) -> bool:
        i = self._index(item)
        return bool(self.bits[i // 8] & (1 << (i % 8)))
