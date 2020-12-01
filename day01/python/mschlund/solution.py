import math
import itertools

def find_two_numbers(target, all_numbers):
    numbers_to_expect = set([])
    for num in all_numbers:
        remaining_sum = target - num
        if num in numbers_to_expect:
            print('Found it!')
            result = num * remaining_sum
            print(result)
        else:
            numbers_to_expect.add(remaining_sum)

def find_three_numbers(target, all_numbers):
    numbers_to_expect = set([])

    for pair in itertools.permutations(all_numbers, r=2):
        remaining_sum = target-(pair[0] + pair[1])
        if pair[0] in numbers_to_expect and pair[1] in numbers_to_expect:
            print('Found it!')
            result = pair[0] * pair[1] * remaining_sum
            print(result)
        else:
            numbers_to_expect.add(remaining_sum)

def main():
    target_number = 2020
    input_filename = 'input.txt'
    numbers_to_expect = set([])
    all_numbers = []
    with open(input_filename, 'r') as input:
        for line in input:
            try:
                num = int(line)
            except ValueError:
                print('no int:\"{}\"'.format(line))
                continue
            numbers_to_expect.add(num-target_number)
            all_numbers.append(num)
    find_three_numbers(target_number, all_numbers)

if __name__ == "__main__":
    main()