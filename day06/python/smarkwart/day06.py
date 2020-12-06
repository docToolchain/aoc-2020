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


def get_declarations_from_file(file_name):
    """
    Generates a list of declarations from given file
    """
    raw_declarations = get_input_data_as_list(sys.argv[1])
    declarations = create_declarations_list_from_raw_data(raw_declarations)

    return declarations

def create_declarations_list_from_raw_data(raw_declarations):
    """
    Creates a list of declarations where each passwort is a dictionary
    """
    declarations_list = []
    new_group = {'declarations':"", 'persons':0}
    for line in raw_declarations:
        if line.strip() != '':
            new_group['declarations'] += line.strip()
            new_group['persons'] += 1
        else:
            declarations_list.append(new_group)
            new_group = {'declarations':"", 'persons':0}

    #in case data does not end with newline there might be unprocessed password data
    if new_group != "":
        declarations_list.append(new_group)
        new_group = ""
    return declarations_list

def count_positive_questions(declarations_list):
    """
    Counts total number of positive answered questions for star1
    """
    total_count_all_positive = 0
    total_count_common_positive = 0
    for declaration in declarations_list:
        string_without_duplicates = remove_duplicate_char(declaration.get('declarations'))
        total_count_all_positive += len(string_without_duplicates)
        for char in string_without_duplicates:
            if declaration.get('declarations').count(char) == declaration.get('persons'):
                total_count_common_positive += 1
    return total_count_all_positive, total_count_common_positive

def remove_duplicate_char(input_string):
    """
    returns an unordered string without duplicate characters
    """
    return "".join(set(input_string))

customs_declarations = get_declarations_from_file(sys.argv[1])
count_positive_questions(customs_declarations)

print(count_positive_questions(customs_declarations))
