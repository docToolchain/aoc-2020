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
    println!("Grid width: {}, height: {}", grid.width, grid.height);

    let instant = Instant::now();
    let cnt = grid.run(1, 4);
    println!("Solved in {} ms: {} are occupied for depth: 1, threshold: 4",
             instant.elapsed().as_millis(), cnt);
    assert_eq!(cnt, 2489);

    let instant = Instant::now();
    let cnt = grid.run(grid.data.len(), 5);
    println!("Solved in {} ms: {} are occupied for depth: Inf, threshold: 5",
             instant.elapsed().as_millis(), cnt);
    assert_eq!(cnt, 2180);
}
