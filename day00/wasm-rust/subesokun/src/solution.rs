use web_sys::console;

fn read_puzzle_input(content: String) -> std::vec::Vec<f64> {
    let mut vec = Vec::new();
    for line in content.lines() {
        let number: f64 = line.parse().unwrap();
        vec.push(number);
    }
    return vec
}

fn calculate_fuel(mass: f64) -> f64 {
    return (mass / 3.0).floor() - 2.0;
}

fn calculate_fuel_recursive(mass: f64) -> f64 {
    let fuel: f64 = calculate_fuel(mass);
    if fuel < 0.0 {
        return 0.0
    } else {
        return fuel + calculate_fuel_recursive(fuel)
    };
}

pub fn run(input_txt_string: String) {
    println!("Hello, world!");
    let puzzle_input = read_puzzle_input(input_txt_string);

    let solution_part_1: f64 = puzzle_input.iter().map(|&mass| calculate_fuel(mass)).sum();
    console::log_2(&"Solution to part 1: {}".into(), &solution_part_1.to_string().into());

    let solution_part_2: f64 = puzzle_input.iter().map(|&mass| calculate_fuel_recursive(mass)).sum();
    console::log_2(&"Solution to part 2: {}".into(), &solution_part_2.to_string().into());
}