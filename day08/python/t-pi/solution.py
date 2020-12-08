import math


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list

def run_code(opcode_list):
    accumulator = 0
    past_line_numbers = list()
    cursor = 0
    while cursor not in past_line_numbers:
        line = opcode_list[cursor]
        past_line_numbers.append(cursor)
        code = line[:3]
        parameter = int(line[3:])
        if (code == 'jmp'): 
            cursor += parameter
            continue
        if (code == 'acc'): 
            accumulator += parameter
        cursor += 1
    return accumulator


def main():
    daily_list = read_daily_input('input08.txt')
    star1 = run_code(daily_list)
    print(f"Accmulator status at closing loop: {star1}")

if __name__ == "__main__":
    main()


