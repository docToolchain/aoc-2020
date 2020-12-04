PuzzleInput = "PuzzleInput.txt"

f = open(PuzzleInput)
txt = f.readlines()
numbers = 0
splitnumbers = []
minnr = 0
maxnr = 0
letter = 0
line = ""
splitline = []
password = ""
result = 0

for i in range(len(txt)):    
    line = txt[i]
    
    splitline = line.split()
    numbers = splitline[0]
    splitnumbers = numbers.split("-")
    minnr = int(splitnumbers[0])
    maxnr = int(splitnumbers[1])
    letter = splitline[1]
    letter = letter[:-1]
    password = splitline[2]
    
    if password[minnr-1] == letter and password[maxnr-1] != letter:
        result = result+1
    if password[minnr-1] != letter and password[maxnr-1] == letter:
        result = result+1
                            
print("The result is:", result)