PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()
seatID = 0

for i in txt:
    binary = i.replace("F", "0")
    binary = binary.replace("B", "1")
    binary = binary.replace("L", "0")
    binary = binary.replace("R", "1")
    
    row = int(binary[:7],2)
    seat = int(binary[7:],2)
    
    if seatID < row*8 + seat:
        seatID = row*8 + seat
    
print("The highest seat ID is:", seatID)