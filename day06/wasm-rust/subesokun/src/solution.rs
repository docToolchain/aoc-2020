//tag::star1[]
fn count_anyone_answers_per_group(puzzle_input: String) -> u32 {
    let groups: Vec<String> = puzzle_input.replace("\n\n", " ").replace("\n", "").split(" ").map(|s| s.to_string()).collect();
    let mut result = 0;
    for group in groups.into_iter() {
        let mut chars: Vec<char> = group.chars().collect();
        chars.sort();
        chars.dedup();
        let group_answers: String = chars.into_iter().collect();
        result += group_answers.len();
    }
    return result as u32;
}

pub fn run_star1(puzzle_input: String) -> u32 {
    let soltuion = count_anyone_answers_per_group(puzzle_input);
    return soltuion;
}
//end::star1[]

//tag::star2[]

fn count_everyone_answers_per_group(puzzle_input: String) -> u32 {
    let groups: Vec<String> = puzzle_input.split("\n\n").map(|s| s.to_string()).collect();
    let mut result = 0;
    for group in groups.into_iter() {
        let group_size = group.matches("\n").count() + 1;
        let group_answer = group.replace("\n", "");
        let mut group_answer_chars: Vec<char> = group_answer.chars().collect();
        group_answer_chars.sort();
        group_answer_chars.dedup();
        for answer_type in group_answer_chars {
            let cnt_answers = group_answer.matches(answer_type).count();
            if cnt_answers == group_size {
                result += 1;
            }
        }
    }
    return result as u32;
}

pub fn run_star2(puzzle_input: String) -> u32 {
    let soltuion = count_everyone_answers_per_group(puzzle_input);
    return soltuion;
}
//end::star2[]
