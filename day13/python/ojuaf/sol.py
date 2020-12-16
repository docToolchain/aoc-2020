#!/usr/bin/env python

import doctest
import logging
import math as m

def load_input():
    data = list()
    with open('input.txt') as fd:
        lines = fd.readlines()
        time = int(lines[0].strip())
        freqs = lines[1].strip().split(',')
        ids = list()
        offsets = list()
        count = 0
        for freq in freqs:
            if freq != 'x':
                ids.append(int(freq))
                offsets.append(count)
            count += 1
    return time, ids, offsets


def get_n(prime_orig, prime, offset):
    i = 0
    while True:
        if (prime_orig*i + offset) % prime == 0:
            return i
        i += 1


def main():
    start, ids, offsets = load_input()

    # Part 1
    time = start
    result = None
    stop = False
    while True:
        for bus_id in ids:
            if time % bus_id == 0:
                result = (time - start) * bus_id
                break
        if result:
            break
        time += 1

    print("Part 1:", result)

    # Part 2
    value = ids[0]
    k_off = offsets[0]

    for bus_id, offset in zip(ids[1:], offsets[1:]):
        n = get_n(value, bus_id, offset + k_off)
        k_off += n*value
        value = bus_id*value

    result = k_off
    print("Part 2:", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
