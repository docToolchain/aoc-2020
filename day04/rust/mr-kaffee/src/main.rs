use regex::Regex;
use std::collections::HashMap;
use std::error::Error;
use std::fs;

fn main() {
    let content = fs::read_to_string("input.txt")
        .expect("Could not read file.");

    let passports = Passport::parse(&content)
        .expect("Could not parse passports.");

    let count1 = count_with_required_fields(&passports);
    println!("Found {} passports with required fields.", count1);
    assert_eq!(count1, 235);

    let count2 = count_valid(&passports);
    println!("Found {} valid passports.", count2);
    assert_eq!(count2, 194);
}

fn count_with_required_fields(passports: &Vec<Passport>) -> usize {
    // filter for passports with required fields and count
    passports.iter()
        .filter(|passport| passport.has_required_fields())
        .count()
}

fn count_valid(passports: &Vec<Passport>) -> usize {
    // checker instance instantiates regular expressions once
    let checker = Checker::new();

    // filter for valid passports and count
    passports.iter()
        .filter(|passport| checker.is_valid(&passport))
        .count()
}

#[derive(Debug, PartialEq, Default)]
struct Passport {
    byr: Option<String>,
    iyr: Option<String>,
    eyr: Option<String>,
    hgt: Option<String>,
    hcl: Option<String>,
    ecl: Option<String>,
    pid: Option<String>,
    cid: Option<String>,
}

impl Passport {
    fn from_map(map: &HashMap<String, String>) -> Result<Passport, String> {
        let mut passport = Passport::default();

        for entry in map.iter() {
            match &(entry.0)[..] {
                "byr" => passport.byr = Some(String::from(entry.1)),
                "iyr" => passport.iyr = Some(String::from(entry.1)),
                "eyr" => passport.eyr = Some(String::from(entry.1)),
                "hgt" => passport.hgt = Some(String::from(entry.1)),
                "hcl" => passport.hcl = Some(String::from(entry.1)),
                "ecl" => passport.ecl = Some(String::from(entry.1)),
                "pid" => passport.pid = Some(String::from(entry.1)),
                "cid" => passport.cid = Some(String::from(entry.1)),
                other => return Err(format!("Unknown key: {}", other)),
            };
        };

        Ok(passport)
    }

    fn parse(content: &str) -> Result<Vec<Passport>, Box<dyn Error>> {
        let mut passports = Vec::new();

        let re = Regex::new(r"(\w+):([^\s]+)\s*")?;

        let mut map = HashMap::new();
        for line in content.lines() {
            if line.len() == 0 {
                if map.len() > 0 {
                    passports.push(Passport::from_map(&map)?);
                    map.clear();
                }
            } else {
                re.captures_iter(line).fold((), |_, v| {
                    map.insert(String::from(&v[1]), String::from(&v[2]));
                });
            }
        }
        if map.len() > 0 {
            passports.push(Passport::from_map(&map)?);
            map.clear();
        }

        Ok(passports)
    }

    fn has_required_fields(&self) -> bool {
        self.byr.is_some() &&
            self.iyr.is_some() &&
            self.eyr.is_some() &&
            self.hgt.is_some() &&
            self.hcl.is_some() &&
            self.ecl.is_some() &&
            self.pid.is_some()
    }
}

struct Checker {
    re_hcl: Regex,
    re_ecl: Regex,
    re_pid: Regex,
}

impl Checker {
    fn new() -> Checker {
        Checker {
            re_hcl: Regex::new(r"^#[0-9a-f]{6}$")
                .expect("Invalid regular expression"),
            re_ecl: Regex::new(r"^(amb|blu|brn|gry|grn|hzl|oth)$")
                .expect("Invalid regular expression"),
            re_pid: Regex::new(r"^\d{9}$")
                .expect("Invalid regular expression"),
        }
    }

    fn chk_range(&self, text: &str, min: u32, max: u32) -> bool {
        match text.parse::<u32>() {
            Err(_) => false,
            Ok(val) => val >= min && val <= max,
        }
    }

    pub fn is_valid(&self, val: &Passport) -> bool {
        if !val.has_required_fields() { return false; };

        // check byr by range
        if !self.chk_range(val.byr.as_ref().unwrap(), 1920, 2020) { return false; };

        // check iyr by range
        if !self.chk_range(val.iyr.as_ref().unwrap(), 2010, 2020) { return false; };

        // check eyr by range
        if !self.chk_range(val.eyr.as_ref().unwrap(), 2020, 2030) { return false; };

        // check hgt by range depending on suffix
        let hgt = val.hgt.as_ref().unwrap();
        let (min, max) =
            if hgt.ends_with("cm") {
                // limits for height in cm
                (150, 193)
            } else if hgt.ends_with("in") {
                // limits for height in in
                (59, 76)
            } else { return false; };
        if !self.chk_range(&hgt[..hgt.len() - 2], min, max) { return false; };

        // check hcl with regular expression
        if !self.re_hcl.is_match(&val.hcl.as_ref().unwrap()) { return false; };

        // check ecl with regular expression
        if !self.re_ecl.is_match(&val.ecl.as_ref().unwrap()) { return false; };

        // check pid with regular expression
        if !self.re_pid.is_match(&val.pid.as_ref().unwrap()) { return false; };

        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in";

    const CONTENT_INVALID: &str = "eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007";

    const CONTENT_VALID: &str = "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719";


    #[test]
    fn test_passport_parse() {
        let passports = Passport::parse(CONTENT)
            .expect("Could not parse passports");

        assert_eq!(passports.len(), 4);
    }

    #[test]
    fn test_passport_has_required_fields() {
        let passports = Passport::parse(CONTENT)
            .expect("Could not parse passports");

        assert_eq!(passports[0].has_required_fields(), true, "{:?}", passports[0]);
        assert_eq!(passports[1].has_required_fields(), false, "{:?}", passports[1]);
        assert_eq!(passports[2].has_required_fields(), true, "{:?}", passports[2]);
        assert_eq!(passports[3].has_required_fields(), false, "{:?}", passports[3]);
    }

    #[test]
    fn test_passport_is_valid() {
        let passports_invalid = Passport::parse(CONTENT_INVALID)
            .expect("Could not parse passports");
        let passports_valid = Passport::parse(CONTENT_VALID)
            .expect("Could not parse passports");

        assert_eq!(count_valid(&passports_invalid), 0);
        assert_eq!(count_valid(&passports_valid), passports_valid.len());
    }
}