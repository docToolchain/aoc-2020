use std::fs;
use regex::Regex;

#[derive(Debug, PartialEq)]
struct Password {
    p1: usize,
    p2: usize,
    sym: char,
    password: String,
}

impl Password {
    fn check(&self) -> (bool, bool) {
        // counter for occurrence of letter
        let mut cnt = 0;

        // flags for matching letter in position
        let mut m1 = false;
        let mut m2 = false;

        // loop over letters
        for (idx, c) in self.password.chars().enumerate() {
            // symbol found
            if c == self.sym {
                // count occurrences
                cnt += 1;

                // check positions, mind the offset for zero based idx and one based p1/p2
                if idx + 1 == self.p1 {
                    m1 = true;
                }
                if idx + 1 == self.p2 {
                    m2 = true;
                }
            }
        };

        (cnt >= self.p1 && cnt <= self.p2, m1 ^ m2)
    }

    fn parse(content: &str) -> Vec<Password> {
        let re = Regex::new(r"(\d+)-(\d+)\s+(\w):\s+(\w+)\s*")
            .expect("Illegal regular expression");

        re.captures_iter(content)
            .map(|cap|
                Password {
                    p1: cap[1].parse().expect("Could not parse p1"),
                    p2: cap[2].parse().expect("Could not parse p2"),
                    sym: cap[3].chars().next().expect("Empty string!"),
                    password: String::from(&cap[4]),
                }).collect()
    }
}

// tag::count_pass[]
fn count_pass(passwords: &[Password]) -> (u32, u32) {
    // check and sum trues for elements on tuples independently
    passwords.iter()
        .map(|password| password.check())
        .fold((0, 0),
              |count, check|
                  (count.0 + check.0 as u32, count.1 + check.1 as u32))
}
// end::count_pass[]

fn main() {
    // read content from file
    let content = fs::read_to_string("input.txt")
        .expect("Could not read file.");
    // parse passwords
    let passwords = Password::parse(&content);

    // count passes
    let (count1, count2) = count_pass(&passwords);

    println!("{} passwords are ok for rule 1", count1);
    assert_eq!(count1, 483);

    println!("{} passwords are ok for rule 2", count2);
    assert_eq!(count2, 482);
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc";

    fn passwords() -> Vec<Password> {
        vec![
            Password { p1: 1, p2: 3, sym: 'a', password: String::from("abcde") },
            Password { p1: 1, p2: 3, sym: 'b', password: String::from("cdefg") },
            Password { p1: 2, p2: 9, sym: 'c', password: String::from("ccccccccc") },
        ]
    }

    #[test]
    fn test_password_parse() {
        assert_eq!(
            Password::parse(CONTENT),
            passwords()
        );
    }

    #[test]
    fn test_password_check() {
        let passwords = passwords();
        assert_eq!(passwords[0].check(), (true, true));
        assert_eq!(passwords[1].check(), (false, false));
        assert_eq!(passwords[2].check(), (true, false));
    }

    #[test]
    fn test_count_pass() {
        assert_eq!((2, 1), count_pass(&passwords()));
    }
}
