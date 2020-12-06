use std::fs::read_to_string;
use std::path::Path;

mod solution;

fn read_puzzle_input(path: &Path) -> String {
    return read_to_string(path).unwrap();
}

fn main() {
    let input_path = Path::new("input.txt");
    let puzzle_input = read_puzzle_input(&input_path);

    let solution_part_1 = solution::run_star1(puzzle_input.clone());
    println!("Solution to part 1: {}", solution_part_1);

    let solution_part_2 = solution::run_star2(puzzle_input.clone());
    println!("Solution to part 2: {}", solution_part_2);
}