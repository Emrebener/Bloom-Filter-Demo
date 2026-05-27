# Bloom-Filter-Demo

A minimal, working Bloom filter in ~40 lines of Python, built as the
companion code for the blog post
[Understanding Bloom Filters](https://emrebener.com/topics/systems-and-infrastructure/understanding-bloom-filters).

It is a study artifact, not a library. No dependencies, no tests, no
packaging — three scripts that you can read top to bottom.

## What's here

| File | What it shows |
| --- | --- |
| `bloom.py` | The Bloom filter class. ~40 lines. One hash call per item via the double-hashing trick; a `for_capacity(n, p)` constructor that derives `m` and `k` from the tuning formulas. |
| `demo_one_hash.py` | The smallest possible setup: one hash, 128 bits, 20 items. Shows the false-positive rate climbing into double digits. |
| `demo_tuning.py` | Drives the tuned constructor at its design point (n=10k, p=0.01) and compares the measured rate to the theoretical prediction. |
| `demo_blocklist.py` | The main attraction: one million URLs in a Bloom filter sized for a 1% false-positive rate, with a memory comparison against a plain Python `set`. |

## Running

```
python3 demo_one_hash.py
python3 demo_tuning.py
python3 demo_blocklist.py
```

Requires Python 3.9+. No `pip install` step. The blocklist demo takes
~8 seconds on a modern laptop.
