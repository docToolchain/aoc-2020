use std::fs;
use mr_kaffee_2020_14::*;
use std::time::Instant;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    let content = read_input();

    // parse
    let instructions = Instruction::parse(&content);

    // solve part 1
    let instant = Instant::now();
    let sum = run_v1(&instructions).values().sum::<u64>();
    println!("Solution part 1 done in {:?}: {}", instant.elapsed(), sum);
    assert_eq!(sum, 6_513_443_633_260);

    // solve part 2
    let instant = Instant::now();
    let sum = run_v2(&instructions).values().sum::<u64>();
    println!("Solution part 2 done in {:?}: {}", instant.elapsed(), sum);
    assert_eq!(sum, 3_442_819_875_191);
}