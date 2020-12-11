# see README.doc

import copy

NO_SEAT = '.'
FREE = 'L'
OCCUPIED = '#'

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [list(item.strip()) for item in local_list]
        return return_list


def is_occupied(row, seat, floor_plan):
    ''' Returns count of adjacent occupied seats in floor_plan
    '''
    length = len(floor_plan)
    width = len(floor_plan[0])
    if ((row < 0) or (row >= length) or
        (seat < 0) or (seat >= width)): return False
    return (floor_plan[row][seat] == OCCUPIED)

def get_adjacent(row, seat, floor_plan):
    '''
    '''
    count = 0
    for r in [-1, 0, 1]:
        for s in [-1, 0, 1]:
            if (r == 0 and s == 0): continue
            if (is_occupied(row + r, seat + s, floor_plan)): count += 1
    return count

def count_seats(floor_plan, status):
    count_seats = 0
    for row in range(len(floor_plan)):
        for seat in range(len(floor_plan[row])):
            if (floor_plan[row][seat] == status): count_seats += 1
    return count_seats

def iterate_floor_plan(floor_plan):
    '''
    '''
    new_floor_plan = copy.deepcopy(floor_plan)
    for row in range(len(floor_plan)):
        for seat in range(len(floor_plan[row])):
            new_status = floor_plan[row][seat]
            if (new_status != NO_SEAT):
                adajacent_count = get_adjacent(row, seat, floor_plan)
                if ((new_status == FREE) and (adajacent_count == 0)):
                    new_status = OCCUPIED
                elif (adajacent_count >= 4):
                    new_status = FREE
            new_floor_plan[row][seat] = new_status
    return new_floor_plan

def does_iteration_evolve(floor_plan, iteration):
    '''
    '''
    for i in range(len(floor_plan)):
        print(floor_plan[i], iteration[i])
    for row in range(len(floor_plan)):
        for seat in range(len(floor_plan[row])):
            if (floor_plan[row][seat] != iteration[row][seat]): 
                return True
    return False
    #return all(map(lambda step0, step1: step0 == step1, floor_plan, iteration))


def get_free_seats(floor_plan, verbose = True):
    '''
    '''
    iteration = iterate_floor_plan(floor_plan)
    count = 0
    while(floor_plan != iteration):
        floor_plan = copy.deepcopy(iteration)
        iteration = iterate_floor_plan(floor_plan)
        count += 1
        if (verbose):
            for i in range(len(floor_plan)):
                print(count, "".join(floor_plan[i]))
            print()
    return count_seats(floor_plan, OCCUPIED)

        
def main():
    daily_list = read_daily_input('input11.txt')
    star1 = get_free_seats(daily_list, False)
    print(f"Free seats: {star1}")

if __name__ == "__main__":
    main()


