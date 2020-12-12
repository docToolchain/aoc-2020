PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()
txt = map(int, txt)
txt = sorted(txt)

dif1 = 0
dif2 = 0
dif3 = 0
difs = []
start = 0
end = 0
block = 0
blocksof1 = []
combinations = 1

for i in range(len(txt)-1):
    if i == 0:
        if txt[i] == 1:
            dif1 = dif1 + 1
            difs.append(1)
        elif txt[i] == 2:
            dif2 = dif2 + 1
            difs.append(2)
        elif txt[i] == 3:
            dif3 = dif3 + 1
            difs.append(3)
        else:
            continue
        
    if txt[i+1]-1 == txt[i]:      
        dif1 = dif1 + 1
        difs.append(1)
    elif txt[i+1]-2 == txt[i]:
        difs.append(2)
    elif txt[i+1]-3 == txt[i]:
        dif3 = dif3 + 1
        difs.append(3)
    else:
        break

dif3 = dif3 + 1
difs.append(3)

print("1st star: The result is:",dif1*dif3)

for i in range(len(difs)-1):
    if difs[i] == 3 and difs[i+1] == 1:
        start = i+1
    if difs[i] == 1 and difs[i+1] == 3:
        end = i
        block = end-start
        blocksof1.append(block)

for i in range(len(blocksof1)):
    if blocksof1[i] == 3:
        blocksof1[i] = 7
    else:
        blocksof1[i] = 2**blocksof1[i]
    
    combinations = combinations * blocksof1[i]

print("2nd star: There are",combinations,"combinations")