import collections

class CupClass():
    def __init__(self, id):
        self.id = id
        self.next = None

def problem1(puzzle_input,rounds):
    cups = collections.deque([int(i) for i in puzzle_input],len(puzzle_input))
    current_cup = cups[0]
    length = len(cups)

    for move in range(1,rounds+1):
        cups.rotate(-1)
        cups_to_move = [cups.popleft() for n in range(3)]
        ind = (current_cup-1)%(length+1)
        while ind == 0 or ind in cups_to_move:
            ind = (ind-1)%(length+1)
        insert_ind = cups.index(ind)
        for i in range(3):
            cups.insert(insert_ind+i+1,cups_to_move[i])
        current_cup = cups[0]

    one_ind = cups.index(1)
    cups.rotate(length - one_ind)
    cups.popleft()

    problem1 = str(cups[0])
    for i in range(1,8):
        problem1 += (str(cups[i]))

    return problem1



def main():

    puzzle_input = str(476138259)

    print("The labels on the cups after cup 1 are",problem1(puzzle_input,100))

    # create Cups
    cups_dictionary = dict()
    for digit in puzzle_input:
        temp_cup = CupClass(int(digit))
        cups_dictionary[int(digit)] = temp_cup
    for i in range(10,1000001):
        temp_cup = CupClass(i)
        cups_dictionary[i] = temp_cup

    # Link the cups
    for i in range(len(puzzle_input)-1):
        cups_dictionary[int(puzzle_input[i])].next = cups_dictionary[int(puzzle_input[i+1])]
    cups_dictionary[int(puzzle_input[8])].next = cups_dictionary[10]
    for i in range(10, 1000000):
        cups_dictionary[i].next = cups_dictionary[i+1]
    cups_dictionary[1000000].next = cups_dictionary[int(puzzle_input[0])]

    current_cup = cups_dictionary[int(puzzle_input[0])]

    for move in range(1, 10000001):
        cups_to_move = [current_cup.next.id, current_cup.next.next.id, current_cup.next.next.next.id]
        current_cup.next = current_cup.next.next.next.next
        ind = (current_cup.id - 1)
        if ind == 0: ind = 1000000
        while ind in cups_to_move:
            ind -= 1
            if ind == 0: ind = 1000000
        cups_dictionary[cups_to_move[2]].next = cups_dictionary[ind].next
        cups_dictionary[ind].next = cups_dictionary[cups_to_move[0]]
        current_cup = current_cup.next

    ones_cup = cups_dictionary[1]
    print(ones_cup.id)
    print(ones_cup.next.id)
    print(ones_cup.next.next.id)

    print(ones_cup.next.id*ones_cup.next.next.id)

main()