PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()
txt.append("\n")

ansgroup = ""
count = 0

for i in txt:
    if i != "\n":
        ansgroup = ansgroup + i.replace("\n","")
        
    elif i == "\n":        
        ansgroup = set(ansgroup)
        count = count + len(ansgroup)
        ansgroup = ""
        
print("The sum of counts is" ,count)