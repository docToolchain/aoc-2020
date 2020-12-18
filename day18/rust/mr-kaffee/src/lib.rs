use regex::Regex;

// tag::token[]
#[derive(PartialEq, Debug)]
pub enum Token {
    Open,
    Close,
    Plus,
    Times,
    Value(isize),
}

impl Token {
    pub fn parse(content: &str) -> Vec<Vec<Self>> {
        let re = Regex::new(r"\s*(\d+|[+*()])").expect("Illegal regular expression");
        let mut token_lines = Vec::new();
        for line in content.lines() {
            token_lines.push(re.captures_iter(line).map(|v| {
                match &v[1] {
                    "+" => Token::Plus,
                    "*" => Token::Times,
                    "(" => Token::Open,
                    ")" => Token::Close,
                    val => Token::Value(val.parse().expect("Could not parse value")),
                }
            }).collect());
        }
        token_lines
    }
}
// end::token[]

// tag::expression[]
#[derive(Debug)]
pub enum Expression {
    Leaf(isize),
    Sum(Box<Expression>, Box<Expression>),
    Prod(Box<Expression>, Box<Expression>),
    Nil,
}

impl Expression {
    pub fn evaluate(&self) -> isize {
        match self {
            Expression::Leaf(v) => *v,
            Expression::Sum(a, b) => a.evaluate() + b.evaluate(),
            Expression::Prod(a, b) => a.evaluate() * b.evaluate(),
            _ => panic!("Cannot evaluate Nil"),
        }
    }
}
// end::expression[]

pub fn evaluate1(tokens: &[Token]) -> isize {
    to_expression(tokens, true, false).0.evaluate()
}

pub fn evaluate2(tokens: &[Token]) -> isize {
    to_expression(tokens, true, true).0.evaluate()
}

// tag::to_expression[]
fn to_expression(tokens: &[Token], greedy: bool, precedence: bool) -> (Expression, usize) {
    let mut tree = Expression::Nil;

    let mut k = 0;
    while k < tokens.len() {
        tree = match tokens[k] {
            Token::Value(v) => Expression::Leaf(v),
            Token::Times => {
                let (rhs, k_int) = to_expression(
                    &tokens[k + 1..], precedence, precedence);
                k += k_int;
                Expression::Prod(Box::new(tree), Box::new(rhs))
            }
            Token::Plus => {
                let (rhs, k_int) = to_expression(
                    &tokens[k + 1..], false, precedence);
                k += k_int;
                Expression::Sum(Box::new(tree), Box::new(rhs))
            }
            Token::Open => {
                let mut idx = None;
                let mut level = 1;
                for l in k+1 .. tokens.len() {
                    level = match tokens[l] {
                        Token::Open => level + 1,
                        Token::Close => level - 1,
                        _ => level,
                    };
                    if level == 0 {
                        idx = Some(l);
                        break;
                    }
                }
                let idx = idx.expect("No matching bracket");
                let (rhs, k_int) = to_expression(
                    &tokens[k + 1..idx], true, precedence);
                k += k_int + 1;
                rhs
            }
            Token::Close => {
                panic!("What should I do here?")
            }
        };
        k += 1;
        if !greedy { break; }
    }

    (tree, k)
}
// end::to_expression[]

#[cfg(test)]
mod tests {
    use super::*;
    use crate::Token::{Value, Plus, Open, Close, Times};

    #[test]
    fn test_evaluate1() {
        let a = evaluate1(&Token::parse("1 + 2 * 3 + 4 * 5 + 6")[0]);
        assert_eq!(a, ((((1 + 2) * 3) + 4) * 5) + 6);
    }

    #[test]
    fn test_evaluate2() {
        let a = evaluate2(&Token::parse("1 + 2")[0]);
        assert_eq!(a, 3);

        let a = evaluate2(&Token::parse("1 * 2")[0]);
        assert_eq!(a, 2);

        let a = evaluate2(&Token::parse("2 * 1 + 3")[0]);
        assert_eq!(a, 8);

        let a = evaluate2(&Token::parse("1 + (2 * 3) + (4 * (5 + 6))")[0]);
        assert_eq!(a, 51);

        let a = evaluate2(&Token::parse("1 + 2 * 3 + 4 * 5 + 6")[0]);
        assert_eq!(a, 231);
    }

    #[test]
    fn test_token_parse() {
        let token_lines = Token::parse("1 + (2 * 3) + (4 * (5 + 6))");
        assert_eq!(token_lines, vec![vec![
            Value(1), Plus, Open, Value(2), Times, Value(3), Close, Plus,
            Open, Value(4), Times, Open, Value(5), Plus, Value(6), Close, Close]]);
    }
}
