use std::{fs, cmp};

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
fn find_contiguous(list: &[i64], val: i64) -> i64 {
    for (i1, v1) in list[..list.len() - 1].iter().enumerate() {
        let mut sum = *v1;
        let mut min = *v1;
        let mut max = *v1;

        for v2 in &list[i1 + 1..] {
            sum = sum + v2;
            min = cmp::min(min, *v2);
            max = cmp::max(max, *v2);
            if sum >= val {
                break;
            }
        }

        if sum == val {
            // match found, return sum of smallest and largest number in range
            return min + max;
        }
    }

    // I will only end up here, if no matching range was found
    panic!("Nothing found.");
}
// end::find_contiguous[]

// tag::find_fail[]
fn find_fail(list: &[i64], len: usize) -> i64 {
    let pos = (len..list.len())
        .find(|pos| !check_pos(list, *pos, len))
        .expect("Nothing found.");
    list[pos]
}
// end::find_fail[]

// tag::check_pos[]
fn check_pos(list: &[i64], pos: usize, len: usize) -> bool {
    // again those ugly nested for loops :(
    for a in list[pos - len..pos - 1].iter() {
        for b in list[pos - len + 1..pos].iter() {
            if a + b == list[pos] {
                return true;
            }
        }
    }

    false
}
// end::check_pos[]

fn parse(content: &str) -> Vec<i64> {
    content.lines()
        .map(|line| line.parse::<i64>().expect("Parse error"))
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

    fn numbers() -> Vec<i64> {
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