# see README.doc

import re
import math


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [(item.strip()) for item in local_list]
        return return_list


def split_input(puzzle_input):
    ''' Puzzle input is split into 3 parts: rules, my ticket, other tickets
        Returns split input plus bonus:
        - rules dict, one_rule set with all rule ranges, my_ticket and nearby_ticket list
        All int values as int
    '''
    split1 = puzzle_input.index('your ticket:')
    split2 = puzzle_input.index('nearby tickets:')
    rules, one_rule = understand_rules(puzzle_input[:split1-1])
    my_ticket = [int(number) for number in puzzle_input[split1+1].split(',')]
    nearby_tickets = [[int(number) for number in line.split(',')]
                      for line in puzzle_input[split2+1:]]
    return (rules, one_rule, my_ticket, nearby_tickets)


def understand_rules(rules_list):
    ''' Interpret and split rule lines
        Returns dict {field_name: [range tuples]} for rules
        and set with all rule ranges combined for validity check
    '''
    rules = dict()
    union = set()
    for line in rules_list:
        field_name, segments = [item.strip() for item in line.split(':')]
        rules[field_name] = list()
        for segment in segments.split('or'):
            min_range, max_range = [int(num)
                                    for num in segment.strip().split('-')]
            rules[field_name].append((min_range, max_range))
            union.update(range(min_range, max_range+1))
    return (rules, union)


def scan_ticket_errors(tickets, one_rule):
    ''' Star1: Checks all nearby tickets for validity (in combined range)
        Returns error rate and list of valid tickets
    '''
    error_rate = 0
    valid_tickets = list()
    for ticket in tickets:
        if (all(n in one_rule for n in ticket)):
            valid_tickets.append(ticket)
        else:
            for n in ticket:
                if (not n in one_rule):
                    error_rate += n
    return error_rate, valid_tickets


def check_col_for_rules(rules, col_numbers):
    ''' Checks single column from nearby tickets against all rules
        Returns all valid rule field_names as list
    '''
    valid_rules = list()
    for field in rules.keys():
        full_range = set()
        full_range.update(*[range(min_range, max_range+1)
                            for min_range, max_range in rules[field]])
        if (all(number in full_range for number in col_numbers)):
            valid_rules.append(field)
    return valid_rules


def clean_field_map(field_map):
    ''' After checking all columns for matching field_names, 
        filter by columns with only one matching rule and repeat.
        Sorting would probably be more efficient...
    '''
    done = False
    while (done == False):
        done = True
        for idx, names in field_map.items():
            if (len(names) == 1):
                name = names[0]
                for sub_idx, sub_names in field_map.items():
                    if (sub_idx == idx):
                        continue
                    if (name in sub_names):
                        done = False
                        field_map[sub_idx].remove(name)
    return field_map


def get_departure_fields(rules, tickets):
    ''' Get matching rule names for all nearby ticket columns.
        Clean resulting field_map to single name per column.
        Filter for field_names with "departure"
        Returns list of column indexes for "departure" fields
    '''
    field_count = len(tickets[0])
    field_map = dict()
    departure_fields = list()
    for idx in range(field_count):
        orthocut = [t[idx] for t in tickets]
        field_map[idx] = check_col_for_rules(rules, orthocut)
    field_map = clean_field_map(field_map)
    departure_fields = [
        i for i, n in field_map.items() if ('departure' in n[0])]
    return departure_fields


def main():
    #daily_list = read_daily_input('input_test2.txt')
    daily_list = read_daily_input('input16.txt')
    rules, one_rule, ticket, nearby_tickets = split_input(daily_list)
    star1, star2_tickets = scan_ticket_errors(nearby_tickets, one_rule)
    print(f"Ticket error rate: {star1}")
    departure_fields = [ticket[i]
                        for i in get_departure_fields(rules, star2_tickets)]
    print(f"My departure fields' product: {math.prod(departure_fields)}")


if __name__ == "__main__":
    main()
