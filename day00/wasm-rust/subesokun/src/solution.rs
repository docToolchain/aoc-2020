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

pub fn run_star1(input_txt_string: String) -> f64 {
    let puzzle_input = read_puzzle_input(input_txt_string);
    let solution: f64 = puzzle_input.iter().map(|&mass| calculate_fuel(mass)).sum();
    return solution;
}

pub fn run_star2(input_txt_string: String) -> f64 {
    let puzzle_input = read_puzzle_input(input_txt_string);
    let solution: f64 = puzzle_input.iter().map(|&mass| calculate_fuel_recursive(mass)).sum();
    return solution;
}
