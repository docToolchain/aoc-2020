import re
import numpy as np

def read_ticketfields(line):
    regex_cmd = re.compile('([^:]+):\s(\d+)-(\d+)\s(or)\s(\d+)-(\d+)\s')
    temp_line = re.match(regex_cmd,line)
    temp_groups = temp_line.groups()

    return {temp_groups[0] : ((int(temp_groups[1]),int(temp_groups[2])),(int(temp_groups[4]),int(temp_groups[5])))}

def read_ticket(line):
    line.rstrip()
    return list(int(i) for i in line.split(','))

def process_input(file_contents):
    i = 0
    flag = 0
    ticket_fields = dict()
    other_tickets = list()
    while (i < len(file_contents)):
        if flag == 0:
            if file_contents[i] == "\n":
                flag = 1
                i += 2
            else:
                ticket_fields.update(read_ticketfields(file_contents[i]))
                i += 1
        elif flag == 1:
            my_ticket = read_ticket(file_contents[i])
            flag = 2
            i += 3
        else:
            other_tickets.append(read_ticket(file_contents[i]))
            i += 1

    return ticket_fields, my_ticket, other_tickets

def validate_number(ticket_value, ticket_fields):
    valid = list()
    for key,value in ticket_fields.items():
        if value[0][0] <= ticket_value <= value[0][1] or (value[1][0] <= ticket_value <= value[1][1]):
            valid.append(1)
        else:
            valid.append(0)
    return valid

def validate_ticket(ticket, ticket_fields):
    error = 0
    possible_fields = list()
    for entry in ticket:
        vector = validate_number(entry,ticket_fields)
        if sum(vector) == 0:
            error += entry
        else:
            possible_fields.append(vector)
    if len(possible_fields) == len(ticket):
        return possible_fields
    else:
        return [error]

with open("input.txt",'r') as code_file:
    all_code_file = code_file.readlines()

ticket_fields, my_ticket, other_tickets = process_input(all_code_file)

# Problem 1
error_rate = 0
valid_tickets = list()
valid_fields = list()
for ticket in other_tickets:
    if len(validate_ticket(ticket,ticket_fields)) == 1:
        error_rate += validate_ticket(ticket,ticket_fields)[0]
    else:
        valid_tickets.append(ticket)
        valid_fields.append(validate_ticket(ticket,ticket_fields))

print("The ticket error rate is", error_rate)

# Problem 2
number_fld_pos = len(ticket_fields)
number_val_tickets = len(valid_tickets)

# Go over all tickets to find which fields are principally valid for each position
pos_field = [[1 for i in range(number_fld_pos)] for j in range(number_fld_pos)]
for ticket_position in range(number_fld_pos):
    for field in range(number_fld_pos):
        for ticket in range(number_val_tickets):
            if valid_fields[ticket][ticket_position][field] == 0:
                pos_field[ticket_position][field] = 0

# Turn the answer into a matrix in Numpy
pos_field = np.array(pos_field)

matrix_of_ones = np.zeros((number_fld_pos,number_fld_pos))
matrix_of_ones.fill(1)

temp = pos_field@matrix_of_ones

order = temp[: , 0]
field_list = list()
mapping = dict()

for i in range(1,number_fld_pos+1):
    position = np.where(order == i)[0][0]
    valid_fields = np.nonzero(pos_field[position , :])
    field = list(set(valid_fields[0])-set(field_list))[0]
    field_list.append(field)
    mapping.update({list(ticket_fields)[field] : position})

departure_positions = [mapping[key] for key in mapping if "departure" in key]

product = 1
for positions in departure_positions:
    product *= my_ticket[positions]

print("The product of the 6 fields on my ticket starting with 'departure' is", product)