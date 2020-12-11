import sys
import collections
import copy
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        #data_list = list(input_file.readlines())
        #data_list = list(map(list, input_file.readlines()))
        data_list = input_file.readlines()
        data_list = [str.strip(line) for line in data_list]
        data_list = [list(line) for line in data_list]
    return data_list

def surround_with_floor(floor_plan):
    """
    docstring
    """
    for row in floor_plan:
        row.append('.')
        row.reverse()
        row.append('.')
        row.reverse()
    floor_plan.append(['.'] * len(floor_plan[0]))
    floor_plan.reverse()
    floor_plan.append(['.'] * len(floor_plan[0]))
    floor_plan.reverse()
    pass

def occupy_seat(floor_plan, row_idx, column_idx):
    """
    docstring
    """
    if get_adjacent_occupied_seats(floor_plan, row_idx, column_idx) == 0:
        return True
    else:
        return False

def leave_seat(floor_plan, row_idx, column_idx):
    """
    docstring
    """
    if get_adjacent_occupied_seats(floor_plan, row_idx, column_idx) >= 4:
        return True
    else:
        return False

def get_adjacent_occupied_seats(floor_plan, row_idx, column_idx):
    """
    docstring
    """
    seats_above = floor_plan[row_idx-1][column_idx-1:column_idx+2].count('#')
    seats_same = floor_plan[row_idx][column_idx-1:column_idx+2:2].count('#')
    seats_below = floor_plan[row_idx+1][column_idx-1:column_idx+2].count('#')
    return seats_above + seats_same + seats_below

def print_floor(floor_plan):
    """
    docstring
    """
    print()
    for row in floor_plan:
        print("".join(row))
    print()

def seat_the_people(floor_plan_in):
    floor_plan_copy = copy.deepcopy(floor_plan_in)

    for row_idx,row in enumerate(floor_plan_in):
        for column_idx,field in enumerate(row):
            #print(field)
            if field == 'L':
                if occupy_seat(floor_plan_in, row_idx, column_idx):
                    floor_plan_copy[row_idx][column_idx] = '#'
            elif field == '#':
                if leave_seat(floor_plan_in, row_idx, column_idx):
                    floor_plan_copy[row_idx][column_idx] = 'L'
                    pass
    return floor_plan_copy

def count_seated(floor_plan):
    fields = [field for row in floor_plan for field in row if field == '#'].count('#')
    return fields

floor_plan = get_input_data_as_list(sys.argv[1])
surround_with_floor(floor_plan)

print_floor(floor_plan)

#floor_plan = seat_the_people(floor_plan)
#print_floor(floor_plan)
#count_seated(floor_plan)
#
#floor_plan = seat_the_people(floor_plan)
#print_floor(floor_plan)
#count_seated(floor_plan)

seated_old = -1
seated_new = -2

while seated_old != seated_new:
    cls()
    seated_old = seated_new
    floor_plan = seat_the_people(floor_plan)
    print_floor(floor_plan)
    seated_new = count_seated(floor_plan)
    #input("Press Enter to continue...")
print(f"1st star: occupied seats when stable: {seated_new}\n")
