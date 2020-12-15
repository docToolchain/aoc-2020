# see README.doc

import re


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [(item.strip()) for item in local_list]
        return return_list


def get_number_at(numbers_list, target_turn, verbose=False):
    ''' Store last turn in dict for all upcoming numbers (number = key)
        Iterate for <target-turn> times.
        Verbose: print out every turn
    '''
    memory = {int(nr): i for i, nr in enumerate(numbers_list)}
    print(memory)
    last_turn = max(memory.values())
    last_number = numbers_list[last_turn]
    for turn in range(max(memory.values())+1, target_turn):
        if (last_number in memory.keys()):
            this_number = last_turn - memory[last_number]
        else:
            this_number = 0
        if verbose:
            print(last_turn, ":", last_number, " -- ", turn, ":", this_number)
        memory[last_number] = last_turn
        last_number = this_number
        last_turn = turn
    return this_number


def main():
    daily_list = read_daily_input('input15.txt')
    for line in daily_list:
        star1 = get_number_at(line.split(','), 2020)
    print(f"2020th: {star1}")
    for line in daily_list:
        star2 = get_number_at(line.split(','), 30000000)
    print(f"30000000th: {star2}")


if __name__ == "__main__":
    main()
