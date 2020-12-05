PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()
seatID = []
missingSeatID = 0

for i in txt:
    binary = i.replace("F", "0")
    binary = binary.replace("B", "1")
    binary = binary.replace("L", "0")
    binary = binary.replace("R", "1")

    row = int(binary[:7],2)
    seat = int(binary[7:],2)

    seatID.append(row*8 + seat)

seatID.sort()

for i in range(len(seatID)-1):
    if seatID[i]+1 != seatID[i+1]:
        missingSeatID = seatID[i]+1
        print("My seat has the seat ID", missingSeatID)