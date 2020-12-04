
import re

def read_file_to_list(filename):
    """Read file to List"""
    list = []
    dataset = {}
    nr = 0
    file = open(filename, "r")
    for line in file:
        if line.strip() == '':
            nr = nr + 1
            list.append(dataset)
            dataset = {}
        else:
            sline = line.strip().split(' ')
            for item in sline:
                key,val = item.split(':')
                dataset.update({ key : val })
    if dataset:
        list.append(dataset)
    file.close()
    return list



#    byr (Birth Year)
#    iyr (Issue Year)
#    eyr (Expiration Year)
#    hgt (Height)
#    hcl (Hair Color)
#    ecl (Eye Color)
#    pid (Passport ID)
#    cid (Country ID)



def check_password(password):
    
    for f in ('byr','iyr','eyr','hgt','hcl','ecl','pid'):
        if f not in password:
            return False
    if 'cid' in password:
        return True

    #temporary
    return True



def check_password2(password):
    
    for f in ('byr','iyr','eyr','hgt','hcl','ecl','pid'):
        if f not in password:
            return False
    #byr (Birth Year) - four digits; at least 1920 and at most 2002.
    byr = int(password['byr'])
    if( byr < 1920 or byr > 2002):
        return False
    #iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    iyr = int(password['iyr'])
    if( iyr < 2010 or iyr > 2020):
        return False
    #eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    eyr = int(password['eyr'])
    if( eyr < 2020 or eyr > 2030):
        return False
    #hgt (Height) - a number followed by either cm or in:
     #If cm, the number must be at least 150 and at most 193.
    #If in, the number must be at least 59 and at most 76.
    m = re.search("^([0-9]+)([cmin]+)$", password['hgt'])
    if not m:
        return False
    hgt = int(m.group(1))
    if(m.group(2) == 'cm'):
        if(hgt < 150 or hgt > 193):
            return False
    else:
        if(hgt < 59 or hgt > 76):
            return False
    #hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl = password['hcl']
    if not re.search("^#[0-9a-f]{6,6}$", hcl):
        return False
    #ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    ecl = password['ecl']
    if ecl not in ('amb' , 'blu' , 'brn' , 'gry' ,  'grn' , 'hzl' , 'oth'):
        return False
    #pid (Passport ID) - a nine-digit number, including leading zeroes.
    pid = password['pid']
    if not re.search("^[0-9]{9,9}$", pid):
        return False
    #cid (Country ID) - ignored, missing or not.


    #temporary
    return True
