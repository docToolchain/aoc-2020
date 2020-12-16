# see README.doc

import re


def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [(item.strip()) for item in local_list]
        return return_list


def apply_bitmask(value, bitmask):
    ''' Apply bitmask list (036b) list-element per list-element to value list (036b)
    '''
    len_val = len(value)
    len_mask = len(bitmask)
    if (len_val != len_mask):
        return -1
    for idx in range(len_mask):
        if (bitmask[idx] != 'X'):
            value[idx] = bitmask[idx]
    val_str = "".join(value)
    if (val_str.isnumeric()):
        return(int(val_str, 2))
    else:
        return -1


def get_mem_sum(instructions):
    ''' Star 1: Fill 'mem' dict with values and sum up
    '''
    bitmask = list(format(0, '036b'))
    mem = dict()
    for line in instructions:
        command, value = [s.strip() for s in line.split('=')]
        if (command == 'mask'):
            bitmask = value
        else:
            address = int(re.search('\[([0-9]+)\]', command).group(1))
            bitvalue = list(format(int(value), '036b'))
            mem[address] = apply_bitmask(bitvalue, bitmask)
    return sum(mem.values())


def apply_bitmask_v2(base_address, bitmask):
    ''' Star 2: Derive memory addresses from base address list (036b) and bitmask list (036b)
        Returns list with all found addresses (int)
    '''
    for idx in range(len(bitmask)):
        if ((bitmask[idx] == '1') or (bitmask[idx] == 'X')):
            base_address[idx] = bitmask[idx]
    address_list = [base_address]
    for idx in range(base_address.count('X')):
        address_buffer = list()
        for address in address_list:
            if ('X' in address):
                x_pos = address.index('X')
                address_buffer.append(
                    address[:x_pos] + ['0'] + address[x_pos+1:])
                address_buffer.append(
                    address[:x_pos] + ['1'] + address[x_pos+1:])
        address_list = address_buffer
    return [int("".join(addr), 2) for addr in address_list]


def get_mem_sum_v2(instructions):
    ''' Star 2: Fill 'mem' dict for masked address lists and sum p
    '''
    bitmask = list(format(0, '036b'))
    mem = dict()
    for line in instructions:
        command, value_str = [s.strip() for s in line.split('=')]
        if (command == 'mask'):
            bitmask = list(value_str)
        else:
            value = int(value_str)
            start_addr = list(
                format(int(re.search('\[(\d+)\]', command).group(1)), '036b'))
            address_list = apply_bitmask_v2(start_addr, bitmask)
            for address in address_list:
                mem[address] = value
    return sum(mem.values())


def main():
    daily_list = read_daily_input('input14.txt')
    star1 = get_mem_sum(daily_list)
    print(f"Memory sum: {star1}")
    star2 = get_mem_sum_v2(daily_list)
    print(f"Memory sum v2: {star2}")


if __name__ == "__main__":
    main()
