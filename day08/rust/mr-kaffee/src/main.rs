use regex::Regex;
use std::collections::BTreeSet;
use std::fs;
use std::mem;

fn main() {
    let content = fs::read_to_string("input.txt")
        .expect("Could not read file.");

    let mut program = Instr::parse(&content);

    let (_, acc) = run(&program);
    println!("Accumulator is {} before program repeats.", acc);
    assert_eq!(acc, 1179);

    let (_, acc) = fix(&mut program);
    println!("Fixed program yields {}.", acc);
    assert_eq!(acc, 1089);
}

fn swap(program: &mut [Instr], i: usize) -> Option<Instr> {
    match program[i] {
        Instr::NOp(val) => Some(mem::replace(&mut program[i], Instr::Jmp(val))),
        Instr::Jmp(val) => Some(mem::replace(&mut program[i], Instr::NOp(val))),
        Instr::Acc(_) => None,
    }
}

// tag::fix[]
fn fix(program: &mut Vec<Instr>) -> (usize, i32) {
    for i in 0..program.len() {
        // if swap, evaluate variant
        if let Some(old) = swap(program, i) {
            // run program and return if it terminates
            let (pos, acc) = run(&program);
            if pos >= program.len() {
                println!("Changed {:?} to {:?} at {}", old, program[i], i);
                return (pos, acc);
            }

            // revert
            program[i] = old;
        };
    };

    panic!("Nothing found.");
}
// end::fix[]

// tag::run[]
fn run(program: &[Instr]) -> (usize, i32) {
    let mut pos = 0;
    let mut acc = 0;

    let mut seen = BTreeSet::new();
    seen.insert(0);

    while pos < program.len() {
        let (pos_upd, acc_upd) = match &program[pos as usize] {
            Instr::NOp(_) => (pos + 1, acc),
            Instr::Acc(inc) => (pos + 1, acc + inc),
            Instr::Jmp(jmp) => ((pos as i32 + jmp) as usize, acc),
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
enum Instr {
    NOp(i32),
    Acc(i32),
    Jmp(i32),
}
// end::instruction[]

impl Instr {
    fn parse(content: &str) -> Vec<Instr> {
        let re = Regex::new(r"(nop|acc|jmp) \+?(-?\d+)\s*")
            .expect("Invalid regular expression");

        re.captures_iter(content).map(|cap| {
            let val: i32 = cap[2].parse().expect("Could not parse number");
            match &cap[1] {
                "nop" => Instr::NOp(val),
                "acc" => Instr::Acc(val),
                "jmp" => Instr::Jmp(val),
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

    fn instructions() -> Vec<Instr> {
        vec![
            Instr::NOp(0), Instr::Acc(1), Instr::Jmp(4),
            Instr::Acc(3), Instr::Jmp(-3), Instr::Acc(-99),
            Instr::Acc(1), Instr::Jmp(-4), Instr::Acc(6)
        ]
    }

    #[test]
    fn test_instruction_parse() {
        assert_eq!(Instr::parse(CONTENT), instructions());
    }

    #[test]
    fn test_run() {
        let mut program = instructions();

        // run original program, should not terminate
        let (pos, acc) = run(&program);
        assert!(pos < program.len());
        assert_eq!(acc, 5);

        // swap Jmp(-4) to NOp(-4) at i = 7
        let option_old = swap(&mut program, 7);
        assert_eq!(option_old, Some(Instr::Jmp(-4)));

        // run modified program, should terminate
        let (pos, acc) = run(&program);
        assert_eq!(pos, program.len());
        assert_eq!(acc, 8);
    }

    #[test]
    fn test_fix() {
        let mut program = instructions();

        // fix program and get result
        let (pos, acc) = fix(&mut program);
        assert_eq!(pos, program.len());
        assert_eq!(acc, 8);

        // re-run fixed program should reprocude results
        let (pos, acc) = run(&program);
        assert_eq!(pos, program.len());
        assert_eq!(acc, 8);
    }
}