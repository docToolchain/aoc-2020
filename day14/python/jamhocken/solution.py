import re

def process_input(file_contents):
    container = list()
    for code_lines in file_contents:
        command_line = code_lines.split(' = ')
        if command_line[0] == 'mask':
            container.append(('mask',command_line[1].rstrip()))
        else:
            container.append(('mem',int(command_line[0].strip('me[]')),int(command_line[1].rstrip())))
    return container

def run_program1(commands):
    memory_dict = dict()
    for command in commands:
        if command[0] == 'mask':
            mask = command[1]
        else:
            memory_dict[command[1]] = update_memory(command[2],mask)
    return memory_dict

def update_memory(value, mask):
    binary_value = list(format(value,'0=036b'))
    for j,i in enumerate(mask):
        if i != 'X':
            binary_value[j] = mask[j]
    return (int("".join(binary_value),2))

def run_program2(commands):
    memory_dict = dict()
    for command in commands:
        if command[0] == 'mask':
            mask = command[1]
        else:
            addresses = update_memory2(command[1], mask)
            for i in addresses:
                memory_dict[i] = command[2]
    return sum(memory_dict.values())

def update_memory2(address, mask):
    X_bits = list()
    addresses = list()
    address_bin = list(format(address,'0=036b'))
    for j,i in enumerate(mask):
        if i == '1':
            address_bin[j] = '1'
        elif i == 'X':
            X_bits.append(j)
    if len(X_bits) == 0:
        addresses.append(int("".join(address_bin),2))
    else:
        temp_address = [(int("".join(address_bin),2))]
        for bits in X_bits:
            for i in temp_address.copy():
                a1 = list(format(i,'0=036b'))
                a2 = list(format(i,'0=036b'))
                a1[bits] = '0'
                a2[bits] = '1'
                addresses.append(int("".join(a1),2))
                addresses.append(int("".join(a2),2))
                temp_address.append(int("".join(a1),2))
                temp_address.append(int("".join(a2),2))
    return addresses

with open("input.txt",'r') as code_file:
    all_code_file = code_file.readlines()

program_contents = process_input(all_code_file)
memory_contents = run_program1(program_contents)

print('The sum of all values in memory from problem 1 is', sum(memory_contents.values()))

print('The sum of all values in memory from problem 2 is', run_program2(program_contents.copy()))
