from collections import defaultdict
from itertools import groupby
import math

def count_gaps(sorted_numbers):
  counts = defaultdict(int)
  for fst, snd in zip(sorted_numbers, sorted_numbers[1:]):
    gapsize = snd - fst
    counts[gapsize] += 1
  return counts

def is_valid(sorted_numbers, threshold=4):
  return all([x<threshold for x in count_gaps(sorted_numbers).keys()])

def arrangements(n):
  if n == 0:
    return 1
  elif n == 1:
    return 2
  elif n == 2:
    return 4
  elif n == 3:
    return 7
  else:
    return arrangements(n-1) + arrangements(n-2) + arrangements(n-3)

def get_spacings(sorted_numbers):
  return [sorted_numbers[0]] + [y - x for x,y in zip(sorted_numbers, sorted_numbers[1:])]

# see https://stackoverflow.com/questions/6352425/whats-the-most-pythonic-way-to-identify-consecutive-duplicates-in-a-list
def count_blocks_of_ones(spacings):
  return [sum(1 for i in g) for k,g in groupby(spacings) if k==1]

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    all_numbers = []
    for line in input:
      num = int(line)
      all_numbers.append(num)
    spacings = count_gaps(sorted(all_numbers))
    # star 1:
    print(spacings)
    print('1-gaps * 3-gaps = {}'.format((spacings[1]+1)*(spacings[3]+1)))
    #star 2:
    print('------------------------------------')
    spacings = get_spacings(sorted(all_numbers))
    block_lengths = [x-1 for x in count_blocks_of_ones(spacings)]
    total_num_arrangements = math.prod([arrangements(n) for n in block_lengths])
    print('Total number of arrangements: {}'.format(total_num_arrangements))

if __name__ == "__main__":
  main()