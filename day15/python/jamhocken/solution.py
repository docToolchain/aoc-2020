import re

def process_input(file_contents):
    return {int(key):value for value,key in enumerate(file_contents.split(','))}

def return_last_value(dictionary,iterations):
    running_dict = dictionary.copy()
    current_value = 0

    for round_no in range(len(initial_no), iterations):
        if round_no == iterations-1:
            last_value = current_value
        if not (current_value in running_dict.keys()):
            running_dict[current_value] = round_no
            current_value = 0
        else:
            next_value = round_no - running_dict[current_value]
            running_dict[current_value] = round_no
            current_value = next_value
    return last_value

with open("input.txt",'r') as code_file:
    all_code_file = code_file.readline()

initial_no = process_input(all_code_file.rstrip())

#Problem 1
no_of_rounds = 2020

print('What will be the 2020th number spoken?', return_last_value(initial_no, no_of_rounds))

#Problem 1
no_of_rounds = 30000000

print('What will be the 30000000th number spoken?', return_last_value(initial_no, no_of_rounds))