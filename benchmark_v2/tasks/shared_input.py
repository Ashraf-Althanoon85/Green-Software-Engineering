"""
shared_input.py — provides deterministic inputs that are identical
across all three versions of every task.

Each task imports `get_input()` from this module to ensure the same
workload is processed by Clean / Medium / Bad versions.
"""

import random


def get_int_array(task_id: int, n: int, seed_offset: int = 0) -> list:
    """Return a deterministic list of n integers for task_id."""
    rng = random.Random(task_id * 1000 + seed_offset)
    return [rng.randint(0, 1_000_000) for _ in range(n)]


def get_float_array(task_id: int, n: int, seed_offset: int = 0) -> list:
    rng = random.Random(task_id * 1000 + seed_offset)
    return [rng.random() * 1000.0 for _ in range(n)]


def get_string_array(task_id: int, n: int, max_len: int = 30) -> list:
    rng = random.Random(task_id * 1000)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    out = []
    for _ in range(n):
        ln = rng.randint(3, max_len)
        out.append("".join(rng.choices(alphabet, k=ln)))
    return out


def get_int_pairs(task_id: int, n: int, max_val: int = 1_000_000) -> list:
    rng = random.Random(task_id * 1000)
    return [(rng.randint(1, max_val), rng.randint(1, max_val)) for _ in range(n)]
