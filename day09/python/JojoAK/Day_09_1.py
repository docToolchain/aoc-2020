PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()

sums = []
k=0

for j in range(len(txt)):
    for i in range(25):
        for k in range(25):
            if i == k:
                continue
            else:
                sums.append(int(txt[i])+int(txt[k]))
            
    if int(txt[25]) in sums:
        txt.pop(0)
        sums = []       
    else:
        print(int(txt[25]),"is not a sum of 2 of the previous 25 numbers")
        break