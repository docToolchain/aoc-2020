#!/usr/bin/env python

import doctest
import logging
from collections import deque


def load_input():
    data = list()
    with open('input.txt') as fd:
        data = fd.read()
        data = list(map(int, data.strip().split(',')))
    return data


def execute(start, steps):
    hist = dict()
    last_val = None

    for i, value in enumerate(start):
        hist[value] = [deque([0, i + 1]), True]
        last_val = value

    for i in range(len(start) + 1, steps + 1):
        if hist[last_val][1]:
            last_val = 0
        else:
            last_val = hist[last_val][0][1] - hist[last_val][0][0]

        if last_val in hist:
            hist[last_val][1] = False
            hist[last_val][0].popleft()
            hist[last_val][0].append(i)
        else:
            values = [deque([0, i]), True]
            hist[last_val] = values

    return last_val


def main():
    data = load_input()
    print("Part1: ", execute(data, 2020))
    print("Part2: ", execute(data, 30000000))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
