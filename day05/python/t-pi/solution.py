import math

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list

def binarize_boarding_pass(boarding_pass):
    ''' Replaces F/L with 0 resp. B/R with 1 in boarding pass to interpret them binarily.
        Returns tuple (row, column).
        Return negative column and/or row if anything fails.
    '''
    row = -1
    column = -1
    if (len(boarding_pass) == 10):
        row_str = boarding_pass[:7].replace('F', '0').replace('B', '1')
        col_str = boarding_pass[7:].replace('L', '0').replace('R', '1')
        try:
            row = int(row_str, 2)
            column = int(col_str, 2)
        except ValueError:
            pass
    return (row, column)

def get_seat_id(row, column):
    ''' Calculate seat ID from row * 8 + column
    '''
    return (row * 8 + column)

def bit_len(int_type):
    ''' Returns the position of the highest set bit in an integer
        Source: wiki.python.org/moin/BitManipulation
    '''
    length = 0
    while (int_type):
        int_type >>= 1
        length += 1
    return (length)

def check_all_boarding_passes(pass_list, star = 2):
    ''' Checks all boarding passes for 
        star = 1: highest seat id
        star = 2: missing seat id in rows[1:-1]
    '''
    max_id = 0
    plane = [0] * 128
    for line in pass_list:
        (row, column) = binarize_boarding_pass(line)
        if ((row >= 0 ) and (column >= 0)):
            plane[row] += 2**column
            id = get_seat_id(row, column)
            if (id > max_id): max_id = id
    if (star == 1): return max_id
    full_column = 255
    first_column = 0
    for my_row, my_col in enumerate(plane):
        if (my_col == 0): continue
        if (first_column == 0): 
            first_column = my_col
            continue
        if (my_col < full_column):
            my_seat_col = bit_len(full_column - my_col)-1
            print(f"Found empty seat @row: {my_row}, column: {my_seat_col}")
            return get_seat_id(my_row, my_seat_col)

def main():
    daily_list = read_daily_input('input05.txt')
    max_seat_id = check_all_boarding_passes(daily_list, 1)
    if (max_seat_id >= 0):
        print(f"Max seat ID: {max_seat_id}")
    my_seat_id = check_all_boarding_passes(daily_list, 2)
    if (my_seat_id >= 0):
        print(f"My seat ID: {my_seat_id}")

if __name__ == "__main__":
    main()


