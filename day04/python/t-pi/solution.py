import math

def read_daily_input(filename):
    ''' Read lines from file with given input name
        cast to daily required type and return list '''
    with open(filename) as input_file:
        local_list = input_file.readlines()
        return_list = [item.strip() for item in local_list]
        return return_list

def check_passport_field_valid(field_type, field_content):
    ''' Check field for validity according to given rules:
    - byr (Birth Year) - four digits; at least 1920 and at most 2002.
    - iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    - eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    - hgt (Height) - a number followed by either cm or in:
    - If cm, the number must be at least 150 and at most 193.
    - If in, the number must be at least 59 and at most 76.
    - hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    - ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    - pid (Passport ID) - a nine-digit number, including leading zeroes.
    - cid (Country ID) - ignored, missing or not.
    '''
    field_valid = False
    if (field_type == 'byr'):
        if (field_content.isnumeric()): 
            field_valid = (int(field_content)>=1920) and (int(field_content)<=2002)
    if (field_type == 'iyr'):
        if (field_content.isnumeric()): 
            field_valid = (int(field_content)>=2010) and (int(field_content)<=2020)
    if (field_type == 'eyr'):
        if (field_content.isnumeric()): 
            field_valid = (int(field_content)>=2020) and (int(field_content)<=2030)
    if (field_type == 'hgt'):
        if (field_content[:-2].isnumeric()):
            if (field_content[-2:] == 'cm'):
                field_valid = (int(field_content[:-2])>=150) and (int(field_content[:-2])<=193)
            if (field_content[-2:] == 'in'):
                field_valid = (int(field_content[:-2])>=59) and (int(field_content[:-2])<=76)
    if (field_type == 'hcl'):
        if ((field_content[0] == '#') and (len(field_content) == 7)):
            try:
                # fastest for small strings, according to
                # https://stackoverflow.com/a/34261051
                field_valid = (int(field_content[1:], 16) >= 0)
            except ValueError:
                pass
    if (field_type == 'ecl'):
        eye_colors = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
        field_valid = (field_content in eye_colors)
    if (field_type == 'pid'):
        if (field_content.isnumeric()): 
            field_valid = (len(field_content) == 9)
    return field_valid

def count_valid_passports_in_list(passport_list):
    ''' Count valid password by checking internally defined required fields
        against given rules (s. check_passport_field_valid())
    '''
    required_fields = {
        'byr': 'Birth Year',
        'iyr': 'Issue Year',
        'eyr': 'Expiration Year',
        'hgt': 'Height',
        'hcl': 'Hair Color',
        'ecl': 'Eye Color',
        'pid': 'Passport ID'
    }
    found_field_names = list()
    valid_count = 0
    for line_nr, line in enumerate(passport_list):
        if (len(line) < 3):
            found_field_names = list()
            continue
        pairs = line.split(' ')
        for pair in pairs:
            split_pair = pair.split(':')
            if (split_pair[0] in required_fields.keys()) and \
                (split_pair[0] not in found_field_names) and \
                (check_passport_field_valid(split_pair[0], split_pair[1])):
                found_field_names.append(split_pair[0])
        #important: check validity independently of newline, else missing the last...
        if (len(found_field_names) == len(required_fields.keys())):
            valid_count += 1
            found_field_names = list()
    return valid_count

def count_total_passports_in_list(passport_list):
    ''' Count total number of passports, just for completeness
    '''
    total_count = 0
    for line in passport_list:
        if (len(line) < 3):
            total_count += 1
    if (len(passport_list[-1]) > 3):
        total_count += 1
    return total_count

def main():
    daily_list = read_daily_input('input04.txt')
    print(f"Valid passports: {count_valid_passports_in_list(daily_list)} of {count_total_passports_in_list(daily_list)} total")

if __name__ == "__main__":
    main()


