use std::fs;
use std::error::Error;
use std::time::Instant;

use itertools::Itertools;

// tag::generic_no_iter[]
fn solve_generic_no_iter(list: &[i32], n: usize) -> i32 {
    let mut indices: Vec<usize> = (0..n).collect();
    while indices[n - 1] <= list.len() {
        // if sum matches, return product
        if indices.iter().fold(0, |sum, idx| sum + list[*idx]) == 2020 {
            return indices.iter().fold(1, |prod, idx| prod * list[*idx]);
        }

        // update indices
        let mut i = 0;
        // find first index which can be incremented
        while i < indices.len() - 1 && indices[i] == indices[i + 1] - 1 {
            i += 1;
        }
        // increment index
        indices[i] += 1;
        // reset all lower indices
        for j in 0..i {
            indices[j] = j;
        }
    }

    panic!("Nothing found.");
}
// end::generic_no_iter[]

// tag::generic[]
fn solve_generic(list: &[i32], n: usize) -> i32 {
    list.iter().combinations(n)
        .find(|v| v.iter().map(|a| *a).sum::<i32>() == 2020)
        .expect("Nothing found").into_iter()
        .product()
}
// end::generic[]

fn solve_two(list: &[i32]) -> i32 {
    let (a, b) = list.iter().tuple_combinations()
        .find(|(a, b)| *a + *b == 2020)
        .expect("Nothing found.");

    a * b
}

// tag::part2[]
fn solve_three(list: &[i32]) -> i32 {
    let (a, b, c) = list.iter().tuple_combinations()
        .find(|(a, b, c)| *a + *b + *c == 2020)
        .expect("Nothing found");

    a * b * c
}
// end::part2[]

fn read_input() -> Result<Vec<i32>, Box<dyn Error>> {
    let content = fs::read_to_string("input.txt")?;

    let mut list: Vec<i32> = Vec::new();
    for line in content.lines() {
        list.push(line.parse()?);
    }

    Ok(list)
}

fn main() {
    let list = read_input()
        .expect("Could not read from file");

    // solve part 1, check & print
    let now = Instant::now();
    let r1 = solve_two(&list);
    println!("Solved part 1 with tuple combinations in {} ms -> {}", now.elapsed().as_millis(), r1);
    assert_eq!(r1, 381_699);

    // solve with generic method
    let now = Instant::now();
    let r1 = solve_generic(&list, 2);
    println!("Solved part 1 with vec combinations in {} ms -> {}", now.elapsed().as_millis(), r1);
    assert_eq!(r1, 381_699);

    // solve with generic method without iterators
    let now = Instant::now();
    let r1 = solve_generic_no_iter(&list, 2);
    println!("Solved part 1 with generic solution without iterators in {} ms -> {}", now.elapsed().as_millis(), r1);
    assert_eq!(r1, 381_699);

    // solve part 2, check & print
    let now = Instant::now();
    let r2 = solve_three(&list);
    assert_eq!(r2, 111_605_670);
    println!("Solved part 2 with tuple combinations in {} ms -> {}", now.elapsed().as_millis(), r2);

    // solve with generic method without iterators
    let now = Instant::now();
    let r2 = solve_generic_no_iter(&list, 3);
    println!("Solved part 2 with generic solution without iterators in {} ms -> {}", now.elapsed().as_millis(), r2);
    assert_eq!(r2, 111_605_670);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_generic_no_iter() {
        let list = vec![1721,
                        979,
                        366,
                        299,
                        675,
                        1456];

        let prod = solve_generic_no_iter(&list, 2);
        assert_eq!(prod, 514_579);

        let prod = solve_generic_no_iter(&list, 3);
        assert_eq!(prod, 241_861_950);
    }
}
