import re

def get_answers_of_group(group):
    answers = {x for x in group if re.match('[a-z]', x)}
    return answers

def get_unanimously_answered_questions(group):
    persons = group.split('\n')
    questions_answered = [{q for q in person} for person in persons]
    return set.intersection(*questions_answered)

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    all_custom_forms = input.read()
    groups_answers = re.split('\n\n', all_custom_forms)
    nr_answered = [len(get_answers_of_group(g)) for g in groups_answers]
    print('Sum of # of questions answered: {}'.format(sum(nr_answered)))
    unanimously_answered = [len(get_unanimously_answered_questions(g)) for g in groups_answers]
    print('Sum of questions answered unanimously: {}'.format(sum(unanimously_answered)))

if __name__ == "__main__":
  main()