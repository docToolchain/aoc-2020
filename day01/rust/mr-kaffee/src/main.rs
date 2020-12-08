use std::error::Error;
use std::fs;

fn part1(list: &[i32]) -> Result<i32, &str> {
    // find 2-combination that sums to 2020
    // idx values start counting from 0,
    // indices to slice are
    //   i1 = idx1,
    //   i2 = idx1 + idx2 + 1
    for (idx1, v1) in list[..list.len() - 1].iter().enumerate() {
        for (idx2, v2) in list[idx1 + 1..].iter().enumerate() {
            if v1 + v2 == 2020 {
                println!(
                    "Values at {}/{}: {} + {} = 2020",
                    idx1,
                    idx1 + idx2 + 1,
                    v1,
                    v2
                );
                return Ok(v1 * v2);
            }
        }
    }

    Err("Could not solve part 1")
}

fn part2(list: &[i32]) -> Result<i32, &str> {
    // find 3-combination that sums to 2020
    // idx values start counting from 0
    // indices to slice are
    //   i1 = idx1,
    //   i2 = idx1 + idx2 + 1,
    //   i3 = idx1 + idx2 + idx3 + 2
    for (idx1, v1) in list[..list.len() - 2].iter().enumerate() {
        for (idx2, v2) in list[idx1 + 1..list.len() - 1].iter().enumerate() {
            // if v1 + v2 >= 2020, there is no way that v1 + v2 + v3 == 2020
            if v1 + v2 >= 2020 {
                continue;
            }

            for (idx3, v3) in list[idx1 + idx2 + 2..].iter().enumerate() {
                if v1 + v2 + v3 == 2020 {
                    println!(
                        "Values at {}/{}/{}: {} + {} + {} = 2020",
                        idx1,
                        idx1 + idx2 + 1,
                        idx1 + idx2 + idx3 + 2,
                        v1,
                        v2,
                        v3
                    );
                    return Ok(v1 * v2 * v3);
                }
            }
        }
    }

    Err("Could not solve part 2")
}

fn read_input() -> Result<Vec<i32>, Box<dyn Error>> {
    let content = fs::read_to_string("input.txt")?;

    let mut list: Vec<i32> = Vec::new();
    for line in content.lines() {
        list.push(line.parse()?);
    }

    Ok(list)
}

fn main() -> Result<(), Box<dyn Error>> {
    let list = read_input()?;

    // solve part 1, check & print
    let r1 = part1(&list)?;
    assert_eq!(r1, 381_699);
    println!("Solved part 1: {}", r1);

    // solve part 2, check & print
    let r2 = part2(&list)?;
    assert_eq!(r2, 111_605_670);
    println!("Solved part 2: {}", r2);

    Ok(())
}
