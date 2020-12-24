import typer


app = typer.Typer()


INPUT = list(map(int, "974618352"))


def init_cups_list(cups, pad):
    rest = [i for i in range(len(cups)+1, pad+1)]
    cups = list(cups) + rest

    cups_list = {}
    for i in range(len(cups)):
        if i == len(cups)-1:
            cups_list[cups[i]] = cups[0]
        else:
            cups_list[cups[i]] = cups[i+1]
    return cups_list


def play_crab_cups_round(head, cups_list):

    cup1 = cups_list[head]
    cup2 = cups_list[cup1]
    cup3 = cups_list[cup2]

    dest = head-1 if head > 1 else len(cups_list)
    while dest in [cup1, cup2, cup3]:
        dest = dest-1 if dest > 1 else len(cups_list)

    cups_list[head] = cups_list[cup3]
    cups_list[cup3] = cups_list[dest]
    cups_list[dest] = cup1

    head = cups_list[head]
    return head, cups_list


def play_crab_cups(cups, pad, rounds):
    """
    Use dict as a linked list. The index is the label of the cups,
    the value is the next cup.
    """
    cups_list = init_cups_list(cups, pad)
    head = cups[0]

    for _ in range(rounds):
        head, cups_list = play_crab_cups_round(head, cups_list)

    return cups_list


@app.command()
def part1():
    cups_list = play_crab_cups(INPUT, len(INPUT), 100)

    start = 1
    result = ""
    for _ in range(len(cups_list)-1):
        result += str(cups_list[start])
        start = cups_list[start]

    print(f"The labels after cup 1 are: {result}")


@app.command()
def part2():
    cups_list = play_crab_cups(INPUT, 1_000_000, 10_000_000)

    print(f"The result for part 2 is: {cups_list[1] * cups_list[cups_list[1]]}")


if __name__ == "__main__":
    app()
