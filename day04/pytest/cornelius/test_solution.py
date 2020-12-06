from pathlib import Path
import re

#tag::parse_passports[]
def parse_passports(passport_data):
    passports = []
    for passport_str in passport_data.split("\n\n"):
        passport_str = passport_str.replace("\n", " ")
        fields = passport_str.split()
        passport = {}
        for field in fields:
            passport[field[0:3]] = field[4:]
        passports.append(passport)
    return passports
#end::parse_passports[]

#tag::test_star1[]
example_input = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

def test_example1():
    assert count_valid_passports(example_input, check_fields=False) == 2
#end::test_star1[]

#tag::count_valid_passports[]
def count_valid_passports(input_data, check_fields):
    passports = parse_passports(input_data)
    valid_count = 0
    for passport in passports:
        if is_valid_passport(passport, check_fields):
            valid_count += 1
    return valid_count

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

def is_valid_passport(passport, check_fields=False):
    for required_field in required_fields:
        if not required_field in passport:
            return False
        if check_fields:
            for key in passport:
                if not is_valid_field(key, passport[key]):
                    return False
    return True
#end::count_valid_passports[]

#tag::star1[]
def read_input():
    with Path("input.txt").open() as f:
        return f.read()

puzzle_input = read_input()

def test_answer1():
    assert count_valid_passports(puzzle_input, check_fields=False) == 204
#end::star1[]

#tag::test_star2[]
valid_passports = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

invalid_passports = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

def test_is_valid_passport():
    passports = parse_passports(example_input)

    assert is_valid_passport(passports[0]) == True
    assert is_valid_passport(passports[1]) == False
    assert is_valid_passport(passports[2]) == True
    assert is_valid_passport(passports[3]) == False

    passports = parse_passports(valid_passports)
    for passport in passports:
        assert is_valid_passport(passport, check_fields=True)

    passports = parse_passports(invalid_passports)
    for passport in passports:
        assert not is_valid_passport(passport, check_fields=True)

def test_is_valid_field():
    assert is_valid_field("byr", "2002")
    assert not is_valid_field("byr", "2003")

    assert is_valid_field("iyr", "2010")
    assert not is_valid_field("iyr", "2009")

    assert is_valid_field("eyr", "2025")
    assert not is_valid_field("eyr", "2035")

    assert is_valid_field("hgt","60in")
    assert is_valid_field("hgt","190cm")
    assert not is_valid_field("hgt","190in")
    assert not is_valid_field("hgt","190")

    assert is_valid_field("hcl","#123abc")
    assert not is_valid_field("hcl","#123abz")
    assert not is_valid_field("hcl","123abc")

    assert is_valid_field("ecl","brn")
    assert not is_valid_field("ecl","wat")

    assert is_valid_field("pid","000000001")
    assert not is_valid_field("","0123456789")
#end::test_star2[]

#tag::check_fields[]
def parse_year(string):
    m = re.search(r"^(\d\d\d\d)$", string)
    if not m:
        return -1
    else:
        return int(m.group(1))

def parse_height(string):
    m = re.search(r"^(\d+)(cm|in)$", string)
    if not m:
        return -1, None
    else:
        return int(m.group(1)), m.group(2)

def is_valid_field(key, value):
    if key == "byr":
        year = parse_year(value)
        return year >= 1920 and year <= 2002
    elif key == "iyr":
        year = parse_year(value)
        return year >= 2010 and year <= 2020
    elif key == "eyr":
        year = parse_year(value)
        return year >= 2020 and year <= 2030
    elif key == "hgt":
        height, unit = parse_height(value)
        if unit == "cm":
            return height >= 150 and height <= 2023
        elif unit == "in":
            return height >= 59 and height <= 76
        else:
            return False
    elif key == "hcl":
        m = re.search(r"^#[0-9a-f]{6}$", value)
        return bool(m)
    elif key == "ecl":
        valid_colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        return value in valid_colors
    elif key == "pid":
        m = re.search(r"^\d{9}$", value)
        return bool(m)
    elif key == "cid":
        return True
    return False
#end::check_fields[]

#tag::star2[]
def test_answer2():
    assert count_valid_passports(puzzle_input, check_fields=True) == 179
#end::star2[]
