#!/usr/bin/env python

import doctest
import logging
import math as m
import re
from networkx import DiGraph
import copy
import itertools as it
import numpy as np

def load_input_part1():
    data = list()
    with open('input.txt') as fd:
        for i, line in enumerate(fd):
            value = line.strip()
            for j, char in enumerate(value):
                if char == '#':
                    data.append((i, j, 0))
    return data


def load_input_part2():
    data = list()
    with open('input.txt') as fd:
        for i, line in enumerate(fd):
            value = line.strip()
            for j, char in enumerate(value):
                if char == '#':
                    data.append((i, j, 0, 0))
    return data


def get_mins(array, dim):
    mins = list()
    for i in range(dim):
        mins.append(min(a[i] for a in array))
    return tuple(mins)


def get_maxs(array, dim):
    maxs = list()
    for i in range(dim):
        maxs.append(max(a[i] for a in array))
    return tuple(maxs)


def part1():
    print("Part 1")
    data = load_input_part1()

    n_off = [(l, m, n) for l in range(-1, 2) for m in range(-1, 2) for n in range(-1, 2)]
    n_off.remove((0, 0, 0))

    for cycle in range(6):
        next_data = list()
        x_min, y_min, z_min = get_mins(data, 3)
        x_max, y_max, z_max = get_maxs(data, 3)

        for i in range(x_min-1, x_max+2):
            for j in range(y_min-1, y_max+2):
                for k in range(z_min-1, z_max+2):
                    count = 0
                    neighbors = [(i+l, j+m, k+n) for l, m, n in n_off]
                    for neighbor in neighbors:
                        if neighbor in data:
                            count += 1
                    if (i, j, k) in data and (count == 3 or count == 2):
                        next_data.append((i, j, k))
                    elif (i, j, k) not in data and count == 3:
                        next_data.append((i, j, k))
                    else:
                        pass
        print("Round", cycle + 1)
        data = next_data

    return len(data)


def part2():
    print("Part 2")
    data = load_input_part2()

    n_off = [(l, m, n, o) for l in range(-1, 2) for m in range(-1, 2) for n in range(-1, 2) for o in range(-1, 2)]
    n_off.remove((0, 0, 0, 0))

    for cycle in range(6):
        next_data = list()
        x_min, y_min, z_min, w_min = get_mins(data, 4)
        x_max, y_max, z_max, w_max = get_maxs(data, 4)

        for i in range(x_min-1, x_max+2):
            for j in range(y_min-1, y_max+2):
                for k in range(z_min-1, z_max+2):
                    for u in range(w_min-1, w_max+2):
                        count = 0
                        neighbors = [(i+l, j+m, k+n, u+o) for l, m, n, o in n_off]
                        for neighbor in neighbors:
                            if neighbor in data:
                                count += 1
                                if count > 3:
                                    break

                        if (i, j, k, u) in data and (count == 3 or count == 2):
                            next_data.append((i, j, k, u))
                        elif (i, j, k, u) not in data and count == 3:
                            next_data.append((i, j, k, u))
                        else:
                            pass
        print("Round", cycle + 1)
        data = next_data

    return len(data)


def main():
    result = part1()
    print("Solution Part1: ", result)

    print("")

    result = part2()
    print("Solution Part2:", result)


def print_data_part1(data):
    x_min, y_min, z_min = get_mins(data)
    x_max, y_max, z_max = get_maxs(data)

    for k in range(z_min, z_max+1):
        print("")
        print(f"z={k}")
        column = ""
        for i in range(x_min, x_max+1):
            row = ""
            for j in range(y_min, y_max+1):
                if (i, j, k) in data:
                    row += "#"
                else:
                    row += "."
            print(row)

def print_data_part2(data):
    x_min, y_min, z_min, w_min = get_mins(data)
    x_max, y_max, z_max, w_max = get_maxs(data)

    for k in range(z_min, z_max+1):
        for u in range(w_min, w_max+1):
            print("")
            print(f"z={k}, w={u}")
            for i in range(x_min, x_max+1):
                row = ""
                for j in range(y_min, y_max+1):
                    if (i, j, k, u) in data:
                        row += "#"
                    else:
                        row += "."
                print(row)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
