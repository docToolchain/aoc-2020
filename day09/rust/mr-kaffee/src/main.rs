use std::{fs, cmp};
use itertools::Itertools;

fn main() {
    let content = fs::read_to_string("input.txt").expect("Failed to read file");

    let list = parse(&content);

    let val = find_fail(&list, 25);
    println!("Fails at {}", val);
    assert_eq!(val, 23_278_925);

    let chk = find_contiguous(&list, val);
    println!("Check is {}", chk);
    assert_eq!(chk, 4_011_064);
}

// tag::find_contiguous[]
fn find_contiguous(list: &[u64], val: u64) -> u64 {
    // O(n) algorithm - thanks Daniel Lin for the hint ;)

    let mut i1 = 0;
    let mut i2 = 0;
    let mut sum = 0;

    while sum != val && i2 < list.len() {
        while sum < val && i2 < list.len() {
            sum += list[i2];
            i2 += 1;
        }

        // if value is too big, move lower bound up
        // sum > val implies i1 < i2 because val >= 0 and sum = 0 if i1 == i2
        while sum > val {
            sum -= list[i1];
            i1 += 1;
        }
    }

    assert_eq!(sum, val, "Nothing found");

    let (min, max) = list[i1..i2].iter()
        .fold(
            (list[i1], list[i1]),
            |(min, max), v| (cmp::min(min, *v), cmp::max(max, *v)),
        );
    return min + max;
}
// end::find_contiguous[]

// tag::find_fail[]
fn find_fail(list: &[u64], len: usize) -> u64 {
    let pos = (len..list.len())
        .find(|pos| !check_pos(list, *pos, len))
        .expect("Nothing found.");
    list[pos]
}
// end::find_fail[]

// tag::check_pos[]
fn check_pos(list: &[u64], pos: usize, len: usize) -> bool {
    list[pos - len..pos].iter()
        .tuple_combinations()
        .find(|(a, b)| *a + *b == list[pos]).is_some()
}
// end::check_pos[]

fn parse(content: &str) -> Vec<u64> {
    content.lines()
        .map(|line| line.parse::<u64>().expect("Parse error"))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576";

    fn numbers() -> Vec<u64> {
        vec![35,
             20,
             15,
             25,
             47,
             40,
             62,
             55,
             65,
             95,
             102,
             117,
             150,
             182,
             127,
             219,
             299,
             277,
             309,
             576]
    }

    #[test]
    fn test_parse() {
        let list = parse(CONTENT);
        assert_eq!(list, numbers());
    }

    #[test]
    fn test_check_pos() {
        let list = numbers();
        assert!(check_pos(&list, 5, 5));
        assert!(check_pos(&list, 6, 5));
        assert!(!check_pos(&list, 14, 5));
    }

    #[test]
    fn test_find_fail() {
        let list = numbers();
        assert_eq!(find_fail(&list, 5), 127);
    }

    #[test]
    fn test_find_contiguous() {
        let list = numbers();
        assert_eq!(find_contiguous(&list, 127), 62);
    }
}