from pathlib import Path
from functools import reduce
import typer


PASSPORT_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    lines = list(map(lambda s: s.strip(), lines))
    return lines


def split_input(lines):
    data = []
    passport = ""

    for line in lines:
        if line != "":
            passport = passport + " " + line
        else:
            data.append(passport.split())
            passport = ""
    data.append(passport.split())

    return data


def build_passport(key_value_list):
    passport = dict()
    for key_value in key_value_list:
        key, value = key_value.split(":")
        passport[key] = value
    return passport


def build_passports(data):
    passports = list(map(lambda e: build_passport(e), data))
    return passports


def puzzle_input(input_file):
    return build_passports(split_input(read_input_file(input_file)))


def check_required_fields(passport):
    checked_passport = dict(passport)
    checked_passport["valid"] = all(k in checked_passport for k in PASSPORT_FIELDS)
    return checked_passport


def check_field_constraints(passport):
    """
    This function checks the following constraints:
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.

    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    """
    checked_passport = dict(passport)

    byr_valid = 1920 <= int(passport["byr"]) <= 2002
    iyr_valid = 2010 <= int(passport["iyr"]) <= 2020
    eyr_valid = 2020 <= int(passport["eyr"]) <= 2030

    hgt_valid = False
    if len(passport["hgt"]) > 2:
        hgt_value = int(passport["hgt"][:-2])
        hgt_unit = passport["hgt"][-2:]
        if hgt_unit == "cm":
            hgt_valid = 150 <= hgt_value <= 193
        else:
            hgt_valid = 59 <= hgt_value <= 76

    hcl_valid = (passport["hcl"][0] == "#") \
            and len(passport["hcl"]) == 7
    ecl_valid = passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    pid_valid = len(passport["pid"]) == 9 and passport["pid"].isdigit()

    checked_passport["valid"] = all([byr_valid, iyr_valid, eyr_valid, hgt_valid, hcl_valid, ecl_valid, pid_valid])
    return checked_passport


def filter_valid_passports(passports):
    return list(filter(lambda p: p["valid"], passports))


@app.command()
def part1(input_file: str):
    passports = puzzle_input(input_file)
    passports = map(lambda p: check_required_fields(p), passports)
    valid_passports = filter_valid_passports(passports)

    print(f"The number of passports containing all required fields is {len(valid_passports)}.")


@app.command()
def part2(input_file: str):
    passports = puzzle_input(input_file)
    passports = map(lambda p: check_required_fields(p), passports)
    passports = list(filter(lambda p: p["valid"], passports))
    passports = map(lambda p: check_field_constraints(p), passports)
    valid_passports = filter_valid_passports(passports)

    print(f"The number of passports with valid constraints is {len(valid_passports)}.")


if __name__ == "__main__":
    app()
