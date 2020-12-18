use std::fs;
use mr_kaffee_2020_18::*;
use std::time::Instant;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    // start timer
    let instant_main = Instant::now();

    // read file
    let content = read_input();
    let token_lines = Token::parse(&content);

    // solve part 1
    let instant_part = Instant::now();
    let sol = token_lines.iter()
        .map(|items| evaluate1(items)).sum::<isize>();
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 8_929_569_623_593);

    // solve part 2
    let instant_part = Instant::now();
    let sol = token_lines.iter()
        .map(|items| evaluate2(items)).sum::<isize>();
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 231_235_959_382_961);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
