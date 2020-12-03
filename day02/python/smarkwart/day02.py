import sys
import re

def get_input_data_as_list(file_name):
    """ Reads in data from the given file and returns them as list
        with one entry per line """
    with open(file_name) as input_file:
        data_list = input_file.readlines()
    return data_list

def validate_passwords_from_list(input_data):
    """ Takes a list with the input data and validates according to the rules 
        for each rule the number of valid passwords is returned """
    correct_passwords_old_rules = 0
    correct_passwords_new_rules = 0
    for line in input_data:
        if is_password_valid_with_old_rules(parse_line(line)):
            correct_passwords_old_rules += 1
        if is_password_valid_with_new_rules(parse_line(line)):
            correct_passwords_new_rules += 1
    return correct_passwords_old_rules, correct_passwords_new_rules

def parse_line(line):
    """ uses a regexp to parse the line into a dictionary """
    regex_match = re.match(r"(?P<first>\d*)-(?P<last>\d*) (?P<letter>.): (?P<password>.*)",line)
    dataset = regex_match.groupdict()
    return regex_match.groupdict()

def is_password_valid_with_old_rules(dataset):
    """ Validate password according to the old rules """
    letter_count = dataset['password'].count(dataset['letter'])
    return int(dataset['first']) <= letter_count and letter_count <= int(dataset['last'])

def is_password_valid_with_new_rules(dataset):
    """ Validate password accoding to the new rules """
    char_found = 0
    if dataset['password'][int(dataset['first'])-1] == dataset['letter']:
        char_found += 1
    if dataset['password'][int(dataset['last'])-1] == dataset['letter']:
        char_found += 1
    return char_found == 1

input = get_input_data_as_list(sys.argv[1])
print(f"Number of correct passwords (old_rules, new_rules): {validate_passwords_from_list(input)}")
