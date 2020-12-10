class BoardingPassScanner:
    def __init__(self, data):
        self.__data=data
        self.__boardingPasses=[]
        self.__parse()
    def __parse(self):
        for d in data:
            bP = BoardingPass(d)
            #print(bP.getRow())
            self.__boardingPasses.append(bP)        
    def getBoardingPassesWithHighestSeatId(self):
        currentSeatId=0
        for p in self.__boardingPasses:
            #print("{}: Row: {}, Column: {}".format(p.getData(), p.getRow(), p.getColumn()))
            if p.getId() > currentSeatId:
                currentSeatId = p.getId()   
        return currentSeatId

class BoardingPass:
    def __init__(self,data):
        self.__data=data
        self.__row=0
        self.__column=0
        self.__id=0
        self.__passId=0
        self.__parse()
    def __parse(self):
        rowLetters=self.__data[0:7]
        columnLetters=self.__data[7:10]
        self.__row=self.__calcRow(rowLetters)
        self.__column=self.__calcColumn(columnLetters)
        self.__passId=self.__row*8+self.__column
    def __calcRow(self, rowLetters):
        return self.__calc(rowLetters,"F", 127)
    def __calcColumn(self, columnLetters):
        return self.__calc(columnLetters,"L", 7)
    def __calc(self, letters, lowerHalfLetter, count):
        upper=count
        lower=0
        for r in letters:            
            if r==lowerHalfLetter:
                upper=upper-(upper+1-lower)/2
            else:
                lower=lower+(upper+1-lower)/2 
        return upper
    def getId(self):
        return self.__passId
    def getRow(self):
        return self.__row
    def getColumn(self):
        return self.__column
    def getData(self):
        return self.__data

f=open("input.txt","r")
data=f.readlines()
scanner=BoardingPassScanner(data)
print("Answer 1: {}".format(scanner.getBoardingPassesWithHighestSeatId()))