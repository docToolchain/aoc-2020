use std::fs;

fn main() {
    let content = fs::read_to_string("input.txt")
        .expect("Could not read from file");

    // parse into vector and sort
    let mut passes: Vec<u16> = content.lines()
        .map(|line| parse_pass(line))
        .collect();
    passes.sort_unstable();

    let max = passes.last().expect("No passes.");
    println!("Max ID is {}", max);
    assert_eq!(*max, 878);

    // tag::zip[]
    let (a, b) = passes.iter().zip(passes[1..].iter())
        .find(|(a, b)| *b - *a == 2)
        .expect("No seats with one in between found");
    // end::zip[]
    println!("{} -> {} -> {} ", a, a + 1, b);
    assert_eq!(a + 1, 504);
}

fn parse_pass(line: &str) -> u16 {
    line.chars().fold(0, |acc, sym| {
        match sym {
            'B' => (acc << 1) + 1,
            'F' => acc << 1,
            'R' => (acc << 1) + 1,
            'L' => acc << 1,
            other => panic!(format!("Unexpected symbol: {}", other)),
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_line() {
        assert_eq!(parse_pass("BFFFBBFRRR"), 567);
        assert_eq!(parse_pass("FFFBBBFRRR"), 119);
        assert_eq!(parse_pass("BBFFBBFRLL"), 820);
    }
}
