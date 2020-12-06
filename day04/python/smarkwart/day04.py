import sys
import re

def get_input_data_as_list(file_name):
    """ Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed """
    with open(file_name) as input_file:
        #data_list = map(str.strip,input_file.readlines())
        data_list = input_file.readlines()
    return data_list

def get_passports_from_file(file_name):
    """
    Generates a list of passports from given file
    """
    raw_passports = get_input_data_as_list(sys.argv[1])
    passports = create_passport_list_from_raw_data(raw_passports)

    return passports

def create_passport_list_from_raw_data(raw_passports):
    """
    Creates a list of passports where each passwort is a dictionary
    """
    passport_dicts = []
    new_passport = ""
    for line in raw_passports:
        if line.strip() != '':
            new_passport += line.strip()
            new_passport += ' '
        else:
            passport_dicts.append(translate_passport_into_dict(new_passport))
            new_passport = ""

    #in case data does not end with newline there might be unprocessed password data
    if new_passport != "":
        passport_dicts.append(translate_passport_into_dict(new_passport))
        new_passport = ""
    return passport_dicts

def translate_passport_into_dict(passport_line):
    passport_line = passport_line.strip()
    passport_dict = dict(key_value.split(":") for key_value in passport_line.split(" "))
    return passport_dict

def validate_passports(passports):
    """
    Validate the passports and returns the number of valid ones
    """
    valid_passports_star1 = 0
    valid_passports_star2 = 0
    for passport in passports:
        valid_passports_star1 += validate_passport_star1(passport)
        valid_passports_star2 += validate_passport_star2(passport)
    return valid_passports_star1, valid_passports_star2

def validate_passport_star1(passport):
    """
    Validate a single passport against required keys. returns 1 if valid otherwise 0
    """
    required_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for key in required_keys:
        if passport.get(key) == None:
            return False
    return True

def validate_passport_star2(passport):
    """
    Validate a single passport against the more strict rules
    """
    return (
        byr_valid(passport) and 
        iyr_valid(passport) and 
        eyr_valid(passport) and 
        hgt_valid(passport) and 
        hcl_valid(passport) and 
        ecl_valid(passport) and 
        pid_valid(passport)
        )

def byr_valid(passport):
    """
    Validate birth year
    """
    byr = passport.get('byr')
    if byr != None and is_four_digit_number(byr):
        return 1920 <= int(byr) and int(byr) <= 2002
    return False

def iyr_valid(passport):
    """
    Validate issue year
    """
    iyr = passport.get('iyr')
    if iyr != None and is_four_digit_number(iyr):
        return 2010 <= int(iyr) and int(iyr) <= 2020
    return False

def eyr_valid(passport):
    """
    Validate expiration year
    """
    eyr = passport.get('eyr')
    if eyr != None and is_four_digit_number(eyr):
        return 2020 <= int(eyr) and int(eyr) <= 2030
    return False

def hgt_valid(passport):
    """
    docstring
    """
    hgt = passport.get('hgt')
    if hgt != None:
        return valid_height_cm(hgt) or valid_height_in(hgt)
    return False

def hcl_valid(passport):
    """
    docstring
    """
    hcl = passport.get('hcl')
    if hcl != None:
        return valid_hair_color(hcl)
    return False

def ecl_valid(passport):
    """
    docstring
    """
    valid_eye_colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    ecl = passport.get('ecl')
    if ecl in valid_eye_colors:
        return True
    else:
        print(ecl)
        return False

def pid_valid(passport):
    """
    docstring
    """
    pid = passport.get('pid')
    return passport.get('pid') != None and is_nine_digit_number(pid)

def is_four_digit_number(string):
    """
    Checks if string is exactly four digits
    """
    matched = re.match(r"^\d{4}$", string)
    return bool(matched)

def is_nine_digit_number(string):
    """
    Checks if string is exactly four digits
    """
    matched = re.match(r"^\d{9}$", string)
    return bool(matched)

def valid_height_cm(height_string):
    """
    Check if height is valid in cm
    """
    match = re.match(r"^(\d*)(cm)$", height_string)
    if match:
        height_cm = int(match.group(1))
        if 150 <= height_cm and height_cm <= 193:
            return True
    return False

def valid_height_in(height_string):
    """
    Check if height is valid in in
    """
    match = re.match(r"^(\d*)(in)$", height_string)
    if match:
        height_in = int(match.group(1))
        if 59 <= height_in and height_in <= 76:
            return True
    return False

def valid_hair_color(hair_color):
    """
    Check if hair color is valid
    """
    matched = re.match(r"^#[0-9 a-f]{6}$", hair_color)
    return bool(matched)

passports = get_passports_from_file(sys.argv[1])
print(f"Valid passports found (easy rule, strict rule): {validate_passports(passports)}")
