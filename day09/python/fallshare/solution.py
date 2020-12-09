from pathlib import Path
import itertools


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        data = list(map(int, f.readlines()))

    return data

def get_first_weak_number(data, preamble_length):
    pos_current_number = preamble_length

    weak_number_found = False
    while(not weak_number_found):
        #itertools.combinations(values, length)
        current_numbers = data[(pos_current_number - preamble_length):pos_current_number ]
        
        number_combinations = itertools.combinations(current_numbers, 2)
        current_sums = list(map(sum, number_combinations))

        if data[pos_current_number] not in current_sums:
            weak_number_found = True
        else:
            pos_current_number += 1

           
      
    if weak_number_found == True:
        return pos_current_number


def get_encrytpion_weakness(data, weak_number):
    contiguous_numbers = get_contiguous_numbers(data, weak_number)
    return min(contiguous_numbers) + max(contiguous_numbers)

def get_contiguous_numbers(data, weak_number):
    #left boundary
    for left in range(0, weak_number):
        for right in range(left + 1, weak_number):
            current_list = data[left:right]
            if sum(current_list) == data[weak_number]:
                return current_list

if __name__ == "__main__":

    cypher = read_input_file("input.txt")

    pos_weak_number = get_first_weak_number(cypher, 25)

    print(f"Star 1: first weak number is {cypher[pos_weak_number]}")
    print(f"Star 2: Encryption wekaness is {get_encrytpion_weakness(cypher, pos_weak_number)}")