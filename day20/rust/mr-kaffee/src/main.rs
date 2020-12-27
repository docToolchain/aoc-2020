use mr_kaffee_2020_20::*;
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
    let tiles = Tile::parse(&content);

    // solve part 1
    let instant_part = Instant::now();
    let (width, solution) = solve(&tiles);
    let sol = corners_checksum(width, &solution);
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 20_033_377_297_069);

    let instant_part = Instant::now();
    let (width_v2, solution_v2) = solve_variant(&tiles);
    let sol_v2 = corners_checksum(width_v2, &solution_v2);
    println!("Solution part 1 (variant) done in {:?}: {}", instant_part.elapsed(), sol_v2);
    assert_eq!(sol_v2, sol);

    // solve part 2
    let instant_part = Instant::now();
    let picture = get_picture(width, &solution);
    let (monsters, _t) = find_monsters(&picture, MONSTER, MONSTER_WIDTH);
    let sol = get_roughness(&picture, monsters.len());
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 2_084);

    // substitute_monsters(&picture, _t, &monsters, MONSTER, MONSTER_WIDTH).print(_t);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
