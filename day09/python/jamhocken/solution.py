import re

# variable length of preamble
length = 25

def process_input(file_contents):      
    code = list()
    for line in file_contents:
        code.append(int(line))
    return code

def find_sums(list_numbers):
    sums_list = list()
    for i in range(0,len(list_numbers)-1):
        for j in range(i+1,len(list_numbers)):
            sums_list.append(list_numbers[i] + list_numbers[j])
    return sums_list

def find_indices(all_codes, magic_number):
    for i in range(0,len(all_codes)):
        j = i+1
        while sum(all_codes[i:j]) <= magic_number and j < len(all_codes):
            if sum(all_codes[i:j]) == magic_number:
                return i, j
            else:
                j = j+1
    return

with open("XMAS.txt",'r') as code_file: 
    all_code_file = code_file.readlines()

all_codes = process_input(all_code_file)

point = length
queue = all_codes[0:point]
sums = find_sums(queue)

while all_codes[point] in sums:
    point += 1
    queue = all_codes[point-length:point]
    sums = find_sums(queue)

print('The first number that is not the sum of the previous', 
      length, 'numbers, is', all_codes[point])
magic_number = all_codes[point]

i,j = find_indices(all_codes,magic_number)
print('The encryption weakness is', min(all_codes[i:j]) + max(all_codes[i:j]))
