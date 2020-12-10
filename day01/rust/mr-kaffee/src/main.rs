use std::fs;
use std::error::Error;
use std::time::Instant;
use mr_kaffee_2020_01::*;

fn read_input() -> Result<Vec<i32>, Box<dyn Error>> {
    let content = fs::read_to_string("input.txt")?;

    let mut list: Vec<i32> = Vec::new();
    for line in content.lines() {
        list.push(line.parse()?);
    }

    Ok(list)
}

fn main() {
    let list = read_input()
        .expect("Could not read from file");

    const R1: i32 = 381_699;

    // solve part 1, check & print
    let now = Instant::now();
    let r1 = solve_n2(&list);
    println!("Solved part 1 with tuple combinations in {} us -> {}", now.elapsed().as_micros(), r1);
    assert_eq!(r1, R1);

    // solve with generic method
    let now = Instant::now();
    let r1 = solve_with_itertools(&list, 2);
    println!("Solved part 1 with itertools::combinations in {} us -> {}", now.elapsed().as_micros(), r1);
    assert_eq!(r1, R1);

    // solve with generic method without iterators
    let now = Instant::now();
    let r1 = solve_with_while(&list, 2);
    println!("Solved part 1 with while loop in {} us -> {}", now.elapsed().as_micros(), r1);
    assert_eq!(r1, R1);

    const R2: i32 = 111_605_670;

    // solve part 2, check & print
    let now = Instant::now();
    let r2 = solve_n3(&list);
    assert_eq!(r2, R2);
    println!("Solved part 2 with tuple combinations in {} us -> {}", now.elapsed().as_micros(), r2);

    // solve with generic method
    let now = Instant::now();
    let r2 = solve_with_itertools(&list, 3);
    println!("Solved part 2 with itertools::combinations in {} us -> {}", now.elapsed().as_micros(), r2);
    assert_eq!(r2, R2);

    // solve with generic method without iterators
    let now = Instant::now();
    let r2 = solve_with_while(&list, 3);
    println!("Solved part 2 with while loop in {} us -> {}", now.elapsed().as_micros(), r2);
    assert_eq!(r2, R2);
}
