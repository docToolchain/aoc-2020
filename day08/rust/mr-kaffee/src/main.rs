use regex::Regex;
use std::collections::BTreeSet;
use std::fs;

fn main() {
    let content = fs::read_to_string("input.txt")
        .expect("Could not read file.");

    let program = Instruction::parse(&content);

    let (_, acc) = run(&program);
    println!("Accumulator is {} before program repeats.", acc);
    assert_eq!(acc, 1179);

    let (_, acc) = find(&program);
    println!("Fixed program yields {}.", acc);
    assert_eq!(acc, 1089);
}

// tag::find[]
fn find(program: &[Instruction]) -> (usize, i32) {
    let len = program.len();
    let mut modified = Vec::from(program);
    for i in 0..len {
        modified[i] = match program[i] {
            Instruction::NOp(val) => Instruction::Jmp(val),
            Instruction::Jmp(val) => Instruction::NOp(val),
            _ => { continue; }
        };

        let (pos, acc) = run(&modified);
        if pos >= len {
            println!("Changed {:?} to {:?} at {}", program[i], modified[i], i);
            return (pos, acc);
        }
        modified[i] = program[i];
    };

    panic!("Nothing found.");
}
// end::find[]

// tag::run[]
fn run(program: &[Instruction]) -> (usize, i32) {
    let mut pos = 0;
    let mut acc = 0;

    let mut seen = BTreeSet::new();
    seen.insert(0);

    while pos < program.len() {
        let (pos_upd, acc_upd) = match &program[pos as usize] {
            Instruction::NOp(_) => (pos + 1, acc),
            Instruction::Acc(inc) => (pos +1, acc + inc),
            Instruction::Jmp(jmp) => ((pos as i32 + jmp) as usize, acc),
        };
        pos = pos_upd;
        acc = acc_upd;

        // infinite loop detector
        if !seen.insert(pos) {
            break;
        }
    }

    (pos, acc)
}
// end::run[]

// tag::instruction[]
#[derive(Debug, PartialEq, Clone, Copy)]
enum Instruction {
    NOp(i32),
    Acc(i32),
    Jmp(i32),
}
// end::instruction[]

impl Instruction {
    fn parse(content: &str) -> Vec<Instruction> {
        let re = Regex::new(r"(nop|acc|jmp) \+?(-?\d+)\s*")
            .expect("Invalid regular expression");

        re.captures_iter(content).map(|cap| {
            let val: i32 = cap[2].parse().expect("Could not parse number");
            match &cap[1] {
                "nop" => Instruction::NOp(val),
                "acc" => Instruction::Acc(val),
                "jmp" => Instruction::Jmp(val),
                other => panic!(format!("Illegal instruction: {}", other)),
            }
        }).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6";

    fn instructions() -> Vec<Instruction> {
        vec![
            Instruction::NOp(0), Instruction::Acc(1), Instruction::Jmp(4),
            Instruction::Acc(3), Instruction::Jmp(-3), Instruction::Acc(-99),
            Instruction::Acc(1), Instruction::Jmp(-4), Instruction::Acc(6)
        ]
    }

    #[test]
    fn test_instruction_parse() {
        assert_eq!(Instruction::parse(CONTENT), instructions());
    }

    #[test]
    fn test_run() {
        let mut instructions = instructions();
        let len = instructions.len();
        let (pos, acc) = run(&instructions);
        assert!(pos < len);
        assert_eq!(acc, 5);

        instructions[len - 2] = Instruction::NOp(0);
        let (pos, acc) = run(&instructions);
        assert_eq!(pos, len);
        assert_eq!(acc, 8);
    }

    #[test]
    fn test_find() {
        let instructions = instructions();
        let (pos, acc) = find(&instructions);
        assert_eq!(pos, instructions.len());
        assert_eq!(acc, 8);
    }
}