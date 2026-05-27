"""Watch the false-positive rate climb with a single-hash Bloom filter.

We seed the filter with N known items, then query M unseen items and
count how many the filter wrongly reports as members. With one hash,
the rate grows roughly as N/m — much worse than the optimal k-hash
version we build in section 2.
"""

from bloom import BloomFilter

M_BITS = 128
N_INSERTED = 20
M_QUERIED = 10_000


def main() -> None:
    bf = BloomFilter(M_BITS, k=1)

    for i in range(N_INSERTED):
        bf.add(f"member-{i}")

    false_positives = sum(
        1 for j in range(M_QUERIED) if bf.contains(f"stranger-{j}")
    )

    rate = false_positives / M_QUERIED
    print(f"m = {M_BITS} bits, inserted = {N_INSERTED} items")
    print(f"queried {M_QUERIED} strangers, {false_positives} false positives")
    print(f"measured false-positive rate: {rate:.3%}")
    print(f"naive expectation (N / m):    {N_INSERTED / M_BITS:.3%}")


if __name__ == "__main__":
    main()
