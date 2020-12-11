# see README.doc

import copy, time

NO_SEAT = '.'
FREE = 'L'
OCCUPIED = '#'
NO_BOAT = 'X'

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [list(item.strip()) for item in local_list]
        return return_list


def get_seat_status(floor_plan, row, seat):
    ''' Returns seat status or NO_BOAT if outside of floor range
    '''
    length = len(floor_plan)
    width = len(floor_plan[0])
    if ((row < 0) or (row >= length) or
        (seat < 0) or (seat >= width)): return NO_BOAT
    return floor_plan[row][seat]

def get_adjacent(row, seat, floor_plan, star = 1):
    ''' Returns count of adjacent occupied seats.
        star == 1: direct neighbours
        star == 2: line of sight or end of floor plan
    '''
    count = 0
    for r in [-1, 0, 1]:
        for s in [-1, 0, 1]:
            if (r == 0 and s == 0): continue
            scan = 1
            while ((get_seat_status(floor_plan, row + r*scan, seat + s*scan) == NO_SEAT) and (star == 2)): 
                scan += 1
            if (get_seat_status(floor_plan, row + r*scan, seat + s*scan) == OCCUPIED): count += 1
    return count

def count_seats(floor_plan, status):
    ''' Returns amount of seat with status 'status' in floor plan
    '''
    count_seats = 0
    for row in range(len(floor_plan)):
        for seat in range(len(floor_plan[row])):
            if (floor_plan[row][seat] == status): count_seats += 1
    return count_seats

def iterate_floor_plan(floor_plan, star):
    ''' Generate new iteration of floor plan from (hard coded) rules.
        Rule 2 (amounts of neighbouring occupied) depends on star (1 --> 4, 2 --> 5)
    '''
    new_floor_plan = copy.deepcopy(floor_plan)
    for row in range(len(floor_plan)):
        for seat in range(len(floor_plan[row])):
            new_status = floor_plan[row][seat]
            if (new_status != NO_SEAT):
                adajacent_count = get_adjacent(row, seat, floor_plan, star)
                if ((new_status == FREE) and (adajacent_count == 0)):
                    new_status = OCCUPIED
                elif (adajacent_count >= (3 + star)):
                    new_status = FREE
            new_floor_plan[row][seat] = new_status
    return new_floor_plan

def get_occupied_seats(floor_plan, star = 1, verbose = True):
    ''' Iterates floor plan until it stabilizes. Returns occupied seats
    '''
    iteration = iterate_floor_plan(floor_plan, star)
    count = 0
    while(floor_plan != iteration):
        floor_plan = copy.deepcopy(iteration)
        iteration = iterate_floor_plan(floor_plan, star)
        count += 1
        if (verbose):
            for i in range(len(floor_plan)):
                print(count, "".join(floor_plan[i]))
            print()
    return count_seats(floor_plan, OCCUPIED)

        
def main():
    daily_list = read_daily_input('input11.txt')
    star1 = get_occupied_seats(daily_list, verbose = False)
    print(f"Occupied seats: {star1}")
    star2 = get_occupied_seats(daily_list, star = 2, verbose = False)
    print(f"Occupied seats (star2): {star2}")

if __name__ == "__main__":
    main()


