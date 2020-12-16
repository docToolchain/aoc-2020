use std::fs;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

// tag::parse_input[]
fn parse_input(content: &str) -> Vec<u32> {
    let mut list: Vec<u32> = content.lines()
        .map(|line| line.parse().expect("Could not parse number"))
        .collect();
    list.push(0);
    list.sort_unstable();
    list.push(list.last().expect("Empty list?!?") + 3);

    list
}
// end::parse_input[]

// tag::to_deltas[]
fn to_deltas(list: &[u32]) -> Vec<u32> {
    list.iter().zip(list[1..].iter())
        .map(|(a, b)| b - a).collect()
}
// end::to_deltas[]

// tag::count_deltas[]
fn count_deltas(deltas: &[u32]) -> (usize, usize, usize) {
    deltas.iter()
        .fold((0, 0, 0), |(ones, twos, threes), v|
            match v {
                1 => (ones + 1, twos, threes),
                2 => (ones, twos + 1, threes),
                3 => (ones, twos, threes + 1),
                _ => panic!(format!("Unexpected delta: {}", v))
            },
        )
}
// end::count_deltas[]

// tag::find_one_groups[]
fn find_one_groups(deltas: &[u32]) -> Vec<usize> {
    let mut groups = Vec::new();

    let mut cnt = 1;
    for v in deltas {
        if *v == 1 {
            cnt += 1;
        } else {
            // groups of size <= 2 are not relevant
            if cnt > 2 {
                groups.push(cnt);
            }
            cnt = 1;
        }
    }

    groups
}
// end::find_one_groups[]

// tag::count_combinations[]
fn count_combinations(groups: &[usize]) -> u64 {
    groups.iter().map(|g| match g {
        3 => 2,
        4 => 4,
        5 => 7,
        v => panic!(format!("Cannot handle group size {}", v))
    }).product()
}
// end::count_combinations[]

fn main() {
    let content = parse_input(&read_input());
    let deltas = to_deltas(&content);
    let (ones, twos, threes) = count_deltas(&deltas);

    println!("ones: {}, twos: {}, threes: {} => {}", ones, twos, threes, ones * threes);
    assert_eq!(ones * threes, 2475);

    assert_eq!(twos, 0, "Assume there are no distance of two between any two adaptors");
    let combinations = count_combinations(&find_one_groups(&deltas));
    println!("combinations: {}", combinations);
    assert_eq!(combinations, 442_136_281_481_216)
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT_1: &str = "16
10
15
5
1
11
7
19
6
12
4";

    const CONTENT_2: &str = "28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3";

    #[test]
    fn test_part1() {
        let (ones, twos, threes) =
            count_deltas(&to_deltas(&parse_input(&CONTENT_2)));

        println!("ones: {}, twos: {}, threes: {}", ones, twos, threes);

        assert_eq!((ones, threes), (22, 10));
    }

    fn do_test_part2(content: &str, exp_groups: &[usize], exp_product: u64) {
        let list = parse_input(content);
        let deltas = to_deltas(&list);
        let groups = find_one_groups(&deltas);
        assert_eq!(groups, exp_groups);

        let combinations = count_combinations(&groups);
        assert_eq!(combinations, exp_product);
    }

    #[test]
    fn test_part2() {
        do_test_part2(&CONTENT_1, &vec![4, 3], 8);
        do_test_part2(&CONTENT_2, &vec![5, 5, 4, 3, 5, 5], 19_208);
    }
}