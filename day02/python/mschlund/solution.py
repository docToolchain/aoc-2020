
def parse_parts(line):
    space_separated_parts = line.split()
    bounds = space_separated_parts[0].split('-')
    char = space_separated_parts[1].split(':')[0]
    password = space_separated_parts[2]
    return int(bounds[0]), int(bounds[1]), char, password

def is_valid_first(min_req, max_req, letter, password):
    letter_count = password.count(letter)
    return letter_count >= min_req and letter_count <= max_req

# exactly one of the positions must equal the letter
#  => logical 'xor' of the two comparisions, 'xor' is equivalent to '!='
def is_valid_second(pos1, pos2, letter, password):
    return (password[pos1-1] == letter) != (password[pos2-1] == letter)


def main():
    input_filename = 'input.txt'
    star_number = 2
    num_valid_pws = 0
    with open(input_filename, 'r') as input:
        for line in input:
            num1, num2, letter, password = parse_parts(line)
            if star_number == 1:
                if is_valid_first(num1, num2, letter, password):
                    num_valid_pws += 1
            elif star_number == 2:
                if is_valid_second(num1, num2, letter, password):
                    num_valid_pws += 1
        print('Number of valid passwords: {}'.format(num_valid_pws))

if __name__ == "__main__":
    main()