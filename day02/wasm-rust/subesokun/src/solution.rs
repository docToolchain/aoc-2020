use regex::Regex;

struct Password {
    min: usize,
    max: usize,
    letter: char,
    password: String,
}

fn extract_input_lines(puzzle_input: std::vec::Vec<String>) -> std::vec::Vec<Password> {
    let mut passwords_list : Vec<Password> = Vec::new();
    let re = Regex::new(r"(\d+)-(\d+)\s(\w):\s(\w+)").unwrap();
    for line in puzzle_input.iter() {
        let caps = re.captures(line).unwrap();
        let min: usize = caps.get(1).map_or(0, |m| m.as_str().parse::<usize>().unwrap());
        let max: usize = caps.get(2).map_or(0, |m| m.as_str().parse::<usize>().unwrap());
        let letter: char = caps.get(3).map_or('\0', |m| m.as_str().parse::<char>().unwrap());
        let password: String = caps.get(4).map_or(String::from(""), |m| m.as_str().parse::<String>().unwrap());
        let entry = Password { min, max, letter, password };
        passwords_list.push(entry);
    }
    return passwords_list;
}

//tag::star1[]
fn is_valid_password_old_job(entry: Password) -> u32 {
    let count = entry.password.matches(entry.letter).count();
    if count >= entry.min && count <= entry.max {
        return 1;
    } else {
        return 0;
    }
}

fn count_valid_passwords_old_job_variant(passwords: std::vec::Vec<Password>) -> u32 {
    return passwords.into_iter().map(|entry| is_valid_password_old_job(entry)).sum();
}
//end::star1[]

//tag::star2[]
fn is_valid_password_new_job(entry: Password) -> u32 {
    let ch_one = entry.password.chars().nth(entry.min - 1).unwrap();
    let ch_two = entry.password.chars().nth(entry.max - 1).unwrap();
    if ch_one != ch_two && (ch_one == entry.letter || ch_two == entry.letter) {
        return 1;
    } else {
        return 0;
    }
}

fn count_valid_passwords_new_job_variant(passwords: std::vec::Vec<Password>) -> u32 {
    return passwords.into_iter().map(|entry| is_valid_password_new_job(entry)).sum();
}
//end::star2[]

pub fn run_star1(puzzle_input: std::vec::Vec<String>) -> u32 {
    let passwords = extract_input_lines(puzzle_input);
    let solution: u32 = count_valid_passwords_old_job_variant(passwords);
    return solution;
}

pub fn run_star2(puzzle_input: std::vec::Vec<String>) -> u32 {
    let passwords = extract_input_lines(puzzle_input);
    let solution: u32 = count_valid_passwords_new_job_variant(passwords);
    return solution;
}
