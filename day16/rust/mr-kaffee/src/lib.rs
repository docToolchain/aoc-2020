const YOUR_TICKET: &str = "your ticket:";
const NEARBY_TICKETS: &str = "nearby tickets:";

#[derive(Debug, PartialEq, Hash)]
pub struct Rule {
    name: String,
    range1: (i32, i32),
    range2: (i32, i32),
}

impl Rule {
    fn matches(&self, value: i32) -> bool {
        (value >= self.range1.0 && value <= self.range1.1) ||
            (value >= self.range2.0 && value <= self.range2.1)
    }
}

// tag::parse[]
pub fn parse(content: &str) -> (Vec<Rule>, Vec<i32>, Vec<Vec<i32>>, i32) {
    let mut mode = 0;
    let re = regex::Regex::new(r"([^:]+): (\d+)-(\d+) or (\d+)-(\d+)")
        .expect("Invalid regular expression");

    let mut rules = Vec::new();
    let mut my_pass = Vec::new();
    let mut nearby_passes = Vec::new();
    let mut invalids = 0;

    for line in content.lines() {
        match line {
            YOUR_TICKET => {
                mode = 1;
                continue;
            }
            NEARBY_TICKETS => {
                mode = 2;
                continue;
            }
            _ if line.len() == 0 => continue,
            _ => (),
        };

        match mode {
            0 => {
                let cap = re.captures(line).expect("Unexpected rule");
                let name = String::from(&cap[1]);
                let range1 = (
                    cap[2].parse().expect("Illegal from 1"),
                    cap[3].parse().expect("Illegal to 1"));
                let range2 = (
                    cap[4].parse().expect("Illegal from 2"),
                    cap[5].parse().expect("Illegal to 2"));
                rules.push(Rule { name, range1, range2 });
            }
            1 => {
                my_pass.extend(line.split(",")
                    .map(|v| v.parse::<i32>().expect("Could not parse number")));
                assert_eq!(rules.len(), my_pass.len());
            }
            2 => {
                let pass: Vec<_> = line.split(",")
                    .map(|v| v.parse::<i32>().expect("Could not parse number"))
                    .collect();
                assert_eq!(rules.len(), pass.len());
                let invalid = pass.iter()
                    .filter(|v| !rules.iter().any(|rule| rule.matches(**v)))
                    .fold((0, 0), |(cnt, sum), v| (cnt + 1, sum + *v));
                if invalid.0 == 0 {
                    nearby_passes.push(pass);
                }
                invalids += invalid.1;
            }
            _ => panic!("Illegal mode")
        }
    };

    (rules, my_pass, nearby_passes, invalids)
}
// end::parse[]

// tag::find_fields[]
pub fn find_fields(rules: &[Rule], passes: &[Vec<i32>], prefix: &str) -> Vec<(usize, usize)> {
    let n = rules.len();

    // i = r + f * n -> r = i % n, f 0 i / n
    let mut candidates = (0..n * n)
        .map(|i|
            passes.iter().all(|pass| rules[i % n].matches(pass[i / n])))
        .collect();

    // At this point, we have a matrix with a column for each rule and a row for each field
    // the matrix entries are true, if the rule is a candidate for the field and false otherwise.
    // Candidates are eliminated as follows:
    // - if a rule is a candidate for exactly one field, no other rule can be a candidate for the
    //   same field
    // - if a field is a candidate for exactly one rule, no other field can be a candidate for the
    //   same rule
    while reduce_2d(&mut candidates, n) > 0 {}

    // exactly one rule per field and vice versa
    assert!(
        (0..n).all(|r| (0..n).filter(|f| candidates[r + f * n]).count() == 1),
        "Could not reduce candidates");
    assert!(
        (0..n).all(|f| (0..n).filter(|r| candidates[r + f * n]).count() == 1),
        "Could not reduce candidates");

    (0..n).filter(|r| rules[*r].name.starts_with(prefix))
        .map(|r| (r, (0..n).find(|f| candidates[r + f * n]).unwrap()))
        .collect::<Vec<_>>()
}
// end::find_fields[]

/// Reduce along both dimensions
/// Return the number of removed candidates
fn reduce_2d(candidates: &mut Vec<bool>, n: usize) -> i32 {
    reduce_1d(candidates, n, |y, x| x + n * y) +
        reduce_1d(candidates, n, |x, y| x + n * y)
}

// tag::reduce_1d[]
/// Reduce square `n x n` matrix along one dimension
///
/// The function `f` maps positions in dimensions 1 and 2 to a flat index. It should be set to
/// `|col, row| -> col + n * row` if the first dimension is the column and the second is the row.
/// It should be set to `|row, col| -> col -> n * row` if the first dimension is the row and the
/// second dimension is the column.
///
/// If there is a row/column in the second dimension, which contains exactly one candidate, this
/// candidate is removed from all other columns/rows
fn reduce_1d<F>(candidates: &mut Vec<bool>, n: usize, f: F) -> i32
    where F: Fn(usize, usize) -> usize
{
    let mut removed = 0;
    for k1 in 0..n {
        // find unique in dimension 2
        let mut unique_k2 = None;
        for k2 in 0..n {
            if candidates[f(k1, k2)] {
                if unique_k2.is_none() {
                    // first element found
                    unique_k2 = Some(k2);
                } else {
                    // second element found -> no unique element
                    unique_k2 = None;
                    break;
                }
            }
        }

        if let Some(k2) = unique_k2 {
            for l1 in 0..n {
                if l1 == k1 {
                    continue;
                }

                if candidates[f(l1, k2)] {
                    removed += 1;
                    candidates[f(l1, k2)] = false;
                }
            }
        }
    }

    removed
}
// end::reduce_1d[]

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT_1: &str = "class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12";

    const CONTENT_2: &str = "class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9";

    fn exp_rules() -> Vec<Rule> {
        vec![
            Rule { name: String::from("class"), range1: (1, 3), range2: (5, 7) },
            Rule { name: String::from("row"), range1: (6, 11), range2: (33, 44) },
            Rule { name: String::from("seat"), range1: (13, 40), range2: (45, 50) }
        ]
    }

    #[test]
    fn test_parse() {
        let (rules, my_pass, nearby_passes, invalids) =
            parse(CONTENT_1);
        assert_eq!(rules, exp_rules());
        assert_eq!(my_pass, vec![7, 1, 14]);
        assert_eq!(nearby_passes, vec![vec![7, 3, 47]]);
        assert_eq!(invalids, 71);
    }

    #[test]
    fn test_define_fields() {
        let (rules, my_pass, nearby_passes, _) =
            parse(CONTENT_2);

        let fields = find_fields(&rules, &nearby_passes, "");
        assert_eq!(my_pass[fields[0].1], 12);
        assert_eq!(my_pass[fields[1].1], 11);
        assert_eq!(my_pass[fields[2].1], 13);

        let fields = find_fields(&rules, &nearby_passes, "class");
        assert_eq!(fields, vec![(0, 1)]);
    }
}