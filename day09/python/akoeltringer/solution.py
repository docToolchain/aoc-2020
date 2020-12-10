#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 09"""

# stdlib imports
import itertools
from typing import List

# 3rd party lib imports

# own stuff
import utils


def parse_input(xmas_nums_raw: str) -> List[int]:
    return [int(num) for num in xmas_nums_raw.strip().split("\n")]


def find_first_invalid_xmas_num(xmas_nums: List[int], prev: int) -> int:
    """validate the numbers: each number (starting at index `prev`) must be
    the sum of to of the `prev` numbers. Return the first number that does not
    match this condition.
    Raise ValueError if all numbers are valid.
    """
    for i in range(prev, len(xmas_nums)):
        subset = xmas_nums[(i-prev):i]
        if xmas_nums[i] not in [sum(x) for x in itertools.combinations(subset, 2)]:
            return xmas_nums[i]

    raise ValueError("no invalid nums found")


def find_encryption_weakness(xmas_nums: List[int], first_invalid_num: int) -> int:
    """find a contiguous range of numbers (at least 2) that sum to the invalid num.
    return the sum of the first and last of these numbers.
    """
    # slide through the list
    for i in range(len(xmas_nums) - 1):
        # expand the window
        for j in range(i+1, len(xmas_nums) - 1):
            contiguous_range = xmas_nums[i:(j+1)]
            if sum(contiguous_range) > first_invalid_num:
                break

            if sum(contiguous_range) == first_invalid_num:
                return min(contiguous_range) + max(contiguous_range)

    raise ValueError("no range found")


def main() -> None:
    xmas_nums = parse_input(utils.get_input(__file__))

    # part 1
    first_invalid_num = find_first_invalid_xmas_num(xmas_nums, 25)
    print(f"part 1: first invalid num: {first_invalid_num}")

    # part 2
    enc_weakness = find_encryption_weakness(xmas_nums, first_invalid_num)
    print(f"part 2: encryption weakness: {enc_weakness}")


if __name__ == "__main__":
    main()
