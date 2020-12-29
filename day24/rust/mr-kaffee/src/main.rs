use mr_kaffee_2020_24::*;
use std::time::Instant;
use std::fs;

fn read_input() -> String {
    fs::read_to_string("input.txt").expect("Could not read from file")
}

fn main() {
    // start timer
    let instant_main = Instant::now();

    // read file
    let content = read_input();

    // parse
    let coords = get_coords(&content);

    // solve part 1
    let instant_part = Instant::now();
    let flipped = flip_tiles(&coords);
    let sol = flipped.len();
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 497);

    // solve part 2
    let instant_part = Instant::now();
    let flipped = update(&flipped, 100);
    let sol = flipped.len();
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 4156);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
