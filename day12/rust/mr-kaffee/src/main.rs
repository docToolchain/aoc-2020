use std::fs;
use mr_kaffee_2020_12::*;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    let list = Instr::parse(&read_input());

    let mut ship = Ship::new();
    ship.apply_all(&list, false);
    println!("Ship: {:?} at distance {}", ship, ship.distance());
    assert_eq!(ship.distance(), 1_106);

    let mut ship = Ship::new();
    ship.apply_all(&list, true);
    println!("Ship: {:?} at distance {}", ship, ship.distance());
    assert_eq!(ship.distance(), 107_281);
}
