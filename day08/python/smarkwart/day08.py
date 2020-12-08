import sys
import re
import copy

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

def run_code(listing):
    """
    run the code from the listing:
    return values:
        accumulator: last accumulator value when returning from this function
        no_loop: 'True' if no potential endless loop was detected, 'False' if potential endless loop was detected
    """
    program_counter = 0
    accumulator = 0
    execution_graph = []
    #print(f"\n\tpc\tacc\top\topc")
    while program_counter < len(listing):
        opcode, operand = decode_instruction(listing[program_counter])
        if program_counter in execution_graph:
            return accumulator, False, execution_graph
        execution_graph.append(program_counter)
        program_counter, accumulator = execute_instruction(opcode, operand, program_counter, accumulator)
    return accumulator, True, execution_graph

def decode_instruction(instruction):
    """
    decodes the instruction into opcode and operand
    """
    opcode = instruction.get('opcode')
    operand = int(instruction.get('operand'))
    return opcode, operand

def execute_instruction(opcode, operand, program_counter, accumulator):
    """
    executes the instructions
    """
    #print(f"\t{program_counter}\t{accumulator}\t{opcode}\t{operand}")
    if opcode == 'acc':
        accumulator += operand
        program_counter += 1
    elif opcode == 'jmp':
        program_counter += operand
    else:
        program_counter += 1
    return program_counter, accumulator

def try_to_fix_code(listing):
    """
    Functions tries out which single nop to change to jmp or jmp to change to nop
    in order to run until end of listing.

    returns accumulator value when code was fixed successfully
    """
    for line_of_code, instruction in enumerate(listing):
        opcode, operand = decode_instruction(instruction)
        if opcode == 'nop' or opcode == 'jmp':
            listing_copy = copy.deepcopy(listing)
            if opcode == 'nop':
                listing_copy[line_of_code]['opcode'] = 'jmp'
            else:
                listing_copy[line_of_code]['opcode'] = 'nop'
            accumulator, no_loop, execution_graph = run_code(listing_copy)
            if no_loop:
                return accumulator

def try_to_fix_code_reverse(listing):
    """
    Functions tries out which single nop to change to jmp or jmp to change to nop
    in order to run until end of listing.
    This is done by going backwards the order of instructions executed until detectting the loop

    returns accumulator value when code was fixed successfully
    """
    accumulator, no_loop, execution_graph = run_code(listing)
    if no_loop:
        return accumulator
    execution_graph.reverse()
    for line_of_code in execution_graph:
        opcode, operand = decode_instruction(listing[line_of_code])
        if opcode == 'nop' or opcode == 'jmp':
            listing_copy = copy.deepcopy(listing)
            if opcode == 'nop':
                listing_copy[line_of_code]['opcode'] = 'jmp'
            else:
                listing_copy[line_of_code]['opcode'] = 'nop'
            accumulator, no_loop, execution_graph = run_code(listing_copy)
            if no_loop:
                return accumulator

input_data = get_input_data_as_list(sys.argv[1])

accumulator, no_loop, execution_graph = run_code(parse_instructions(input_data))
print(f"Run the code as it is. No loop? {no_loop}. Last accumulator: {accumulator}")

print(f"Code fixed and accumulator is now: {try_to_fix_code_reverse(parse_instructions(input_data))}")
