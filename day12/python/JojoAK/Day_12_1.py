PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()

xcoord = 0
ycoord = 0
heading = 0

for i in txt:
    action = i[:1]
    value = int(i[1:])
    heading = heading % 360
    
    if action == "N":
        ycoord = ycoord + value
    elif action == "S":
        ycoord = ycoord - value
    elif action == "E":
        xcoord = xcoord + value
    elif action == "W":
        xcoord = xcoord - value
    elif action == "L":
        heading = heading - value
    elif action == "R":
        heading = heading + value
    elif action == "F":
        if heading == 0:
            ycoord = ycoord + value
        elif heading == 90:
            xcoord = xcoord + value
        elif heading == 180:
            ycoord = ycoord - value
        elif heading == 270:
            xcoord = xcoord - value

print("The manhatten distance is",abs(xcoord)+abs(ycoord))