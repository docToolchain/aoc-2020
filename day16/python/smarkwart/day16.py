import sys
import re

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = input_file.readlines()
    return data_list

def get_ticket_data_list_from_ticket(ticket):
    ticket_data = list(map(int, ticket.split(',')))
    return ticket_data

def field_is_valid(field, rules):
    is_valid = False
    for rule_name, data in rules.items():
        if int(data['min_lower']) <= field and field <= int(data['max_lower']):
            is_valid = True
        elif int(data['min_upper']) <= field and field <= int(data['max_upper']):
            is_valid = True
    return is_valid

def verify_ticket(ticket, rules):
    is_valid = True
    invalid_sum = 0
    for field in ticket:
        if not field_is_valid(field, rules):
            invalid_sum += field
            is_valid = False
    return invalid_sum, is_valid

def calculate_scanning_error_rate(tickets, rules):
    scanning_error_rate = 0
    valid_tickets = []
    for ticket in tickets:
        ticket_error, ticket_valid = verify_ticket(get_ticket_data_list_from_ticket(ticket), rules)
        scanning_error_rate += ticket_error
        if ticket_valid:
            valid_tickets.append(ticket)
    return scanning_error_rate, valid_tickets

def parse_rules(rules_input):
    rules_dict = {}
    for rule_line in rules_input:
        rule_splitted = rule_line.split(':')
        regex_match = re.match(r"(?P<min_lower>\d+)-(?P<max_lower>\d+) or (?P<min_upper>\d+)-(?P<max_upper>\d+)",rule_splitted[1].strip())
        if regex_match:
            rules_dict[rule_splitted[0]] = regex_match.groupdict()
    return rules_dict

def get_rule_position_pairs(tickets, rules):
    rule_position_pairs = {}
    while len(rules) > 0:
        rule_matches, rule_names, position_id = identify_single_match(tickets, rules)
        if rule_matches == 1:
            del rules[rule_names[0]]
            rule_position_pairs[rule_names[0]] = position_id
        else:
            break
    return rule_position_pairs

def identify_single_match(tickets, rules):
    rule_matches = 0
    rule_names = []
    position_id = -1
    positions_on_ticket = len(get_ticket_data_list_from_ticket(tickets[0]))
    for position_id in range(0,positions_on_ticket):
        rule_matches, rule_names = get_number_of_rules_matching_postition(tickets, position_id, rules)
        if rule_matches == 1:
            break
    return rule_matches, rule_names, position_id

def get_number_of_rules_matching_postition(tickets, position_id, rules):
    rule_matches = 0
    rule_names = []
    for rule_name, data in rules.items():
        rule_matches_position = True
        for ticket in tickets:
            element = get_ticket_data_list_from_ticket(ticket)[position_id]
            if (element < int(data['min_lower']) or 
                (int(data['max_lower']) < element and element < int(data['min_upper'])) or
                int(data['max_upper']) < element):
                rule_matches_position = False
                break
        if rule_matches_position: 
            rule_matches += 1
            rule_names.append(rule_name)
    return rule_matches, rule_names

def calculate_star2_puzzle_answer(rule_position_pairs, my_ticket, data_to_lookup):
    solution = 1

    for rule, position in rule_position_pairs.items():
        if rule.startswith(data_to_lookup):
            solution *= my_ticket[position]

    return solution


tickets_input = get_input_data_as_list(sys.argv[1])
rules_input = get_input_data_as_list(sys.argv[2])

rules_dict = parse_rules(rules_input)

error_rate, valid_tickets = calculate_scanning_error_rate(tickets_input, rules_dict)
print(f"The ticket scanning error rate is {error_rate}")

rule_position_pairs = get_rule_position_pairs(valid_tickets, rules_dict)

my_ticket = [113,53,97,59,139,73,89,109,67,71,79,127,149,107,137,83,131,101,61,103]
data_to_lookup = "departure"

print(f"The answer for star2 puzzle is: {calculate_star2_puzzle_answer(rule_position_pairs, my_ticket, data_to_lookup)}")
