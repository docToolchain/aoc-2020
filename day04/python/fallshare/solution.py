from pathlib import Path
import re


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        #split entries by blankline
        raw_entries = f.read().split("\n\n")

        passports = []
        #normalize entries by removing newlines and splitting up key value pairs
        for raw_entry in raw_entries:
            #normalize entry by removing new lines
            normalized_entry = raw_entry.split()

            passport = dict()
            #store splitted key value pairs in dictionary
            for field in normalized_entry:
                key, value = field.split(":")
                passport[key] = value

            passports.append(passport)  

    return passports


def get_passports_with_required_fields(passports):
    required_fields = {"byr","iyr","eyr","hgt", "hcl", "ecl", "pid"}

    valid_passports = []
    for passport in passports:
        #the password field must contain all required fields. Hence the required keys must be a subset of the fields in the passport
        if required_fields.issubset(passport.keys()):
           valid_passports.append(passport)

    return valid_passports

def checkHeight(data):

    unit = data[-2:]
    if(unit == "cm" or unit == "in"):
        value = int(data[:-2])
        
    else:
        return False
        
    if unit == "cm":
        if 150 <= value <= 193:
            return True
    if unit == "in":
        if 59 <= value <= 76:
            return True
    
    return False

def checkEyeColor(eyecolor):
    valid_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    
    if eyecolor in valid_colors:
        return True
    else:
        return False

    return False

def get_passports_with_valid_entries(passports):
    valid_passports = []

    for passport in passports:
        if      int(passport["byr"]) in range(1920, 2002 + 1) \
            and int(passport["iyr"]) in range(2010, 2020 + 1) \
            and int(passport["eyr"]) in range(2020, 2030 + 1) \
            and checkHeight(passport["hgt"])\
            and re.findall("#[0-9a-f]{6}",passport["hcl"]) \
            and checkEyeColor(passport["ecl"])\
            and re.findall("^\d{9}$",passport["pid"]):

                valid_passports.append(passport)


    return valid_passports


if __name__ == "__main__":

    passports = read_input_file('input.txt')

    valid_passports = get_passports_with_required_fields(passports)
    print(f"Star 1: {len(valid_passports)} passports with all required fields found.")
    valid_entry_passports = get_passports_with_valid_entries(valid_passports)
    print(f"Star 2: {len(valid_entry_passports)} passports with all required fields and entries found.")