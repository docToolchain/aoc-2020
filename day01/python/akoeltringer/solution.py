#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 01"""

# stdlib imports
import itertools
import math
from typing import List

# 3rd party lib imports

# own stuff
import utils


def get_input_parsed() -> List[int]:
    """get the input from the website and return it parsed in a suitable format"""
    return [int(elem) for elem in utils.get_input(__file__).strip().split("\n")]


def get_prod_2020(accounting_entries: List[int], n_elems: int = 2) -> int:
    """return the product of the numbers, which sum is 2020"""
    for elems in itertools.combinations_with_replacement(accounting_entries, n_elems):
        if sum(elems) == 2020:
            return math.prod(elems)

    raise RuntimeError("No numbers that match that sum == 2020")


def main() -> None:
    """Main entrypoint"""
    accounting_entries = get_input_parsed()

    # Part 1
    print(f"The prod2020 (2 nums) is: {get_prod_2020(accounting_entries, 2)}")

    # Part 2
    print(f"The prod2020 (3 nums) is: {get_prod_2020(accounting_entries, 3)}")


if __name__ == "__main__":
    main()
