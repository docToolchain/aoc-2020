use std::fs;

// tag::part[]
fn part<F>(content: &str, init: i32, f: F) -> (u32, u32)
    where F: Fn(i32, i32) -> i32
{
    // counter for non-empty groups and sum over elements
    let mut cnt: u32 = 0;
    let mut sum: u32 = 0;

    // initialize mask
    let mut msk: i32 = init;

    for line in content.lines() {
        if line.len() == 0 {
            // new group starts
            if msk > 0 {
                // found non-empty group
                cnt += 1;
                sum += msk.count_ones();
            }
            // reset mask
            msk = init;
        } else {
            // update mask with bits from line
            msk = f(
                msk,
                line.chars().fold(0, |acc, v| acc | 1 << (v as i32 - 'a' as i32))
            );
        }
    }
    // handle final group
    if msk > 0 {
        cnt += 1;
        sum += msk.count_ones();
    }

    println!("Found {} groups with {} yes'", cnt, sum);

    // return count and sum
    (cnt, sum)
}
// end::part[]

fn main() {
    let content = fs::read_to_string("input.txt")
        .expect("Could not read file");

    // tag::part1[]
    let (_, sum1) = part(&content, 0, |acc, val| acc | val);
    // end::part1[]
    assert_eq!(sum1, 6530);

    // tag::part2[]
    let (_, sum2) = part(&content, (1 << 27) - 1, |acc, val| acc & val);
    // end::part2[]
    assert_eq!(sum2, 3323);
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "abc

a
b
c

ab
ac

a
a
a
a

b";

    #[test]
    fn test_part() {
        let (cnt, sum) = part(
            CONTENT, 0, |acc, val| acc | val
        );
        assert_eq!(cnt, 5);
        assert_eq!(sum, 11);

        let (cnt, sum) = part(
            CONTENT, (1 << 27) - 1, |acc, val| acc & val
        );
        assert_eq!(cnt, 4);
        assert_eq!(sum, 6);
    }
}
