use std::collections::{BTreeSet, VecDeque, BTreeMap};
use regex::Regex;
use std::fs;

fn main() {
    let content = fs::read_to_string("input.txt")
        .expect("Failed to read from file");

    let bags = Bag::parse(&content);

    let parents = explore_parents(&bags, "shiny gold");
    println!("Found {} containers for shiny gold bags", parents.len());
    assert_eq!(parents.len(), 235);

    // tag::sol2[]
    let count = count_children(&bags, "shiny gold") - 1;
    // end::sol2[]
    println!("Shiny gold bags contain {} bags", count);
    assert_eq!(count, 158493);
}

// tag::explore_parents[]
fn explore_parents<'a>(bags: &'a BTreeMap<String, Bag>, color: &str) -> BTreeSet<&'a str> {
    // breadth first search
    let mut parents: BTreeSet<&str> = BTreeSet::new();
    let mut queue: VecDeque<&str> = VecDeque::new();
    queue.push_back(color);

    while !queue.is_empty() {
        let color = queue.pop_front().expect("Queue is empty?!");

        for bag in bags.values().filter(|bag| bag.contains.contains_key(color)) {
            // if parent has not yet been visited, push to queue
            if parents.insert(&bag.color) {
                queue.push_back(&bag.color);
            }
        }
    };

    parents
}
// end::explore_parents[]

// tag::count_children[]
fn count_children(bags: &BTreeMap<String, Bag>, color: &str) -> i32 {
    // find bag, expect to be present if problem is well-formed
    let bag = bags.get(color)
        .expect("Bag not found");

    // recursively find children
    1 + bag.contains.iter().fold(
        0, |acc,
            (color, count)| acc + count * count_children(bags, color),
    )
}
// end::count_children[]

#[derive(Debug, PartialEq)]
struct Bag {
    color: String,
    contains: BTreeMap<String, i32>,
}

impl Bag {
    fn parse(content: &str) -> BTreeMap<String, Bag> {
        let re_line = Regex::new(r"(\w+ \w+) bags contain ([^.]*)")
            .expect("Illegal regular expression");
        let re_cont = Regex::new(r"(\d+) (\w+ \w+) bag(s?)(, |$)")
            .expect("Illegal regular expression");

        content.lines().map(|line| {
            let cap = re_line.captures(line)
                .expect("Line does not match");

            (
                String::from(&cap[1]),
                Bag {
                    color: String::from(&cap[1]),
                    contains: re_cont.captures_iter(&cap[2])
                        .map(|c|
                            (
                                String::from(&c[2]),
                                c[1].parse().expect("Could not parse number")
                            )
                        )
                        .collect(),
                }
            )
        }).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.";

    const CONTENT2: &str = "shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.";

    #[test]
    fn test_bag_parse() {
        let bags = Bag::parse(CONTENT);
        assert_eq!(bags.len(), 9);
    }

    #[test]
    fn test_explore_parents() {
        let bags = Bag::parse(CONTENT);
        let parents = explore_parents(&bags, "shiny gold");

        assert_eq!(parents.len(), 4);
        assert!(parents.contains("bright white"));
        assert!(parents.contains("muted yellow"));
        assert!(parents.contains("dark orange"));
        assert!(parents.contains("light red"));
    }

    #[test]
    fn test_count_children() {
        let bags = Bag::parse(CONTENT);
        let count = count_children(&bags, "shiny gold");

        // subtract self to get expected number of children
        assert_eq!(count - 1, 32);

        let bags = Bag::parse(CONTENT2);
        let count = count_children(&bags, "shiny gold");

        // subtract self to get expected number of children
        assert_eq!(count - 1, 126);
    }
}
