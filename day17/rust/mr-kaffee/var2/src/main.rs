
use std::fs;
use mr_kaffee_2020_17_1::*;
use std::time::Instant;

fn read_input() -> String {
    fs::read_to_string("../input.txt")
        .expect("Could not read from file.")
}

fn main() {
    // start timer
    let instant_main = Instant::now();

    // read file
    let content = read_input();

    // solve part 1
    let instant_part = Instant::now();
    let (map, bbox) = parse::<(isize, isize, isize)>(&content, &[0]);
    let (map, _) = update_steps(&map, &bbox, 6);
    let sol = map.len();
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 448);

    // solve part 2
    let instant_part = Instant::now();
    let (map, bbox) = parse::<(isize, isize, isize, isize)>(&content, &[0, 0]);
    let (map, _) = update_steps(&map, &bbox, 6);
    let sol = map.len();
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 2_400);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}