use std::collections::{HashMap, HashSet};

// tag::rule[]
#[derive(Debug, PartialEq)]
pub enum Rule {
    Sequence(usize, Vec<usize>),
    Alternative(usize, Vec<usize>, Vec<usize>),
}
// end::rule[]

impl Rule {
    pub fn parse(content: &str) -> (HashMap<usize, Rule>, HashMap<char, usize>) {
        let mut map = HashMap::new();
        let mut rule = HashMap::new();

        for line in content.lines() {
            let mut parts = line.split(": ");
            let id: usize = parts.next().expect("No ID").parse().expect("Illegal ID");
            let line = parts.next().expect("No Content");
            if line.starts_with("\"") {
                let c = line[1..].chars().next().expect("No character");
                map.insert(c, id);
            } else {
                let mut parts = line.split(" | ");
                let opt_a: Vec<_> = parts.next().expect("No list")
                    .split(" ")
                    .map(|part| part.parse::<usize>().expect("Could not parse"))
                    .collect();
                let opt_b: Option<Vec<_>> = parts.next().map(|list|
                    list.split(" ")
                        .map(|part| part.parse::<usize>().expect("Could not parse"))
                        .collect());
                rule.insert(id, if let Some(opt_b) = opt_b {
                    Rule::Alternative(id, opt_a, opt_b)
                } else {
                    Rule::Sequence(id, opt_a)
                });
            }
        }

        (rule, map)
    }
}

pub fn parse(content: &str) -> (HashMap<char, usize>, HashMap<usize, Rule>, &str) {
    let mut parts = content.split("\n\n");
    let rules = parts.next().expect("No rules");
    let patterns = parts.next().expect("No patterns");

    let (rules, map) = Rule::parse(rules);

    (map, rules, patterns)
}

pub fn matches(map: &HashMap<char, usize>, rules: &HashMap<usize, Rule>, content: &str) -> usize {
    // set of leaf nodes
    let mut leaves = HashSet::new();
    map.iter().for_each(|(_, v)| { leaves.insert(*v); });

    // sequence of rule 0 is start pattern
    let cand_0 = if let Some(Rule::Sequence(_, seq)) = rules.get(&0) {
        seq
    } else {
        panic!("No rule 0 found.");
    };

    content.lines().filter(|line| {
        let content: Vec<_> = line.chars()
            .map(|c| *map.get(&c).expect("Illegal char."))
            .collect();
        matches_int(&leaves, rules, &cand_0, &content)
    }).count()
}

// tag::match_int[]
fn matches_int(
    leaves: &HashSet<usize>,
    rules: &HashMap<usize, Rule>,
    cand: &[usize],
    content: &[usize]) -> bool
{
    let mut start = 0;
    while leaves.contains(&cand[start]) {
        // heads do not match, return false
        if cand[start] != content[start] {
            return false;
        }
        // if all matches return true
        start += 1;
        if start == content.len() && start == cand.len() {
            return true;
        }
        // if not all matches and content or cand exhausted, return false
        if start >= content.len() || start >= cand.len() {
            return false;
        }
    };

    match rules.get(&cand[start]) {
        Some(Rule::Sequence(_, a)) => {
            let mut next = Vec::with_capacity(cand.len() - start - 1 + a.len());
            a.iter().for_each(|a| next.push(*a));
            cand[start + 1..].iter().for_each(|a| next.push(*a));
            return matches_int(leaves, rules, &next, &content[start..]);
        }
        Some(Rule::Alternative(_, a, b)) => {
            let mut next1 = Vec::with_capacity(cand.len() - start - 1 + a.len());
            a.iter().for_each(|a| next1.push(*a));
            cand[start + 1..].iter().for_each(|a| next1.push(*a));

            let mut next2 = Vec::with_capacity(cand.len() - start - 1 + b.len());
            b.iter().for_each(|a| next2.push(*a));
            cand[start + 1..].iter().for_each(|a| next2.push(*a));

            return matches_int(leaves, rules, &next1, &content[start..]) ||
                matches_int(leaves, rules, &next2, &content[start..]);
        }
        None => panic!("Not rule found"),
    }
}
// end::match_int[]

#[cfg(test)]
mod tests {
    use super::*;

    const RULES: &str = "0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: \"a\"
5: \"b\"";

    const CONTENT: &str = "0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: \"a\"
5: \"b\"

ababbb
bababa
abbbab
aaabbb
aaaabbb";

    const CONTENT2: &str = "42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: \"a\"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: \"b\"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba";

    #[test]
    fn test_rule_parse() {
        let (rules, map) = Rule::parse(RULES);

        let mut exp_rules = HashMap::new();
        exp_rules.insert(0, Rule::Sequence(0, vec![4, 1, 5]));
        exp_rules.insert(1, Rule::Alternative(1, vec![2, 3], vec![3, 2]));
        exp_rules.insert(2, Rule::Alternative(2, vec![4, 4], vec![5, 5]));
        exp_rules.insert(3, Rule::Alternative(3, vec![4, 5], vec![5, 4]));

        let mut exp_map = HashMap::new();
        exp_map.insert('a', 4);
        exp_map.insert('b', 5);

        assert_eq!(rules, exp_rules);
        assert_eq!(map, exp_map);
    }

    #[test]
    fn test_matches_single() {
        let (rules, map) = Rule::parse(RULES);
        assert_eq!(matches(&map, &rules, "ababbb"), 1);
        assert_eq!(matches(&map, &rules, "bababa"), 0);
        assert_eq!(matches(&map, &rules, "abbbab"), 1);
        assert_eq!(matches(&map, &rules, "aaabbb"), 0);
        assert_eq!(matches(&map, &rules, "aaaabbb"), 0);
    }

    #[test]
    fn test_matches_multi() {
        let (map, rules, patterns) =
            parse(CONTENT);

        assert_eq!(matches(&map, &rules, patterns), 2);
    }

    #[test]
    fn test_matches_part2() {
        let (map, mut rules, patterns) =
            parse(CONTENT2);

        assert_eq!(matches(&map, &rules, patterns), 3);

        rules.insert(8, Rule::Alternative(8, vec![42], vec![42, 8]));
        rules.insert(11, Rule::Alternative(8, vec![42, 31], vec![42, 11, 31]));

        assert_eq!(matches(&map, &rules, patterns), 12);
    }
}