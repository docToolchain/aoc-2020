#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 15"""

# stdlib imports
from typing import List

# 3rd party lib imports

# own stuff


def compute_sequence(starting_numbers: List[int], n_elems: int) -> int:
    """compute the sequence according to the rules. Return the nth element."""
    elems = list(reversed(starting_numbers))

    for _ in range(len(starting_numbers), n_elems):
        try:
            idx_before = elems.index(elems[0], 1)
        except ValueError:
            elems = [0] + elems
        else:
            elems = [idx_before] + elems

    return elems[0]


def compute_sequence_dict(starting_numbers: List[int], n_elems: int) -> int:
    """compute the sequence according to the rules. Use a dictionary for lookup.
    Return the nth element.

    This version is 50x faster for the "2020" versions:
    >>> %timeit compute_sequence([0, 3, 6], 2020)
    8.01 ms ± 447 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    >>> %timeit compute_sequence_dict([0, 3, 6], 2020)
    142 µs ± 160 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    elems = {num: i for i, num in enumerate(starting_numbers[:-1])}
    next_num = starting_numbers[-1]

    for i in range(len(starting_numbers) - 1, n_elems - 1):

        if next_num in elems:
            idx_old = elems[next_num]
            elems[next_num] = i
            next_num = i - idx_old
        else:
            elems[next_num] = i
            next_num = 0

    return next_num


def main() -> None:
    starting_numbers = [18, 8, 0, 5, 4, 1, 20]

    # part 1
    num2020 = compute_sequence(starting_numbers, 2020)
    print(f"part 1: {num2020}")

    # part 2
    num_30m = compute_sequence_dict(starting_numbers, 30_000_000)
    print(f"part 1: {num_30m}")


if __name__ == "__main__":
    main()
