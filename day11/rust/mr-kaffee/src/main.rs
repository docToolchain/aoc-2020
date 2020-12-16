use std::fs;
use mr_kaffee_2020_11::*;
use std::time::Instant;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    let content = read_input();
    let grid = Grid::parse(&content);

    let instant = Instant::now();
    // tag::part1[]
    let cnt = grid.stationary(1, 4)
        .as_ref().unwrap_or(&grid)
        .count_occupied();
    // end::part1[]
    println!("Solved in {} ms: {} are occupied for depth: 1, threshold: 4",
             instant.elapsed().as_millis(), cnt);
    assert_eq!(cnt, 2_489);

    let instant = Instant::now();
    let depth = grid.data.len();
    let cnt = grid.stationary(depth, 5)
        .as_ref().unwrap_or(&grid)
        .count_occupied();
    println!("Solved in {} ms: {} are occupied for depth: Inf, threshold: 5",
             instant.elapsed().as_millis(), cnt);
    assert_eq!(cnt, 2_180);
}
