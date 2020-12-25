from pathlib import Path
import re

def extract_ticket_info(line):
    # breaking up the input into the different parts
  
    numbers = line.strip().split(',')
    numbers =  list(map(int, numbers))
    return numbers

def get_tickets(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        tickets = list(map(extract_ticket_info, f.readlines()))
    return tickets

def extract_rule_information(line):
    # breaking up the input into the different parts
  
    m = re.match(r"^(.*): (\d*)-(\d*) or (\d*)-(\d*)$", line)
    rule = m.group(1)
    limit1 = (int(m.group(2)), int(m.group(3)))
    limit2 = (int(m.group(4)), int(m.group(5)))
    return [rule, limit1, limit2]

def get_rules(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        rules = list(map(extract_rule_information, f.readlines()))
    return rules

def check_tickets(tickets,rules):
    valid_tickets = list()
    error_rate = 0
    for ticket in tickets:
        ticket_valid = True
        for number in ticket:
            #check for every number if at least one rule matches
            matching_rule_found = False
            for rule in rules:
                if matching_rule_found: break
                for limit in rule[1:3]:
                    if limit[0] <= number and number <= limit[1]:
                        matching_rule_found = True                        
                        break

                    #when number within in limit true , break sonst false
            if not matching_rule_found:
                error_rate += number
                ticket_valid = False
        
        if ticket_valid:
            valid_tickets.append(ticket)

    return error_rate, valid_tickets
    
def find_fields(valid_tickets, rules):
    field_values = dict(list())

    #for every field collect all values that occur
    for ticket in valid_tickets:
        for field in range(0, len(ticket)):
            if field in field_values.keys():
                field_values[field].append(ticket[field])
            else:
                field_values[field] = [ticket[field]]

    #for every field check if a rule applies and collect all applicable rules in mapping table
    mapping_table = dict()
    for field in field_values.keys():
        for rule in rules:
            matching_rule_found = True
            for number in field_values[field]:
                if (rule[1][0] <= number and number <= rule[1][1]) or (rule[2][0] <= number and number <= rule[2][1]) :
                    matching_rule_found = True
                else:
                    matching_rule_found = False                 
                    break
            if matching_rule_found:
                if field in mapping_table.keys():
                    mapping_table[field].append(rule[0])
                else:
                    mapping_table[field] = [rule[0]]

    #some fiels have several rules that are appliacable but some rules only have one field    #        
    not_identified_fields = list(mapping_table.keys())

    while len(not_identified_fields) != 0:
        for field in not_identified_fields:
            applicable_rules = len(mapping_table[field])
            if applicable_rules == 1:
                not_identified_fields.remove(field)
                for entry in mapping_table:
                    if entry != field:
                        if mapping_table[field][0] in  mapping_table[entry]: 
                            mapping_table[entry].remove(mapping_table[field][0])
    return mapping_table


if __name__ == "__main__":
    tickets = get_tickets('tickets.txt')
    rules = get_rules('rules.txt')

    error_rate, valid_tickets = check_tickets(tickets,rules)
    print(f"Star 1: Ticket scanning error rate is {error_rate}")

    #star2
    mapping_table = find_fields(valid_tickets, rules)
    my_ticket = tickets[0]
    ticket_product = 1

    for field in ['departure location', 'departure station', 'departure platform', 'departure track', 'departure date', 'departure time']:
        index = 0
        for key, value in mapping_table.items():
            if value[0] == field:
                index = key
        ticket_product *= my_ticket[index]

    print(f"Star 2: Product of all departure field is: {ticket_product}")    
  
