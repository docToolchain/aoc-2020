#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 10"""

# stdlib imports
from collections import Counter
import functools
import math
from typing import List

# 3rd party lib imports

# own stuff
import utils


def prepare_input(input: str) -> List[int]:
    input_parsed = list(sorted([int(elem) for elem in input.strip().split("\n")]))
    return [0] + input_parsed + [input_parsed[-1] + 3]


def get_deltas(data: List) -> List:
    return [a - b for a, b in zip(data[1:], data[:-1])]


def part1(joltages: List[int]) -> int:
    """return compute histogram of deltas. return count(delta=3) * count(delta=1)"""

    deltas = get_deltas(joltages)
    hist = Counter(deltas)

    return hist[1] * hist[3]


def count_arrangements_bf(joltages: List[int]) -> int:
    """recursive brute force: works (for the test cases), but takes way too
    long for the "real" thing.
    """

    @functools.lru_cache
    def recursion(start):
        if start == len(joltages) - 1:
            return 1

        n = 0
        for i in range(start + 1, len(joltages)):
            if joltages[i] - joltages[start] > 3:
                break

            n += recursion(i)

        return n

    return recursion(0)


def get_partitions(joltages: List[int]) -> List[List[int]]:
    """partition the joltages: get contiguous items that have only a delta of 1 to
    their neighbors, e.g.

    [0, 1, 2, 3, 4, 7, 8, 9] ==> [[1, 2, 3], [8]]
    """
    partitions = []
    lower = 0
    while lower < len(joltages) - 2:
        for i in range(lower + 1, len(joltages) - 1):
            if joltages[i] - joltages[i-1] == joltages[i+1] - joltages[i] == 1:
                continue

            break

        if i > lower + 1:
            partitions.append(joltages[lower+1:i])
        lower = i

    return partitions


def count_arrangements_partition(joltages: List[int]) -> int:
    """partition the joltage list: joltages with delta = 3 to a neighbor can't be
    left out, so get partitions of joltages with a delta of 1 to their neighbors
    (delta = 2 does not exist).
    Compute the number of combinations within a partition:
    - each partition is at most 3 items long, so within each partition only 2 can
      be removed at a time
    - take none out: 1
    - take one out: n, i.e. len(part)
    - take two out: draw k from n without replacement, i.e. math.comb(n, k)

    The total number of combinations is given by the product of the number of
    combinations of the partitions.
    """
    partitions = get_partitions(joltages)
    combos = []
    for part in partitions:
        combos.append(1 + len(part) + math.comb(len(part), 2))

    return math.prod(combos)


def main() -> None:
    joltages = prepare_input(utils.get_input(__file__))

    # part 1
    n_part1 = part1(joltages)
    print(f"part 1: {n_part1}")

    # part 2
    n_arrangements_bf = count_arrangements_bf(joltages)
    print(f"part 2 (brute force): {n_arrangements_bf}")

    n_arrangements = count_arrangements_partition(joltages)
    print(f"part 2:               {n_arrangements}")


if __name__ == "__main__":
    main()
