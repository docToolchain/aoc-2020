def process_input(file_contents):

    return [int(line.strip()) for line in file_contents]

def find_loopsize(key, seed, div_number):
    i = 0
    value = 1
    while value != key:
        value *= seed
        value = value % div_number
        i += 1

    return i

def transform_publickey(key, loop, div_number):
    value = 1
    for i in range(loop):
        value *= key
        value = value % div_number
    return value

def main():
    with open("keys.txt",'r') as code_file:
        all_code_file = code_file.readlines()

    keys = process_input(all_code_file)

    div_number = 20201227
    seed = 7
    loop_size = [find_loopsize(key, seed, div_number) for key in keys]
    print("The encryption key is",transform_publickey(keys[0],loop_size[1],div_number))

main()