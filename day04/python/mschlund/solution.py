import re

def number_valid(x, num_digits, lower_bound, upper_bound):
    if not re.match('[0-9]{'+str(num_digits)+'}', x):
        return False
    if int(x) < lower_bound or int(x) > upper_bound:
        return False
    return True

def is_valid_star2(fields_with_values):
    print(fields_with_values)
    try:
        if not number_valid(fields_with_values['byr'], 4, 1920, 2002):
            print('byr invalid')
            return False
        if not number_valid(fields_with_values['iyr'], 4, 2010, 2020):
            print('iyr invalid')
            return False
        if not number_valid(fields_with_values['eyr'], 4, 2020, 2030):
            print('eyr invalid')
            return False
        height = fields_with_values['hgt']
        if height[0].isdigit() and height.endswith('cm'):
            value = int(height.split('cm')[0])
            if value < 150 or value > 193:
                print('hgt(cm) invalid')
                return False
        elif height.endswith('in'):
            value = int(height.split('in')[0])
            if value < 59 or value > 76:
                print('hgt(in) invalid')
                return False
        else:
            print('hgt invalid')
            return False
        if not re.match('#[0-9a-f]{6}', fields_with_values['hcl']):
            print('hcl invalid')
            return False
        valid_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        if not fields_with_values['ecl'] in valid_colors:
            print('ecl invalid')
            return False
        if not re.match('[0-9]{9}$', fields_with_values['pid']):
            print('pid invalid')
            return False
    except KeyError as e:
        print('Missing {}'.format(e))
        return False
    print('Valid')
    return True

def is_valid_star2_str(chunk):
    passport = re.split('\\s', chunk)
    all_fields_values = [(x.split(':')[0], x.split(':')[1]) for x in filter(lambda x: x!='', passport)]
    return is_valid_star2(dict(all_fields_values))

def is_valid_star1(fields):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    return all([x in fields for x in required_fields])

def main():
    input_filename = 'input.txt'
    #input_filename = 'input_small.txt'
    with open(input_filename, 'r') as input:
        all_passports = input.read()
        passports = re.split('\n\n', all_passports)
        valid_1 = 0
        valid_2 = 0
        for chunk in passports:
            passport = re.split('\\s', chunk)
            all_fields_values = [(x.split(':')[0], x.split(':')[1]) for x in filter(lambda x: x!='', passport)]

            fields = list(map(lambda x: x[0], all_fields_values))
            if is_valid_star1(fields):
                valid_1 += 1
            if is_valid_star2(dict(all_fields_values)):
                valid_2 += 1

        print('# of valid passports: {} | {}'.format(valid_1, valid_2))

if __name__ == "__main__":
    main()