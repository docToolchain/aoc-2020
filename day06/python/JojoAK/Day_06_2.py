PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()
txt.append("\n")

ansgroup = ""
distans = ""
count = 0
k=0
j=""

for i in range(len(txt)):
    if txt[i] != "\n":
        ansgroup = ansgroup + txt[i].replace("\n","")
        k = k+1
        
    elif txt[i] == "\n":
        firstans = txt[i-k].replace("\n","")
        for j in firstans:
            if ansgroup.count(j) == k:
                count = count + 1
            else:
                None
        ansgroup = ""
        k=0
        
print("The sum of counts is" ,count)