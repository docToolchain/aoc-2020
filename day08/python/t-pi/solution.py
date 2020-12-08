import math


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list

def check_code_for_loop(opcode_list):
    ''' Checks list of lines with opcodes and single parameter for endless loop.
        Tracks accumulator status along the way of the code.
        Returns (True, accumulator value) for loop starting, (false, acc.) with no loop
    '''
    accumulator = 0
    past_line_numbers = list()
    cursor = 0
    while ((cursor not in past_line_numbers) and   
            (cursor < len(opcode_list))):
        line = opcode_list[cursor]
        past_line_numbers.append(cursor)
        opcode = line[:3]
        parameter = int(line[3:])
        if (opcode == 'jmp'): 
            cursor += parameter
            continue
        if (opcode == 'acc'): 
            accumulator += parameter
        cursor += 1
    return ((cursor in past_line_numbers), accumulator)

def optimize_code(opcode_list):
    ''' Runs through code list and tenatively replaces every 'nop' with 'jmp'
        resp. the other way around at current line if found.
        Then check for loop is run with this single modification of opcode list.
        Returns with accumulator value or False, if code not fixed.
    '''
    nops = list()
    jmps = list()
    for number, line in enumerate(opcode_list):
        opcode = line[:3]
        if (opcode == 'jmp') or (opcode_list == 'nop'):
            modlist = opcode_list.copy()
            if (opcode == 'jmp'):
                modlist[number] = modlist[number].replace('jmp', 'nop')
            else:
                modlist[number] = modlist[number].replace('nop', 'jmp')
            loop, accumulator = check_code_for_loop(modlist)
            if (not loop): return accumulator
    return False

def main():
    daily_list = read_daily_input('input08.txt')
    loop, star1 = check_code_for_loop(daily_list)
    print(f"Accmulator status at closing loop: {star1}")
    star2 = optimize_code(daily_list)
    print(f"Accumulator status with fixed code: {star2}")

if __name__ == "__main__":
    main()


