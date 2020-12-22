from pathlib import Path
import itertools
import copy
import re



def read_input_file(input_file_path):
    p = Path(input_file_path)

    instructions = list(dict())

    with p.open() as f:
        raw_rows = f.read().split("\n")
        for row in raw_rows:
            
            if row.startswith('mask'):
                bit_mask = re.match("^mask = (.*)$", row).group(1)
                instructions.append(dict([('instruction', 'mask'), ('bit_mask', list(bit_mask))]))
            else:
                address, value = re.match("^mem\[(\d*)\] = (\d*)$",row).groups()
                instructions.append(dict([('instruction', 'write'), ('address', int(address)), ('value', int(value))]))      
    return instructions


def process_instructions_star1(instructions):
    bit_mask = '0'
    memory = dict()
    for instruction in instructions:
        
        if instruction['instruction'] == 'mask':
            bit_mask = instruction['bit_mask']
        else:
            new_value  = list(format(2, '036b'))
            #value in binar array umbauen
            cur_value = list(format(instruction['value'], '036b'))
            for i in range(35, -1, -1):
              
                if bit_mask[i] == 'X':
                    new_value[i] = cur_value[i]
                elif bit_mask[i] == '0':
                    new_value[i] = 0
                elif bit_mask[i] == '1':
                    new_value[i] = 1

            memory[instruction['address']] = list_to_int(new_value)
    return memory

def process_instructions_star2(instructions):
    bit_mask = '0'
    memory = dict()
    for instruction in instructions:
        
        if instruction['instruction'] == 'mask':
            bit_mask = instruction['bit_mask']
        else:
            cur_address = list(format(instruction['address'], '036b'))
            new_address = list(format(0, '036b'))

            for i in range(35, -1, -1):              
                if bit_mask[i] == 'X':
                    new_address[i] = 'X'
                elif bit_mask[i] == '0':
                    new_address[i] = cur_address[i]
                elif bit_mask[i] == '1':
                    new_address[i] = '1'


            addresses = permutate([''.join(new_address)])
            
            for address in addresses:
                write_address = list_to_int(address)
                memory[write_address] = instruction['value']
    return memory

def permutate(addresses):

    all_addresses = list()
    for address in addresses:
        address = list(address)
        i =  0
        
        while i < 36:
            if address[i] == 'X':
                var1_address = address.copy()
                var1_address[i] = '0'
                var2_address = address.copy()
                var2_address [i] = '1'
                all_addresses.extend(permutate([''.join(var1_address), ''.join(var2_address)]))
                break
            i += 1
        if i == 36:
            all_addresses.append(''.join(address))
    return all_addresses

def list_to_int(list_input):
    retVal = 0
    for i in range(0, 36, 1):
        retVal += int(list_input[(35-i)]) * (2**i)
    return retVal


if __name__ == "__main__":

    instructions = read_input_file("input.txt")  
    
    #Star 1
    memory = process_instructions_star1(instructions)

    total_value = 0
    for memory_cell in memory.items():
        total_value += memory_cell[1]
    print(f"Star 1: The total sum of all values in all memory cells is: {total_value}")

    #Star 2
    memory = process_instructions_star2(instructions)

    total_value = 0
    for memory_cell in memory.items():
        total_value += memory_cell[1]
    print(f"Star 2: The total sum of all values in all memory cells is: {total_value}")