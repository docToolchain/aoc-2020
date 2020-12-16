import re
import logging

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
logging.basicConfig(level=logging.NOTSET) #https://docs.python.org/3/library/logging.html#levels
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
#CRITICAL 50
#ERROR    40
#WARNING  30
#INFO     20
#DEBUG    10
#NOTSET    0
#log.info('info message')
#log.critical('critical message')
#log.debug('debug message')
#log.warning('warning message')
#log.error('error message')

def getVersion():
    log.debug("AoC2020_Day4!")


def read_file_to_list(filename):
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(line)
    file.close()
    return list


# part 1
def check_passport_content(data):
    required_content = {"ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"}
    optional = "cid"
    is_valid = True
    for c in required_content:
        if c not in data:
            log.debug("invalid: {} is missing in {}".format(c, data))
            return False
        else:
            # log.debug("okay: {} in {}".format(c, data))
            pass

    if is_valid:
        log.debug("valid: {}".format(data))

    return is_valid


# part 2
def check_passport_extended(data):
    required_content = {"ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"}

    key_error = 0
    passport_fields = {
        "ecl": "",  # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        "pid": "",  # pid (Passport ID) - a nine-digit number, including leading zeroes.
        "eyr": "",  # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        "hcl": "",  # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        "byr": "",  # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        "iyr": "",  # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        "hgt": "",  # hgt (Height) - a number followed by either cm or in:
        # If cm, the number must be at least 150 and at most 193.
        # If in, the number must be at least 59 and at most 76.
        "cid": ""  # cid (Country ID) - ignored, missing or not.
    }

    # data[data.find("ecl:")
    content = data.split()
    # log.debug(content)

    for c in content:
        key, val = c.split(":")
        # log.debug("key: {}, value: {}".format(key, val))
        if key in passport_fields:
            passport_fields[key] = val
        else:
            key_error += 1

    if key_error > 0:
        log.debug("key_error: {}".format(key_error))
        return False

    log.debug(passport_fields)

    # https://www.w3schools.com/python/python_regex.asp

    # "pid": -1,  # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if re.match(r"^[0-9]{9}$", passport_fields["pid"]):
        log.debug('pid valid: {}'.format(passport_fields["pid"]))
    else:
        log.debug('pid invalid: {}'.format(passport_fields["pid"]))
        return False

    # "ecl": "",  # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    exp = re.compile('^(amb|blu|brn|gry|grn|hzl|oth){1}$')
    match_list = re.findall(exp, passport_fields["ecl"])
    log.debug("match: {}".format(match_list))
    log.debug(type(match_list))  # ==> list
    if len(match_list) == 1 and len(passport_fields["ecl"]) == 3:
        log.debug('ecl valid: {}'.format(passport_fields["ecl"]))
    else:
        log.debug("match: {}".format(match_list))
        log.debug('ecl invalid: {}'.format(passport_fields["ecl"]))
        return False

    # "eyr": -1,  # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if re.match(r"^[0-9]{4}$", passport_fields["eyr"]):
        log.debug('eyr: {}'.format(passport_fields["eyr"]))
        if 2020 <= int(passport_fields["eyr"]) <= 2030:
            log.debug('eyr valid')
        else:
            log.debug('eyr invalid')
            return False
    else:
        log.debug('eyr invalid: {}'.format(passport_fields["eyr"]))
        return False

    # "hcl": "",  # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if re.match(r"^#[a-f0-9]{6}$", passport_fields["hcl"]):
        log.debug('hcl valid: {}'.format(passport_fields["hcl"]))
    else:
        log.debug('hcl invalid: {}'.format(passport_fields["hcl"]))
        return False

    # "byr": -1,  # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if re.match(r"^[0-9]{4}$", passport_fields["byr"]):
        log.debug('byr: {}'.format(passport_fields["byr"]))
        if 1920 <= int(passport_fields["byr"]) <= 2002:
            log.debug('byr valid')
        else:
            log.debug('byr invalid')
            return False
    else:
        log.debug('byr invalid: {}'.format(passport_fields["byr"]))
        return False

    # "iyr": "",  # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if re.match(r"^[0-9]{4}$", passport_fields["iyr"]):
        log.debug('iyr: {}'.format(passport_fields["iyr"]))
        if 2010 <= int(passport_fields["iyr"]) <= 2020:
            log.debug('iyr valid')
        else:
            log.debug('iyr invalid')
            return False
    else:
        log.debug('iyr invalid: {}'.format(passport_fields["iyr"]))
        return False

    # "hgt": "",  # hgt (Height) - a number followed by either cm or in:
    # # If cm, the number must be at least 150 and at most 193.
    # # If in, the number must be at least 59 and at most 76.
    # "cid": ""  # cid (Country ID) - ignored, missing or not.
    #exp = re.compile('^([0-9]+)(in|cm){1}$')
    #match_list = re.findall(exp, passport_fields["hgt"])
    #log.debug("match: {}".format(match_list))
    #log.debug(type(match_list))  # ==> list

    m = re.search("^([0-9]+)(in|cm)$", passport_fields['hgt'])
    log.debug("match: {}".format(m))
    log.debug(type(m))  # ==> list
    if not m:
        return False
    hgt = int(m.group(1))
    if m.group(2) == 'cm':
        if hgt < 150 or hgt > 193:
            return False
    else:
        if hgt < 59 or hgt > 76:
            return False

    return True
