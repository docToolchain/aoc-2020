use mr_kaffee_2020_19::*;
use std::time::Instant;
use std::fs;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    // start timer
    let instant_main = Instant::now();

    // read file
    let content = read_input();

    // parse
    let (mut rules, texts) = parse(&content);

    // solve part 1
    let instant_part = Instant::now();
    let sol = matches(&rules, texts);
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 226);

    // solve part 2
    let instant_part = Instant::now();
    rules.insert(8, Rule::Alternative(vec![42], vec![42, 8]));
    rules.insert(11, Rule::Alternative(vec![42, 31], vec![42, 11, 31]));
    let sol = matches(&rules, texts);
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 355);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
