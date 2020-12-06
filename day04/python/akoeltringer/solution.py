#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Solution of Problem of Day 04"""

# stdlib imports
import re
from typing import Callable, Dict, Iterable

# 3rd party lib imports

# own stuff
import utils


S_BYR = "byr"
S_IYR = "iyr"
S_EYR = "eyr"
S_HGT = "hgt"
S_HCL = "hcl"
S_ECL = "ecl"
S_PID = "pid"
KEYS = [S_BYR, S_IYR, S_EYR, S_HGT, S_HCL, S_ECL, S_PID]
HCL_PATTERN = re.compile(r"[#][0-9a-f]{6}")


def parse_passport_fields(passport: str) -> Dict[str, str]:
    """convert the string representation of a single passport to a dict"""
    fields = [f.split(":") for f in passport.replace("\n", " ").split(" ")]
    return {k: v for k, v in fields}


def parse_passports(passports_raw: str) -> Iterable[Dict[str, str]]:
    """separate the passports into a list and return them parsed (as dict)"""
    return map(parse_passport_fields, passports_raw.strip().split("\n\n"))


def has_all_keys(passport: Dict[str, str]) -> bool:
    """check if a passport entry has all keys"""
    return all(k in passport for k in KEYS)


def is_byr_valid(byr: str) -> bool:
    """Birth Year"""
    return 1920 <= int(byr) <= 2002


def is_iyr_valid(iyr: str) -> bool:
    """Issue Year"""
    return 2010 <= int(iyr) <= 2020


def is_eyr_valid(eyr: str) -> bool:
    """Expiration Year"""
    return 2020 <= int(eyr) <= 2030


def is_hgt_valid(hgt: str) -> bool:
    """Height"""
    return (hgt[-2:] == "cm" and (150 <= int(hgt[:-2]) <= 193)) or (
        hgt[-2:] == "in" and (59 <= int(hgt[:-2]) <= 76)
    )


def is_hcl_valid(hcl: str) -> bool:
    """Hair Color"""
    return HCL_PATTERN.fullmatch(hcl) is not None


def is_ecl_valid(ecl: str) -> bool:
    """Eye Color"""
    return ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def is_pid_valid(pid: str) -> bool:
    """Passport Id"""
    try:
        int(pid)
    except ValueError:
        return False
    else:
        return len(pid) == 9


def is_passport_valid_1(passport: Dict[str, str]) -> bool:
    """Check if passports are valid (part 1)"""
    return has_all_keys(passport)


VALIDATORS = {
    S_BYR: is_byr_valid,
    S_IYR: is_iyr_valid,
    S_EYR: is_eyr_valid,
    S_HGT: is_hgt_valid,
    S_HCL: is_hcl_valid,
    S_ECL: is_ecl_valid,
    S_PID: is_pid_valid,
}


def is_passport_valid_2(passport: Dict[str, str]) -> bool:
    """Check if passports are valid (part 2)"""
    return has_all_keys(passport) and all(f(passport[k]) for k, f in VALIDATORS.items())


def count_valid_passports(
    validation_func: Callable, passports: Iterable[Dict[str, str]]
) -> int:
    """count the valid passports (those who have all keys"""
    return sum(map(validation_func, passports))


def main() -> None:
    # make list b/c is being used twice
    passports = list(parse_passports(utils.get_input(__file__)))

    # part 1
    n_valid_passports_1 = count_valid_passports(is_passport_valid_1, passports)
    print(f"part 1: valid passports  {n_valid_passports_1}")

    # part 2
    n_valid_passports_2 = count_valid_passports(is_passport_valid_2, passports)
    print(f"part 2: valid passports  {n_valid_passports_2}")


if __name__ == "__main__":
    main()
