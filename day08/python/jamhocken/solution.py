import re

def process_input(file_contents):      
    container = dict()
    for counter, code_lines in enumerate(file_contents):
        regex_cmd = re.compile('((jmp)|(acc)|(nop))\s((\+|-)\d+)')
        temp_line = regex_cmd.match(code_lines)
        container.update({counter : \
                          (temp_line.group(1),int(temp_line.group(5)))})
    return container

def execute_program(program):
    lines_executed = list()
    current_line = 0
    accumulater = 0
    noloop = False
    while (not (current_line in lines_executed) and noloop != True):
        if program[current_line][0] == 'nop':
            lines_executed.append(current_line)
            current_line += 1
        elif program[current_line][0] == 'acc':
            lines_executed.append(current_line)
            accumulater += program[current_line][1]
            current_line += 1
        else:
            lines_executed.append(current_line)
            current_line += program[current_line][1]
        if current_line == len(all_codes):
            noloop = True
            
    return accumulater, noloop, lines_executed

with open("code.txt",'r') as code_file: 
    all_code_file = code_file.readlines()

all_codes = process_input(all_code_file)

accumulater, noloop, lines_executed = execute_program(all_codes)

print('The accumulator had a value of', accumulater, 'before looping.')

for lines in lines_executed:
    current_line = 0
    accumulater = 0
    lines_fixed = list()
    temp_codes = all_codes.copy()

    if all_codes[lines][0] == 'nop':
        temp_codes.update({lines : ('jmp',all_codes[lines][1])})
    elif all_codes[lines][0] == 'jmp':
        temp_codes.update({lines : ('nop',all_codes[lines][1])})  
    accumulater, noloop, lines_executed = execute_program(temp_codes)
    if noloop: capture = accumulater
            
print('The fixed program had an accumulator value of', 
      capture,'after terminating.')
            