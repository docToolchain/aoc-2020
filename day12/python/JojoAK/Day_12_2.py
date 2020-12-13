import math
PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()

xcoord = 0
ycoord = 0
xwp = 10
ywp = 1
quad = 0

for i in txt:
    action = i[:1]
    value = int(i[1:])
    
    if action == "N":
        ywp = ywp + value
    elif action == "S":
        ywp = ywp - value
    elif action == "E":
        xwp = xwp + value
    elif action == "W":
        xwp = xwp - value
    elif action == "L":
        value = math.radians(value)
        temp = xwp
        xwp = xwp*math.cos(value)-ywp*math.sin(value)
        ywp = temp*math.sin(value)+ywp*math.cos(value)
    elif action == "R":
        value = -1 * math.radians(value)
        temp = xwp
        xwp = xwp*math.cos(value)-ywp*math.sin(value)
        ywp = temp*math.sin(value)+ywp*math.cos(value)
    elif action == "F":
        xcoord = xcoord + value * xwp
        ycoord = ycoord + value * ywp

print("The manhattan distance is",abs(xcoord) + abs(ycoord))