import sys
import re

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        #data_list = map(str.strip,input_file.readlines())
        data_list = input_file.readlines()
    return data_list

def transform_binarystring_to_number(binary_string, set_char):
    """
    Transforms the binary string into the row number
    set_char euqals the char which equals to '1' bit 
    """
    row_id = 0
    for idx, char in enumerate(binary_string[::-1]):
        if char == set_char:
            row_id += pow(2,idx)
    return row_id

def get_row_string_from_string(full_string):
    """
    Gets the row string from the full string
    """
    return full_string[0:7]

def get_column_string_from_string(full_string):
    """
    Gets the row string from the full string
    """
    return full_string[7:10]

def calculate_seat_id(seat_code):
    """
    calculates seat id from seat code
    """
    row = transform_binarystring_to_number(get_row_string_from_string(seat_code), "B")
    column = transform_binarystring_to_number(get_column_string_from_string(seat_code), "R")
    return row * 8 + column

def get_seat_codes(seat_list):
    """
    get the highest seat id of the seat code list
    """
    return [calculate_seat_id(seat) for seat in seat_list  ]

def get_my_seat(seat_codes):
    seat_codes.sort()
    return set(range(seat_codes[0], seat_codes[-1] + 1)).difference(seat_codes)



seat_list = get_input_data_as_list(sys.argv[1])
seat_codes = get_seat_codes(seat_list)

print(f"Highest SeatId: {max(seat_codes)}")
print(f"My seat is: {get_my_seat(seat_codes)}")

