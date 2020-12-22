
def get_numbers_for_game():
    turn = 0
    numbers = {}
    last_value = int(input("Please provide number (q if enough): "))
    while True:
        user_input = input("Please provide number (q if enough): ")
        if user_input == 'q':
            break
        numbers[last_value] = turn
        last_value = int(user_input)
        turn += 1
    return numbers, last_value

def get_number_of_turns():
    number_of_turns = int(input("How many turns to play: "))
    return number_of_turns

def play_game(numbers, number_of_turns, last_value):
    for turn in range(len(numbers),(number_of_turns-1)):
        numbers.get(last_value)
        if numbers.get(last_value) == None:
            new_last_value = 0
        else:
            new_last_value = turn - numbers.get(last_value)
        numbers[last_value] = turn
        last_value = new_last_value
    return last_value

def play_game_old(numbers, number_of_turns):
    for turn in range(len(numbers),number_of_turns):
        if numbers.count(numbers[-1]) == 1:
            numbers.append(0)
        else:
            numbers.append(numbers[-2::-1].index(numbers[-1]) + 1)
    return numbers[-1]

numbers, last_value = get_numbers_for_game()
number_of_turns = get_number_of_turns()

print(f"The {number_of_turns}th number spoken is {play_game(numbers, number_of_turns, last_value)}")
