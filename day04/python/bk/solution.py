class Passport:
    def __init__(self, data):
        self.byr=""
        self.iyr=""
        self.eyr=""
        self.hgt=""
        self.hcl=""
        self.ecl=""
        self.pid=""
        self.cid=""
        self.__readData(data)
    def __readData(self, data):
        fields = data.split()
        for field in fields:
            splittedField = field.split(":")
            self.__dict__[splittedField[0]] = splittedField[1]

class Parser:
    def __init__(self, data):
        self.passports=[]
        self.__parse(data)
    def __parse(self, data):
        passportString = ""
        for d in data:
            if not d.strip():
                if len(passportString) > 0:
                    p = Passport(passportString)
                    self.passports.append(p)                    
                passportString=""
            else:
                passportString+=d
        if len(passportString) > 0:
            p = Passport(passportString)
            self.passports.append(p) 
    def getPassports(self):
        return self.passports

class Validator:
    def countValidPassports(self, passports):
        validPassports=0
        for p in passports:
            if self.__validate(p):
                validPassports+=1
        return validPassports
    def __validate(self, passport):
        isValid=True
        for attr, value in passport.__dict__.items():
            if attr != "cid" and value == "" :
                isValid=False
                break
        return isValid


f = open("input.txt", "r")
data=f.readlines()
parser=Parser(data)
passports=parser.getPassports()
#print(len(passports))
v = Validator()
print("Answer 1: {}".format(v.countValidPassports(passports)))