use std::fs;
use mr_kaffee_2020_13::*;
use std::time::Instant;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    let content = read_input();

    // parse
    let (earliest, ids) = parse(&content);

    // solve part 1
    let instant = Instant::now();
    let (id, departure) = find_earliest_departure(earliest, &ids);
    println!("Solution part 1 done in {:?}: {}", instant.elapsed(), id * (departure - earliest));
    assert_eq!(id * (departure - earliest), 246);

    // solve part 2
    let instant = Instant::now();
    let t = find_time(&ids);
    println!("Solution part 2 done in {:?}: {}", instant.elapsed(), t);
    assert_eq!(t, 939_490_236_001_473);

    // solve part 2 variant
    let instant = Instant::now();
    let t = find_time_iteratively(&ids);
    println!("Solution part 2 (variant) done in {:?}: {}", instant.elapsed(), t);
    assert_eq!(t, 939_490_236_001_473);
}