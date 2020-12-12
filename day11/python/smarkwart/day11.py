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

def occupy_seat(seating_function, floor_plan, row_idx, column_idx):
    if seating_function(floor_plan, row_idx, column_idx) == 0:
        return True
    else:
        return False

def leave_seat(seating_function, max_occupied, floor_plan, row_idx, column_idx):
    if seating_function(floor_plan, row_idx, column_idx) >= max_occupied:
        return True
    else:
        return False

def get_adjacent_occupied_seats(floor_plan, row_idx, column_idx):
    seats_above = floor_plan[row_idx-1][column_idx-1:column_idx+2].count('#')
    seats_same = floor_plan[row_idx][column_idx-1:column_idx+2:2].count('#')
    seats_below = floor_plan[row_idx+1][column_idx-1:column_idx+2].count('#')
    return seats_above + seats_same + seats_below

def get_line_of_sight_occupied_seats(floor_plan, row_idx, column_idx):
    seats_right = is_seated_right(floor_plan, row_idx, column_idx)
    seats_left = is_seated_left(floor_plan, row_idx, column_idx)
    seats_above = is_seated_above(floor_plan, row_idx, column_idx)
    seats_below = is_seated_below(floor_plan, row_idx, column_idx)
    seats_lower_right = is_seated_lower_right(floor_plan, row_idx, column_idx)
    seats_upper_right = is_seated_upper_right(floor_plan, row_idx, column_idx)
    seats_lower_left = is_seated_lower_left(floor_plan, row_idx, column_idx)
    seats_upper_left = is_seated_upper_left(floor_plan, row_idx, column_idx)
    return (seats_right + seats_left + seats_above + seats_below + 
    seats_lower_right + seats_upper_right + seats_lower_left + seats_upper_left)

def is_seated_right(floor_plan, row_idx, column_idx):
    for field in floor_plan[row_idx][column_idx+1:]:
        if field == '#':
            return 1
        elif field == 'L':
            return 0
    return 0

def is_seated_left(floor_plan, row_idx, column_idx):
    for field in floor_plan[row_idx][column_idx-1::-1]:
        if field == '#':
            return 1
        elif field == 'L':
            return 0
    return 0

def is_seated_above(floor_plan, row_idx, column_idx):
    for row in floor_plan[row_idx-1::-1]:
        if row[column_idx] == '#':
            return 1
        elif row[column_idx] == 'L':
            return 0
    return 0

def is_seated_below(floor_plan, row_idx, column_idx):
    for row in floor_plan[row_idx+1:]:
        if row[column_idx] == '#':
            return 1
        elif row[column_idx] == 'L':
            return 0
    return 0

def is_seated_lower_right(floor_plan, row_idx, column_idx):
    space_y = len(floor_plan[row_idx+1:])
    space_x = len(floor_plan[row_idx][column_idx+1:])
    for x in range(1, min(space_y, space_x)):
        if floor_plan[row_idx + x][column_idx + x] == '#':
            return 1
        elif floor_plan[row_idx + x][column_idx + x] == 'L':
            return 0
    return 0

def is_seated_upper_right(floor_plan, row_idx, column_idx):
    space_y = len(floor_plan[row_idx-1::-1])
    space_x = len(floor_plan[row_idx][column_idx+1:])
    for x in range(1, min(space_y, space_x)):
        if floor_plan[row_idx - x][column_idx + x] == '#':
            return 1
        elif floor_plan[row_idx - x][column_idx + x] == 'L':
            return 0
    return 0

def is_seated_lower_left(floor_plan, row_idx, column_idx):
    space_y = len(floor_plan[row_idx+1:])
    space_x = len(floor_plan[row_idx][column_idx-1::-1])
    for x in range(1, min(space_y, space_x)):
        if floor_plan[row_idx + x][column_idx - x] == '#':
            return 1
        elif floor_plan[row_idx + x][column_idx - x] == 'L':
            return 0
    return 0

def is_seated_upper_left(floor_plan, row_idx, column_idx):
    space_y = len(floor_plan[row_idx-1::-1])
    space_x = len(floor_plan[row_idx][column_idx-1::-1])
    for x in range(1, min(space_y, space_x)):
        if floor_plan[row_idx - x][column_idx - x] == '#':
            return 1
        elif floor_plan[row_idx - x][column_idx - x] == 'L':
            return 0
    return 0

def print_floor(floor_plan):
    print()
    for row in floor_plan:
        print("".join(row))
    print()

def seat_the_people(seating_function, max_occupied, floor_plan_in):
    floor_plan_copy = copy.deepcopy(floor_plan_in)
    for row_idx,row in enumerate(floor_plan_in):
        for column_idx,field in enumerate(row):
            if field == 'L':
                if occupy_seat(seating_function, floor_plan_in, row_idx, column_idx):
                    floor_plan_copy[row_idx][column_idx] = '#'
            elif field == '#':
                if leave_seat(seating_function, max_occupied, floor_plan_in, row_idx, column_idx):
                    floor_plan_copy[row_idx][column_idx] = 'L'
                    pass
    return floor_plan_copy

def count_seated(floor_plan):
    fields = [field for row in floor_plan for field in row if field == '#'].count('#')
    return fields

def find_seats(seating_function, max_occupied, floor_plan):
    seated_old = -1
    seated_new = -2
    while seated_old != seated_new:
        cls()
        seated_old = seated_new
        floor_plan = seat_the_people(seating_function, max_occupied, floor_plan)
        seated_new = count_seated(floor_plan)
        print_floor(floor_plan)
    return seated_new

def test_seating(seating_function, max_occupied, floor_plan, max_rounds):
    seated_old = -1
    seated_new = -2
    for round in range(0, max_rounds):
        cls()
        print(f"Round {round}")
        seated_old = seated_new
        floor_plan = seat_the_people(seating_function, max_occupied, floor_plan)
        seated_new = count_seated(floor_plan)
        print_floor(floor_plan)
        input("Press Enter to continue ... ")
        if seated_old == seated_new:
            break
    print(f"occupied seats when stable: {seated_new}\n")


floor_plan = get_input_data_as_list(sys.argv[1])
surround_with_floor(floor_plan)

#print_floor(floor_plan)

print(f"Occupied seats 1st star when stable: {find_seats(get_adjacent_occupied_seats, 4, floor_plan)}")

input("Press Enter to continue ... ")

print(f"Occupied seats 2nd star when stable: {find_seats(get_line_of_sight_occupied_seats, 5, floor_plan)}")



