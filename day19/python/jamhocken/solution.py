import itertools

def process_input(file_contents):
    lines_stripped = [line.strip() for line in file_contents]
    i = 0
    rules = dict()
    letter_positions = set()
    while lines_stripped[i] != '':
        fragments1 = lines_stripped[i].split(": ")
        if fragments1[1] == '"a"' or fragments1[1] == '"b"':
            rules.update({int(fragments1[0]): fragments1[1].strip('"')})
            letter_positions.add(int(fragments1[0]))
        else:
            fragments2 = fragments1[1].split(" | ")
            fragments3 = [[int(j) for j in i.split()] for i in fragments2]
            rules.update({int(fragments1[0]) : fragments3})
        i += 1
    patterns = lines_stripped[i+1:]

    return rules, patterns, letter_positions

def create_validpatterns(rules, letter_positions):
    last_rule = 0
    rules_calculated = letter_positions.copy()
    valid_patterns = {position: rules[position] for position in rules_calculated}
    next_rules = set([key for key, values in rules.items() if set(itertools.chain(*values)).issubset(letter_positions)])

    while not (last_rule in valid_patterns.keys()):
        for rule in next_rules:
            temp_set = set()
            for block in rules[rule]:
                temp_pattern = valid_patterns[block[0]]
                count = 1
                while count < len(block):
                    temp_pattern = set([pattern + variant for variant in valid_patterns[block[count]]
                                        for pattern in temp_pattern])
                    count += 1
                temp_set = temp_set.union(temp_pattern)
            valid_patterns.update({rule: temp_set})
        rules_calculated = rules_calculated.union(next_rules)
        next_rules = set([key for key, values in rules.items()
                          if set(itertools.chain(*values)).issubset(rules_calculated)])

    return valid_patterns

def problem2(patterns, valid_patterns, subpattern1, subpattern2):
    count = 0
    last_rule = 0
    for pattern in patterns:
        if pattern in valid_patterns[last_rule]:
            count += 1
        else:
            flag = 0
            while pattern[len(pattern)-len(list(subpattern1)[0]):len(pattern)] in subpattern1:
                pattern = pattern[:len(pattern)-len(list(subpattern1)[0])]
                flag += 1
            if flag > 0:
                flag1 = 0
                while pattern[len(pattern) - len(list(subpattern2)[0]):len(pattern)] in subpattern2:
                    pattern = pattern[:len(pattern) - len(list(subpattern2)[0])]
                    flag1 += 1
                if flag1 > flag and len(pattern) == 0:
                    count += 1
    return count

def main():
    with open("input.txt",'r') as code_file:
        all_code_file = code_file.readlines()

    rules, patterns, letter_positions = process_input(all_code_file)

    valid_patterns = create_validpatterns(rules, letter_positions)

    count = sum([1 for pattern in patterns if pattern in valid_patterns[0]])

    print(count, "messages completely match rule 0.")

    count1 = problem2(patterns, valid_patterns, valid_patterns[31], valid_patterns[42])

    print(count1, "messages completely match rule 0 with updated rules 8 and 11.")

main()