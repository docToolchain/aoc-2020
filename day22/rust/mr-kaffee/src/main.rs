use mr_kaffee_2020_22::*;
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
    let decks = parse(&content);

    // solve part 1
    let instant_part = Instant::now();
    let (_, sol) = play(decks.clone());
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 30_197);

    // solve part 2
    let instant_part = Instant::now();
    let (_, sol) = play_recursive(decks.clone());
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 34_031);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
