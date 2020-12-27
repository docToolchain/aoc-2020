#!/usr/bin/env python

import doctest
import logging


def load_input():
    data = list()
    section = 0
    ranges = dict()
    my_ticket = None
    nearby_tickets = list()

    with open('input.txt') as fd:
        for line in fd:
            value = line.strip()
            if not value:
                pass
            elif value == "your ticket:":
                section += 1
            elif value == "nearby tickets:":
                section += 1
            elif section == 0:
                d = list()
                a = list(map(lambda x: x.strip(), value.split(":")))
                b = list(map(lambda x: x.strip(), a[1].split("or")))
                for el in b:
                    c = el.split('-')
                    d.append([int(i) for i in c])
                ranges[a[0]] = d
            elif section == 1:
                my_ticket = list(map(int, value.split(",")))
            elif section == 2:
                a = list(map(int, value.split(",")))
                nearby_tickets.append(a)
            else:
                print("OH NO!")

    return ranges, my_ticket, nearby_tickets


def calc_valid_keys(values, ranges):
    valid_keys = list()
    for key, rnge in ranges.items():
        valid_count = 0
        for value in values:
            for lower, upper in rnge:
                if lower <= value and value <= upper:
                    valid_count += 1
                    break
        if valid_count == len(values):
            valid_keys.append(key)
    return valid_keys


def is_valid(value, ranges):
    for rnge in ranges.values():
        for lower, upper in rnge:
            if lower <= value and value <= upper:
                return True
    return False


def main():
    ranges, my_ticket, nearby_tickets = load_input()

    # Part 1
    result = 0
    valid_tickets = list()

    for nearby in nearby_tickets:
        valid_ticket = True
        for value in nearby:
            valid = is_valid(value, ranges)
            if not valid:
                valid_ticket = False
                result += value
        if valid_ticket:
            valid_tickets.append(nearby)
    print("Part1: ", result)

    # Part 2
    mapping = dict()
    for i in range(len(ranges)):
        row = [ticket[i] for ticket in valid_tickets]
        keys = calc_valid_keys(row, ranges)
        mapping[i] = keys

    result_dict = dict()
    # Assign each name to a distinct position
    while mapping:
        del_values = list()
        del_keys = list()

        # Find distinct names
        for key, values in mapping.items():
            if len(values) == 1:
                del_values.append(values[0])
                result_dict[values[0]] = key

        # Remove already assigned names
        for key, values in mapping.items():
            for del_value in del_values:
                if del_value in values:
                    del mapping[key][mapping[key].index(del_value)]

        # Clean up source dictionary
        for key, values in mapping.items():
            if not values:
                del_keys.append(key)
        for key in del_keys:
            del mapping[key]

    # Calculate result by multiplying "departure" values
    result = 1
    for key, value in result_dict.items():
        if "departure" in key:
            result *= my_ticket[value]

    print("Part2: ", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
