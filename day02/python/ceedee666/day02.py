from pathlib import Path
import typer


app = typer.Typer()


def read_input_file(input_file_path):
    """ read the input file"""

    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return lines


def convert_input(lines):
    """
    convert the input lines to a list of dicts containing the values.
    """
    return list(map(split_line, lines))


def split_line(line):
    """
    Converts a single input line into its elements.
    Result is a dict containing the keys low, high, letter and passwd.
    """
    parts = line.split()
    numbers = parts[0].split("-")
    
    d = dict()
    d["low"] = int(numbers[0])
    d["high"] = int(numbers[1])
    d["letter"] = parts[1][:-1]
    d["passwd"] = parts[2]

    return d


def check_policies(policies, policy_check):
    """
    The function takes as an input a list of policies as dicts
    containing the keys low, high, letter and passwd and a 
    function to check the policies.
    It checks the password in each dict using the function
    and adds the key valid = True if the check is
    successful and valid = False otherwise.
    """
    return list(map(policy_check, policies))


def check_old_policy(policy):
    """
    Checks the validity of a single policy using the
    rules from part 1 of day 2.
    """
    letter_count = policy["passwd"].count(policy["letter"])
    result = dict(policy)
    result["valid"] = policy["low"] <= letter_count <= policy["high"]

    return result


def check_new_policy(policy):
    """
    Checks the validity of a single policy using the rules from
    part 2 of day 2.
    """
    result = dict(policy)
    letter_pos1 = policy["passwd"][policy["low"]-1]
    letter_pos2 = policy["passwd"][policy["high"]-1]

    result["valid"] = ( letter_pos1 == policy["letter"] \
                        or letter_pos2 == policy["letter"] ) \
                        and not letter_pos1 == letter_pos2

    return result


@app.command()
def part1(input_file: str):
    """
    To solve the part 1 of day 2 this function reads the input
    file and counts how many valid passwars are contained according
    to the old password policy.
    The result is printed to stdout.
    """
    policies = convert_input(read_input_file(input_file))
    policies = check_policies(policies, check_old_policy)
    valid_policies = list(filter(lambda p: p["valid"], policies))

    print(f"The number of valid passwords is {len(valid_policies)}")


@app.command()
def part2(input_file: str):
    """
    To solve the part 2 of day 2 this function reads the input
    file and counts how many valid passwars are contained according
    to the new password policy.
    The result is printed to stdout.
    """
    policies = convert_input(read_input_file(input_file))
    policies = check_policies(policies, check_new_policy)
    valid_policies = list(filter(lambda p: p["valid"], policies))

    print(f"The number of valid passwords is {len(valid_policies)}")


if __name__ == "__main__":
    app()
