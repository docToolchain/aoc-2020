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
        content.lines().map(|line| re.captures_iter(line).map(|v| {
            match &v[1] {
                "+" => Token::Plus,
                "*" => Token::Times,
                "(" => Token::Open,
                ")" => Token::Close,
                val => Token::Value(val.parse().expect("Could not parse value")),
            }
        }).collect()).collect()
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
    let mut upd = (Expression::Nil, 0);
    while upd.1 < tokens.len() {
        upd = match tokens[upd.1] {
            Token::Value(v) => (Expression::Leaf(v), upd.1 + 1),
            Token::Times => {
                let (rhs, k_int) = to_expression(
                    &tokens[upd.1 + 1..], precedence, precedence);
                (Expression::Prod(Box::new(upd.0), Box::new(rhs)), upd.1 + k_int + 1)
            }
            Token::Plus => {
                let (rhs, k_int) = to_expression(
                    &tokens[upd.1 + 1..], false, precedence);
                (Expression::Sum(Box::new(upd.0), Box::new(rhs)), upd.1 + k_int + 1)
            }
            Token::Open => {
                let mut idx = None;
                let mut level = 1;
                for l in upd.1 + 1..tokens.len() {
                    level = match tokens[l] {
                        Token::Open => level + 1,
                        Token::Close if level > 1 => level - 1,
                        Token::Close => {
                            idx = Some(l);
                            break;
                        }
                        _ => { continue; }
                    };
                }
                let idx = idx.expect("No matching bracket");
                let (rhs, k_int) = to_expression(
                    &tokens[upd.1 + 1..idx], true, precedence);
                (rhs, upd.1 + k_int + 2)
            }
            Token::Close => panic!("What should I do here?"),
        };
        if !greedy { break; }
    }

    upd
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
