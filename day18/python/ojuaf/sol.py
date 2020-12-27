#!/usr/bin/env python

import doctest
import logging
import math as m
import re


def load_input():
    data = list()
    with open('input.txt') as fd:
        for line in fd:
            value = line.strip()
            data.append(value)
    return data


def calc_substr_part1(substr):
        a = substr.split('+')
        b = list()
        for el in a:
            b.append(list(map(int, el.split('*'))))

        value = 0
        for i in b:
            for k, j in enumerate(i):
                if k == 0:
                    value += j
                else:
                    value *= j

        return str(value)


def calc_substr_part2(substr):
        a = substr.split('*')
        b = list()
        for el in a:
            b.append(list(map(int, el.split('+'))))

        value = 0
        temp = list()
        for i in b:
            temp.append(sum(i))

        value = m.prod(temp)
        return str(value)


def sol(data, calc):
    data = load_input()
    regex = ".*\(([0-9\*\+\s]+)\).*"
    pattern = re.compile(regex)

    result = 0
    for line in data:
        while True:
            match = pattern.search(line)
            if not match:
                break
            substr = match.group(1)
            value = calc(substr)
            line = line.replace('(' + substr  + ')', value)

        result += int(calc(line))
    return result


def main():
    data = load_input()

    result = sol(data, calc_substr_part1)
    print("Part1:", result)

    result = sol(data, calc_substr_part2)
    print("Part2:", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
