from pathlib import Path
import itertools
import math


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        #split entries by blankline
        start_numbers = f.read().split(",")
    return start_numbers

def get_last_number(start_numbers, iterations):
    number_storage = dict()
    previous_number = 0

    #initialize number storage
    for i in range(0, len(start_numbers)):
        number_storage[int(start_numbers[i])] = [i +1]
        previous_number = int(start_numbers[i])

    for i in range(len(start_numbers) + 1, iterations + 1):
        next_number = 0

        if len(number_storage[previous_number]) == 1:
            next_number = 0
        else:
            length = len(number_storage[previous_number])
            diff = number_storage[previous_number][length - 1] - number_storage[previous_number][length - 2] 
            next_number = diff

        if next_number in number_storage.keys():
            number_storage[next_number].append(i)
        else:
            number_storage[next_number] = [i]

        previous_number = next_number
       
    
    return previous_number

if __name__ == "__main__":

    start_numbers = read_input_file("input.txt")
    print(f"Star 1: Solution is {get_last_number(start_numbers, 2020)}")
    print(f"Star 2: Solution is {get_last_number(start_numbers, 30000000)}")