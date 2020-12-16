use std::fs;
use mr_kaffee_2020_12::*;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    let steps = Step::parse(&read_input());

    // run solution part 1, without waypoints => use_wp = false
    let mut ship = Ship::new();
    ship.apply_all(&steps, false);
    println!("Ship: {:?} at distance {}", ship, ship.distance());
    assert_eq!(ship.distance(), 1_106);

    // run solution part 2, with waypoints => use_wp = true
    let mut ship = Ship::new();
    ship.apply_all(&steps, true);
    println!("Ship: {:?} at distance {}", ship, ship.distance());
    assert_eq!(ship.distance(), 107_281);
}
