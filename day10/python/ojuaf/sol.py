#!/usr/bin/env python

import doctest
import logging
import math as m
import re
from networkx import DiGraph
import copy
import itertools as it


def load_input():
    data = list()
    with open('input.txt') as fd:
        for line in fd:
            value = int(line.strip())
            data.append(value)
    return data


def part1(data):
    value = 0
    ones = 0
    threes = 0

    end = max(data) + 3
    data.append(end)
    while True:
        for i in range(1, 4):
            value += 1
            if value in data:
                if i == 1:
                    ones += 1
                if i == 3:
                    threes += 1
                break
        if value == end:
            break

    return ones*threes


def part2(data):
    combinations = dict()
    end = max(data) + 3

    data.append(0)
    data.append(end)

    combinations[end] = 1
    data.sort(reverse = True)

    for value in data:
        if value == end:
            continue
        sums = 0
        for i in range(1, 4):
            next_value = value + i
            if next_value in data:
                sums += combinations[next_value]
        combinations[value] = sums

    return combinations[0]


def main():
    data = load_input()

    result = part1(data.copy())
    print("Part1: ", result)

    result = part2(data.copy())
    print("Part2: ", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
