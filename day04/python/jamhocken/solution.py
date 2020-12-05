import re

def check_field(dictionary, field_name):
    eyecolors = ['amb','blu','brn','gry','grn','hzl','oth']
    hcl_regex = re.compile('#(\d|[a-f]){6}')
    hgt_regex = re.compile('\d{2,3}((cm)|(in))')

    if field_name == 'byr':
        year = int(dictionary.get('byr'))
        if year >= 1920 and year <= 2002: return True
        else: return False
        
    if field_name == 'iyr':
        year = int(dictionary.get('iyr'))
        if year >= 2010 and year <= 2020: return True
        else: return False
        
    if field_name == 'eyr':
        year = int(dictionary.get('eyr'))
        if year >= 2020 and year <=2030: return True
        else: return False
        
    if field_name == 'pid':
        if dictionary.get('pid').isdigit() and len(dictionary.get('pid'))==9:
            return True
        else: return False
    
    if field_name == 'ecl':
        if dictionary.get('ecl') in eyecolors: return True
        else: return False
    
    if field_name == 'hcl':
        if re.fullmatch(hcl_regex, dictionary.get('hcl')) != None: return True
        else: return False
    
    if field_name == 'hgt':
        if re.fullmatch(hgt_regex, dictionary.get('hgt')) != None:
            if dictionary.get('hgt').endswith('cm'):
                if int((dictionary.get('hgt')).rstrip('cm')) >= 150 and \
                    int((dictionary.get('hgt')).rstrip('cm')) <= 193:
                    return True
                else: return False
            elif int((dictionary.get('hgt')).rstrip('in')) >= 59 and \
                int((dictionary.get('hgt')).rstrip('in')) <= 76: return True
            else: return False

with open("passports.txt",'r') as passport_file: 
    file_contents = passport_file.readlines()

passport_dictionary = []
temp_dictionary = {}
    
for lines in file_contents:
    if lines == '\n':
        passport_dictionary.append(temp_dictionary)
        temp_dictionary = {}
    else:
        stripped_line = lines.rstrip()
        split_line = stripped_line.split()
        for items in split_line:
            keyword_pair = items.split(':')
            temp_dictionary[keyword_pair[0]] = keyword_pair[1]
            
passport_dictionary.append(temp_dictionary)

count_fieldspresent = 0
count_validvalues = 0
keys = ['byr','iyr','eyr','hgt','hcl','ecl','pid']

for entries in passport_dictionary:
    flag_present = True
    for necessary_key in keys:
        if not (necessary_key in entries): flag_present = False
    if flag_present:
        count_fieldspresent += 1
        for necessary_key in keys:
            if not (check_field(entries,necessary_key)): 
                flag_present = False
        if flag_present:
            count_validvalues += 1

print(count_fieldspresent, 'entries have all of the required fields.')
print(count_validvalues, 'entries have all required fields and data is valid.')