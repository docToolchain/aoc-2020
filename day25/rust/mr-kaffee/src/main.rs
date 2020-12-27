use mr_kaffee_2020_25::*;
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
    let (key1, key2) = get_public_keys(&content);

    // solve part 1
    let instant_part = Instant::now();
    let sol = get_encryption_key(key1, key2);
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 6_421_487);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
