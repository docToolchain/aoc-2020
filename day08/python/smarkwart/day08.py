import sys
import re
import copy

from aoccpu import AoCCPU

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = input_file.readlines()
    return data_list

def parse_instructions(instruction_list):
    """
    Parses the instruction strings into a dictionary
    """
    instruction_dict = []
    for instruction in instruction_list:
        regex_match = re.match(r"^(?P<opcode>\w*) (?P<operand>[-+]\d*)",instruction)
        if regex_match:
            instruction_dict.append(regex_match.groupdict())
    return instruction_dict

def try_to_fix_code(listing, reverse):
    """
    Functions tries out which single nop to change to jmp or jmp to change to nop
    in order to run until end of listing.
    If reverse is True this is done by going backwards the order of instructions executed until detectting the loop

    returns accumulator value when code was fixed successfully
    """
    this_cpu = AoCCPU(listing)
    result = this_cpu.restart()
    if result == "COMPLETED":
        return this_cpu.get_accumulator()
    execution_graph = this_cpu.get_execution_graph()
    if reverse:
        execution_graph.reverse()
    for line_of_code in execution_graph:
        opcode = listing[line_of_code].get('opcode')
        if opcode == 'nop' or opcode == 'jmp':
            listing_copy = copy.deepcopy(listing)
            if opcode == 'nop':
                listing_copy[line_of_code]['opcode'] = 'jmp'
            else:
                listing_copy[line_of_code]['opcode'] = 'nop'
            this_cpu.load_program(listing_copy)
            result = this_cpu.restart()
            if result == "COMPLETED":
                return this_cpu.get_accumulator()

input_data = get_input_data_as_list(sys.argv[1])

this_cpu = AoCCPU(parse_instructions(input_data))

result = this_cpu.restart()
print(f"Run the code as it is. No loop? {result}. Last accumulator: {this_cpu.get_accumulator()}")

print(f"Code fixed and accumulator is now: {try_to_fix_code(parse_instructions(input_data), True)}")
