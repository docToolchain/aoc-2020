use std::collections::HashMap;

// tag::rule[]
#[derive(Debug, PartialEq)]
pub enum Rule {
    Sequence(Vec<usize>),
    Alternative(Vec<usize>, Vec<usize>),
    Leaf(char),
}
// end::rule[]

impl Rule {
    pub fn parse(content: &str) -> HashMap<usize, Rule> {
        let mut rules = HashMap::new();

        for line in content.lines() {
            let mut parts = line.split(": ");
            let id: usize = parts.next().expect("No ID").parse().expect("Illegal ID");
            let line = parts.next().expect("No Content");
            if line.starts_with("\"") {
                let c = line[1..].chars().next().expect("No character");
                rules.insert(id, Rule::Leaf(c));
            } else {
                let patterns: Vec<Vec<_>> = line.split(" | ")
                    .map(|sequence| sequence.split(" ").map(|v|
                        v.parse::<usize>().expect("Illegal rule ref")).collect())
                    .collect();
                rules.insert(id, match patterns.len() {
                    1 => Rule::Sequence(patterns[0].clone()),
                    2 => Rule::Alternative(patterns[0].clone(), patterns[1].clone()),
                    _ => panic!("Bad rule"),
                });
            }
        }

        rules
    }
}

pub fn parse(content: &str) -> (HashMap<usize, Rule>, &str) {
    let mut parts = content.split("\n\n");

    (Rule::parse(parts.next().expect("No rules")),
     parts.next().expect("No texts"))
}

pub fn matches(rules: &HashMap<usize, Rule>, texts: &str) -> usize {
    // sequence of rule 0 is start pattern
    let pattern = if let Some(Rule::Sequence(pattern)) = rules.get(&0) {
        pattern
    } else {
        panic!("No rule 0 as sequence found.");
    };

    texts.lines().filter(|text|
        matches_int(rules, &pattern, &text.chars().collect::<Vec<_>>())).count()
}

// tag::match_int[]
fn matches_int(rules: &HashMap<usize, Rule>, pattern: &[usize], text: &[char]) -> bool {
    let mut k = 0;
    while let Some(Rule::Leaf(c)) = rules.get(&pattern[k]) {
        // heads do not match, return false
        if *c != text[k] { return false; }
        k += 1;

        // if all matches return true
        if k == text.len() && k == pattern.len() { return true; }

        // if not all matches and content or candidate exhausted, return false
        if k >= text.len() || k >= pattern.len() { return false; }
    };

    match rules.get(&pattern[k]) {
        Some(Rule::Sequence(a)) =>
            matches_int(rules, &[&a, &pattern[k + 1..]].concat(), &text[k..]),
        Some(Rule::Alternative(a, b)) =>
            matches_int(rules, &[&a, &pattern[k + 1..]].concat(), &text[k..]) ||
                matches_int(rules, &[&b, &pattern[k + 1..]].concat(), &text[k..]),
        _ => panic!("Unexpected leaf node or rule not found"),
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
        let rules = Rule::parse(RULES);

        let mut exp_rules = HashMap::new();
        exp_rules.insert(0, Rule::Sequence(vec![4, 1, 5]));
        exp_rules.insert(1, Rule::Alternative(vec![2, 3], vec![3, 2]));
        exp_rules.insert(2, Rule::Alternative(vec![4, 4], vec![5, 5]));
        exp_rules.insert(3, Rule::Alternative(vec![4, 5], vec![5, 4]));
        exp_rules.insert(4, Rule::Leaf('a'));
        exp_rules.insert(5, Rule::Leaf('b'));

        assert_eq!(rules, exp_rules);
    }

    #[test]
    fn test_matches_single() {
        let rules = Rule::parse(RULES);
        assert_eq!(matches(&rules, "ababbb"), 1);
        assert_eq!(matches(&rules, "bababa"), 0);
        assert_eq!(matches(&rules, "abbbab"), 1);
        assert_eq!(matches(&rules, "aaabbb"), 0);
        assert_eq!(matches(&rules, "aaaabbb"), 0);
    }

    #[test]
    fn test_matches_multi() {
        let (rules, texts) = parse(CONTENT);

        assert_eq!(matches(&rules, texts), 2);
    }

    #[test]
    fn test_matches_part2() {
        let (mut rules, texts) = parse(CONTENT2);

        assert_eq!(matches(&rules, texts), 3);

        rules.insert(8, Rule::Alternative(vec![42], vec![42, 8]));
        rules.insert(11, Rule::Alternative(vec![42, 31], vec![42, 11, 31]));

        assert_eq!(matches(&rules, texts), 12);
    }
}