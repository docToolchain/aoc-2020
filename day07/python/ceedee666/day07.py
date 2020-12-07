from pathlib import Path
from collections import defaultdict
import typer


app = typer.Typer()


def read_input_file(input_file_path):
    p = Path(input_file_path)

    with p.open() as f:
        lines = f.readlines()

    return lines


def parse_line(line):
    content = dict()

    bag_clr, content_str = line.split(" bags contain ")
    
    if "no other" not in content_str:
        for c in content_str.strip(" .").split(", "):
            parts = c.split()
            content[" ".join(parts[1:3])] = int(parts[0])

    return bag_clr, content


def parse_input(lines):
    converted_lines = [parse_line(l) for l in lines]
    content_map = {k: v for (k, v) in converted_lines} 

    reverse_content_map = defaultdict(list)

    for c in content_map:
        for k in content_map[c]: 
            reverse_content_map[k].append(c)

    return content_map, reverse_content_map


def all_bags_containing(color, reverse_content_map):
    all_bags = []

    bags = reverse_content_map[color]
    all_bags += bags

    for b in bags:
        all_bags += all_bags_containing(b, reverse_content_map)

    return all_bags


def sum_contained_bags(color, content_map):
    contained = [sum_contained_bags(c, content_map) * content_map[color][c] for c in content_map[color]]
    return sum(contained) + sum(content_map[color].values())


@app.command()
def part1(input_file: str):
    _, reverse_content_map = parse_input(read_input_file(input_file))
    bag_colors = set(all_bags_containing("shiny gold", reverse_content_map))

    print(f"{len(bag_colors)} bags can contain at least on shiny gold bag.")


@app.command()
def part2(input_file: str):
    content_map, _ = parse_input(read_input_file(input_file))
    s = sum_contained_bags("shiny gold", content_map)

    print(f"The shiny gold bag contains {s} other bags.")


if __name__ == "__main__":
    app()
