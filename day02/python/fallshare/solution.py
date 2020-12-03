from pathlib import Path
import re


def extractPasswordInformation(line):
    # breaking up the input into the different parts
  
    m = re.match(r"(\d*)-(\d*) (\w): (\w*)", line)
    return m.groups()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        data = list(map(extractPasswordInformation, f.readlines()))

    return data


def passwordCheck_Star1(data):
    lowerLimit = int(data[0])
    upperLimit = int(data[1])
    letter = data[2]
    potentialPassword = data[3]

    return potentialPassword.count(letter) in range(lowerLimit, upperLimit + 1)


def passwordCheck_Star2(data):
    posFirstLetter = int(data[0]) - 1
    posSecondLetter = int(data[1]) - 1
    letter = data[2]
    potentialPassword = data[3]
    # xor for the win
    return bool(potentialPassword[posFirstLetter] == letter) ^ bool(potentialPassword[posSecondLetter] == letter)

def find_valid_passwords_Star1(data):
    return len(list(filter(passwordCheck_Star1, data)))

def find_valid_passwords_Star2(data):
    return len(list(filter(passwordCheck_Star2, data)))


if __name__ == "__main__":
    assert extractPasswordInformation("4-5 t: ftttttrvts") == ("4","5","t","ftttttrvts")
    
    data = read_input_file('input.txt')

    assert passwordCheck_Star1(data[0]) == False

    print(f"Star 1: {find_valid_passwords_Star1(data)} valid passwords found!")
    print(f"Star 2: {find_valid_passwords_Star2(data)} valid passwords found!")