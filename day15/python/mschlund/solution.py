def get_next_number_naive(numbers):
  current_number = numbers[-1]
  turns_with_num = [i+1 for i in range(len(numbers)-1) if numbers[i] == current_number]
  if turns_with_num == []:
    return 0
  else:
    return abs(turns_with_num[-1] - len(numbers))

def get_next_number_lookup(number, spoken_in_turn, last_turn):
  if not number in spoken_in_turn:
    spoken_in_turn[number] = last_turn
    return spoken_in_turn, 0
  else:
    next_num = last_turn - spoken_in_turn[number]
    spoken_in_turn[number] = last_turn
  return spoken_in_turn, next_num

# tag::main[]
def main():
  #starting_numbers = [0,3,6]
  starting_numbers = [8,0,17,4,1,12]
  # star 1:
  numbers = starting_numbers.copy()
  N = 2020
  for i in range(N-len(starting_numbers)):
    next_num = get_next_number_naive(numbers)
    numbers.append(next_num)
  #print(numbers)
  print('Last number: {}'.format(numbers[-1]))

  print('--------------------------')
  N=30000000
  # star 2:
  spoken_in_turn = {x : i+1 for i,x in enumerate(starting_numbers[:-1])}
  new_number = starting_numbers[-1]
  #numbers_2 = starting_numbers.copy()
  for i in range(N - len(starting_numbers)):
    last_turn = len(starting_numbers) + i
    #print('Last turn: {}'.format(last_turn))
    #print('Last number: {}'.format(new_number))
    spoken_in_turn, new_number = get_next_number_lookup(new_number, spoken_in_turn, last_turn)
    #print(len(spoken_in_turn))
    #numbers_2.append(new_number)

  print('Last number: {}'.format(new_number))

  #print(numbers_2)
  #print(max(numbers_2))
# end::main[]

if __name__ == "__main__":
  main()
