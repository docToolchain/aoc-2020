import utils

utils.getVersion()

input = utils.read_file_to_list("input.txt")

# print(input)

size = len(input)
utils.log.debug("len: {}".format(size))

passports = {}
counter = 1
data = ""
for i in input:
    if '\n' != i:
        #passports.update({counter: i})
        data += "{} ".format(i.strip())
    else:
        passports[counter] = data.strip()
        data = ""
        counter += 1

#check for remaining data in case of end of file is reached.
if "" != data:
    passports[counter] = data.strip()
    counter += 1

utils.log.debug(passports)

valid_passports = 0
for i in range(1,counter):
    if utils.check_passport_content(passports[i]):
        valid_passports += 1

utils.log.info("\nsolution part 1 ==> valid passports: {}".format(valid_passports)) # ==> 250


valid_passports = 0
for i in range(1,counter):
    if utils.check_passport_extended(passports[i]):
        valid_passports += 1

utils.log.info("\nsolution part 2 ==> valid passports: {}".format(valid_passports))  # ==> 158
