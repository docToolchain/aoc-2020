import sys
import re

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = input_file.readlines()
    return data_list

def set_x_to_zero(mask_string):
    mask_string = str.replace(mask_string, 'X', '0')
    mask_value = int(mask_string, 2)
    return mask_value

def set_x_to_one(mask_string):
    mask_string = str.replace(mask_string, 'X', '1')
    mask_value = int(mask_string, 2)
    return mask_value

def apply_mask(value, mask_string):
    masked_value = (value & set_x_to_one(mask_string)) | set_x_to_zero(mask_string)
    return masked_value

def get_max_mem_size(instructions):
    addresses = [int(instr["parameter"]) for instr in instructions if instr["command"] == "mem"]
    return max(addresses)

def decoder_v1(instructions):
    mask_string = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    memory = [0] * (get_max_mem_size(instructions) + 1)
    for instruction in instructions:
        if instruction["command"] == "mask":
            mask_string = instruction["value"]
        elif instruction["command"] == "mem":
            memory[int(instruction["parameter"])] = apply_mask(int(instruction["value"]), mask_string)
    return sum(memory)

def decoder_v2(instructions):
    mask_string = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    memory = {}
    for instruction in instructions:
        if instruction["command"] == "mask":
            mask_string = instruction["value"]
        elif instruction["command"] == "mem":
            addresses = get_addresses_from_mask(int(instruction["parameter"]), mask_string)
            set_value_at_addresses(int(instruction["value"]), addresses, memory)
    return sum(memory.values())

def set_value_at_addresses(value, addresses, memory):
    for address in addresses:
        memory[address] = value

def get_index_of_address_from_memory(address, memory):
    return next((idx for idx, item in enumerate(memory) if item["address"] == address), None)

def parse_instructions(input_data):
    instruction_dict = []
    for instruction in input_data:
        regex_match = re.match(r"^(?P<command>\w+)\[?(?P<parameter>\d+)?\]? = (?P<value>\w+)",instruction)
        if regex_match:
            instruction_dict.append(regex_match.groupdict())
    return instruction_dict

def get_addresses_from_mask(start_address, mask_string):
    base_address = start_address |  set_x_to_zero(mask_string)
    list_of_addresses = get_list_of_addresses(mask_string, f"{base_address:036b}")
    return list_of_addresses

def get_list_of_addresses(mask_string, base_address_string):
    x_count = mask_string.count('X')
    list_of_xs = [idx for idx, char in enumerate(mask_string) if char == 'X']
    addresses = []
    for address_modifier in range(0,pow(2,x_count)):
        new_address = set_bits_at_positions(list_of_xs, list(f"{address_modifier:b}".zfill(len(list_of_xs))), base_address_string)
        addresses.append(int(new_address,2))
    return addresses

def set_bits_at_positions(positions, bits_to_set, mask_string):
    mask_list = list(mask_string)
    for idx, position in enumerate(positions):
        if bits_to_set[idx] == '1':
            mask_list[position] = '1'
        else:
            mask_list[position] = '0'
    return "".join(mask_list)


input_data = get_input_data_as_list(sys.argv[1])

instructions = [
    {"command" : "mask", "parameter" : "", "value" : "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"},
    {"command" : "mem", "parameter" : "8", "value" : "11"},
    {"command" : "mem", "parameter" : "7", "value" : "101"},
    {"command" : "mem", "parameter" : "8", "value" : "0"},
]

instruction_dict = parse_instructions(input_data)
print(f"Result for 1st star: {decoder_v1(instruction_dict)}")

print(f"Result for 1st star: {decoder_v2(instruction_dict)}")
