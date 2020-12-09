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


def main():
    data = load_input()
    preamble_size = 25
    result = 0
    invalid_pos = 0

    for i in range(len(data)):
        pos = i + preamble_size
        preamble = data[i:pos]
        value = data[pos]
        perm = it.permutations(preamble, 2)
        sums = list(map(sum, perm))
        if value not in sums:
            result = value
            invalid_pos = pos
            break
    print("Part1: ", result)

    for i in range(invalid_pos):
        seq_sum = data[i]
        for j in range(i + 1, invalid_pos):
            seq_sum += data[j]
            if seq_sum > result:
                break
            elif seq_sum == result:
                result = max(data[i:j+1]) + min(data[i:j+1])
            else:
                pass
    print("Part2: ", result)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
