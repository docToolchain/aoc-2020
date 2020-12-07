//tag::star1[]
fn calculate_seat_ids(seat_code_list: std::vec::Vec<String>) -> std::vec::Vec<u32> {
    let mut seat_ids: std::vec::Vec<u32> = Vec::new();
    for seat_code in seat_code_list.iter() {
        let mut min_row: u32 = 0;
        let mut max_row: u32 = 127;
        let mut min_column: u32 = 0;
        let mut max_column: u32 = 7;
        for code_char in seat_code.chars() {
            if code_char == 'F' {
                max_row = min_row + ((max_row - min_row + 1) / 2) - 1;
            } else if code_char == 'B' {
                min_row = min_row + (max_row - min_row + 1) / 2;
            } else if code_char == 'L' {
                max_column = min_column + ((max_column - min_column + 1) / 2) - 1;
            } else if code_char == 'R' {
                min_column = min_column + (max_column - min_column + 1) / 2;
            } 
        }
        seat_ids.push(min_row * 8 + min_column);
    }
    return seat_ids;
}

pub fn run_star1(puzzle_input: std::vec::Vec<String>) -> u32 {
    let seat_ids = calculate_seat_ids(puzzle_input);
    let solution = seat_ids.into_iter().max().unwrap();
    return solution;
}
//end::star1[]

//tag::star2[]
fn find_free_seat_id(mut seat_ids: std::vec::Vec<u32>) -> u32 {
    seat_ids.sort();
    let vlen = seat_ids.len();
    let iter = seat_ids.clone().into_iter();
    let mut result: u32 = 0;
    for (index, seat_id) in iter.enumerate() {
        if (index > 0 && index < vlen - 1) && seat_ids[index - 1] + 1 != seat_id {
            result = seat_id - 1;
            break;
        }
    }
    return result;
}

pub fn run_star2(puzzle_input: std::vec::Vec<String>) -> u32 {
    let seat_ids = calculate_seat_ids(puzzle_input);
    let solution = find_free_seat_id(seat_ids);
    return solution;
}
//end::star2[]
