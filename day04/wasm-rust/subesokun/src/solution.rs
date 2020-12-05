use regex::Regex;

//tag::star1[]
fn extract_passports(puzzle_input: std::vec::Vec<String>) -> std::vec::Vec<String> {
    let mut vec = Vec::new();
    let mut tmp = String::new();
    // For some reason I couldn't find a simple replace function "\n\n\" -> "\n" in Rust...
    for line_value in puzzle_input.into_iter() {
        if line_value == "" {
            vec.push(tmp);
            tmp = String::new();
        } else {
            tmp = tmp + " " + &line_value.to_string() + " " // Always add trailing whitespace as delimiter
        }
    }
    vec.push(tmp);
    return vec
}

fn count_valid_passports(passports: std::vec::Vec<String>) -> u32 {
    let mut valid_cnt = 0;
    let re = Regex::new(r"(byr:|iyr:|eyr:|hgt:|hcl:|ecl:|pid:)").unwrap();
    for passport in passports {
        // println!("-------\n {}", passport);
        let passport_str = passport.to_string();
        let matches: Vec<regex::Match> = re.find_iter(&passport_str).collect();
        if matches.len() == 7 {
            valid_cnt += 1;
        }
    }
    return valid_cnt;
}

pub fn run_star1(puzzle_input: std::vec::Vec<String>) -> u32 {
    let passports = extract_passports(puzzle_input);
    let solution = count_valid_passports(passports);
    return solution;
}
//end::star1[]

//tag::star2[]
fn count_valid_passports_strict(passports: std::vec::Vec<String>) -> u32 {
    let mut valid_cnt = 0;
    let re = Regex::new(r"((byr:(19[2-8][0-9]|199[0-9]|200[0-2]))\s|iyr:((201[0-9]|2020))\s|eyr:(202[0-9]|2030)\s|hgt:((1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in)\s|hcl:(#[0-9a-z]{6})\s|ecl:(amb|blu|brn|gry|grn|hzl|oth)\s|pid:(\d{9})\s)").unwrap();
    for passport in passports {
        let passport_str = passport.to_string();
        let matches: Vec<regex::Match> = re.find_iter(&passport_str).collect();
        if matches.len() == 7 {
            valid_cnt += 1;
        }
    }
    return valid_cnt;
}

pub fn run_star2(puzzle_input: std::vec::Vec<String>) -> u32 {
    let passports = extract_passports(puzzle_input);
    let solution = count_valid_passports_strict(passports);
    return solution;
}
//end::star2[]
