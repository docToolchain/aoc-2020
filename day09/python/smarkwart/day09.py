from itertools import combinations
import sys
import itertools

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = list(map(int, input_file.readlines()))
    return data_list

def find_wrong_value(data, preamble):
    """
    Finds the first value which is not fulfilling the rules for star1 of day09 puzzle
    """
    for idx, item in enumerate(data[preamble:],preamble):
        combinations = itertools.combinations(data[idx-preamble:idx], 2)
        result = [item for x in combinations if sum(x) == item]
        if not result:
            return item

def find_weakness(data, wrong_value):
    """
    Finds the weakness according to star2 day09 puzzle
    """
    index_of_wrong_value = data.index(wrong_value)
    weakness =  [(min(data[start:end]) + max(data[start:end])) 
                for start in range(0, index_of_wrong_value) 
                for end in range(start, index_of_wrong_value) 
                if sum(data[start:end]) == wrong_value]
    return weakness

input_data = get_input_data_as_list(sys.argv[1])
preamble = int(sys.argv[2])

wrong_value = find_wrong_value(input_data, preamble)
print(f"The smallest wrong number is: {wrong_value}")
print(f"The weakness is: {find_weakness(input_data, wrong_value)}")
