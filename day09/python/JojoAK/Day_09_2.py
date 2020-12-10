PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()

summe = 0
i=0
result = []

while summe != 2089807806:
    if summe < 2089807806:
        summe = summe + int(txt[i])
        i=i+1
    elif summe > 2089807806:
        i = 0
        summe = 0
        txt.pop(0)

for k in range(i-1):
    result.append(int(txt[k]))
print("The encryption weakness is:", max(result) + min(result))