// Looks ugly 🙈
fn fix_expense_report_two(target_sum: u32, report: std::vec::Vec<u32>) -> u32 {
    let mut inner_report = report.clone();
    for e in report.iter() {
        println!("e: {}", e);
        inner_report.remove(0);
        for inner_e in inner_report.iter() {
            println!("inner_e: {} {}", inner_e, e + inner_e);
            if e + inner_e == target_sum {
                return e * inner_e;
            }
        }
    }
    return 0;
}

// Looks extra ugly 🙈
fn fix_expense_report_three(target_sum: u32, report: std::vec::Vec<u32>) -> u32 {
    let mut inner_report = report.clone();
    for e in report.iter() {
        inner_report.remove(0);
        let mut inner_inner_report = inner_report.clone();
        for inner_e in inner_report.iter() {
            inner_inner_report.remove(0);
            for inner_inner_e in inner_inner_report.iter() {
                if e + inner_e + inner_inner_e == target_sum {
                    return e * inner_e * inner_inner_e;
                }
            }
        }
    }
    return 0;
}

pub fn run_star1(puzzle_input: std::vec::Vec<u32>) -> u32 {
    let solution: u32 = fix_expense_report_two(2020, puzzle_input);
    return solution;
}

pub fn run_star2(puzzle_input: std::vec::Vec<u32>) -> u32 {
    let solution: u32 = fix_expense_report_three(2020, puzzle_input);
    return solution;
}
