use std::fs;
use mr_kaffee_2020_16::*;
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

    // solve part 1
    let instant_part = Instant::now();
    let (rules, my_pass, nearby_passes, invalids) =
        parse(&content);
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), invalids);
    assert_eq!(invalids, 21_996);


    // solve part 2
    let instant_part = Instant::now();
    let checks = find_fields(&rules, &nearby_passes, "departure");
    let sol = checks.iter().map(|(_, pos)| my_pass[*pos] as i64).product::<i64>();
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 650_080_463_519);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}