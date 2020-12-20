import utils

utils.getVersion()

input = utils.read_file_to_list("input.txt")

# print(input)

size = len(input)
utils.log.debug("len: {}".format(size))
utils.log.debug(input)

unique_group_content = utils.get_unique_group_answers(input)
utils.log.debug(unique_group_content)

number_of_yes_questions = 0
for i in unique_group_content:
    number_of_yes_questions += len(i)

utils.log.info("solution part 1 ==> number_of_yes_questions: {}".format(number_of_yes_questions)) # ==> 6387


intersection_group_answers = utils.get_intersection_group_answers(input)
utils.log.debug(intersection_group_answers)
number_of_common_yes_questions = 0
for i in intersection_group_answers:
    number_of_common_yes_questions += len(i)

utils.log.info("solution part 2 ==> number_of_common_yes_questions: {}".format(number_of_common_yes_questions)) # ==> 3039


