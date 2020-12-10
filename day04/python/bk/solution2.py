import re
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
        for attr, value in passport.__dict__.items():
            if self.__validateField(attr, value) == False:
                return False
        return True
    def __validateField(self, attr, value):
        if attr != "cid" and value == "" :
                return False
        if attr == "byr":
            if value.isnumeric() == False or int(value) < 1920 or int(value) > 2002:
                return False
        if attr == "iyr":
            if value.isnumeric() == False or int(value) < 2010 or int(value) > 2020:
                return False
        if attr == "eyr":
            if value.isnumeric() == False or int(value) < 2020 or int(value) > 2030:
                return False
        if attr == "hgt":
            if self.__validateHight(value) == False:
                return False
        if attr == "hcl":
            if re.search("^#[a-fA-F0-9]{6}$", value) == None:
                return False            
        if attr == "ecl":
            if value != "amb" and value != "blu" and value != "brn" and value != "gry" and value != "grn" and value != "hzl" and value != "oth":
                return False
        if attr == "pid":
            #if re.search("^0\d{8}$", value) == None:
            if re.search("^\d{9}$", value) == None:
                return False
        return True
    def __validateHight(self, value):
        size = int(value[0:len(value)-2])
        unit = value[len(value)-2:len(value)]
        if unit == "cm":
            if size >= 150 and size <= 193:
                return True
        if unit == "in":
            if size >= 59 and size <= 76:
                return True
        return False

f = open("input.txt", "r")
data=f.readlines()
parser=Parser(data)
passports=parser.getPassports()
v = Validator()
print("Answer 2: {}".format(v.countValidPassports(passports)))