import re

def getVersion():
    print("AoC2020_Day4!")


def read_file_to_list(filename):
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(line)
    file.close()
    return list

#part 1
def check_passport_content(data):
    required_content = {"ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"}
    optional = "cid"
    is_valid = True
    print("")
    for c in required_content:
        if c not in data:
            print("invalid: {} is missing in {}".format(c, data))
            is_valid = False
        else:
            #print("okay: {} in {}".format(c, data))
            pass

    if is_valid:
        print("valid: {}".format(data))

    return is_valid


#part 2
def check_passport_extended(data):
    required_content = {"ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"}

    key_error = 0
    is_valid = True

    passport_fields = {
        "ecl": "", # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        "pid": -1, # pid (Passport ID) - a nine-digit number, including leading zeroes.
        "eyr": -1, # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        "hcl": "", # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        "byr": -1, # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        "iyr": -1, # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        "hgt": -1, # hgt (Height) - a number followed by either cm or in:
                     # If cm, the number must be at least 150 and at most 193.
                     # If in, the number must be at least 59 and at most 76.
        "cid": -1  # cid (Country ID) - ignored, missing or not.
    }

    #data[data.find("ecl:")
    content = data.split()
    #print(content)

    for c in content:
        key , val = c.split(":")
        #print("key: {}, value: {}".format(key, val))
        if key in passport_fields:
            passport_fields[key] = val
        else:
            key_error += 1

    if key_error > 0:
        print("key_error: {}".format(key_error))
        is_valid = False

    print(passport_fields)

    #https://www.w3schools.com/python/python_regex.asp

    if re.match(r"[0-9]{9}\b", passport_fields["pid"]):
        print('pid valid: {}'.format(passport_fields["pid"]))
    else:
        print('pid invalid: {}'.format(passport_fields["pid"]))
        is_valid = False

    exp = re.compile('(amb|blu|brn|gry|grn|hzl|oth)')
    match_list = re.findall(exp, passport_fields["ecl"])
    print(type(match_list)) #==> list
    if len(match_list) == 1 and len(passport_fields["ecl"]) == 3:
        print('ecl valid: {}'.format(passport_fields["ecl"]))
    else:
        print("match: {}".format(match_list))
        print('ecl invalid: {}'.format(passport_fields["ecl"]))
        is_valid = False

    # "ecl": "",  # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # "pid": -1,  # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # "eyr": -1,  # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # "hcl": "",  # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # "byr": -1,  # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # "iyr": -1,  # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # "hgt": -1,  # hgt (Height) - a number followed by either cm or in:
    # # If cm, the number must be at least 150 and at most 193.
    # # If in, the number must be at least 59 and at most 76.
    # "cid": -1  # cid (Country ID) - ignored, missing or not.

    is_valid = False
    print("")
    return is_valid