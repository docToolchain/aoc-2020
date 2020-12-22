
def process_input(file_contents):
    deck1 = list()
    i = 1
    while file_contents[i] != "\n":
        deck1.append(int(file_contents[i].strip()))
        i += 1

    deck2 = list()
    for line in file_contents[i+2:]:
        deck2.append(int(line.strip()))

    return deck1, deck2

def combat(deck1,deck2):
    while len(deck1) != 0 and len(deck2) != 0:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            winner = 1
            deck1.append(card1)
            deck1.append(card2)
        else:
            winner = 2
            deck2.append(card2)
            deck2.append(card1)

    if winner == 1: return deck1
    else: return deck2

def recursive_combat(deck1,deck2,level):
    constellations = [(deck1.copy(),deck2.copy())]
    while len(deck1) != 0 and len(deck2) != 0:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner = recursive_combat(deck1[:card1],deck2[:card2],1)
        elif card1>card2: winner = 1
        else: winner = 2
        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
        if (deck1, deck2) in constellations:
            winner = 1
            break
        else: constellations.append((deck1.copy(),deck2.copy()))

    if level == 0:
        if winner == 1: return deck1
        else: return deck2
    if level == 1:
        return winner

def calculate_score(deck):
    count = 0
    for i,value in enumerate(reversed(deck)):
        count += (i+1)*value

    return count

def main():
    with open("cards.txt",'r') as code_file:
        all_code_file = code_file.readlines()

    deck1, deck2 = process_input(all_code_file)

    # Problem 1
    winning_deck = combat(deck1.copy(),deck2.copy())
    print("The winning player's score for problem 1 is", calculate_score(winning_deck))

    # Problem 2
    winning_deck = recursive_combat(deck1.copy(),deck2.copy(),0)
    print("The winning player's score for problem 2 is", calculate_score(winning_deck))

main()