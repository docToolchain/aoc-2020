fn extract_map(puzzle_input: std::vec::Vec<String>, step_with: usize) -> std::vec::Vec<std::vec::Vec<bool>> {
    let mut iter = puzzle_input.iter().peekable();
    let map_height = puzzle_input.len();
    let map_fragment_width = iter.peek().unwrap().len();
    let min_map_width = map_height * step_with + 1;
    let map_fragment_repeat_count = (min_map_width as f64 / map_fragment_width as f64).ceil() as usize;
    let map_width = map_fragment_repeat_count * map_fragment_width;
    let mut map = vec![vec![false; map_width]; map_height]; // true means empty
    for (pos_y, line) in iter.enumerate() {
        for (pos_x, grid_value) in line.chars().enumerate() {
            if grid_value == '#' {
                for repeat_index in 0..map_fragment_repeat_count {
                    map[pos_y][pos_x + repeat_index * map_fragment_width] = true;
                }
            }
        }

    }
    return map;
}

//tag::star1[]
fn count_encountered_trees(step_x: usize, step_y: usize, map: &std::vec::Vec<std::vec::Vec<bool>>) -> u32 {
    let mut pos_x = 0;
    let mut pos_y = 0;
    let mut encountered_trees = 0;
    let map_height = map.len();
    while pos_y < map_height {
        if map[pos_y][pos_x] {
            encountered_trees += 1;
        }
        pos_x += step_x;
        pos_y += step_y;
    }
    return encountered_trees;
}

pub fn run_star1(puzzle_input: std::vec::Vec<String>) -> u32 {
    let map = extract_map(puzzle_input, 3);
    let solution: u32 = count_encountered_trees(3, 1, &map);
    return solution;
}
//end::star1[]

//tag::star2[]
pub fn run_star2(puzzle_input: std::vec::Vec<String>) -> u32 {
    let map = extract_map(puzzle_input, 7);
    let mut solution = 1;
    solution *= count_encountered_trees(1, 1, &map);
    solution *= count_encountered_trees(3, 1, &map);
    solution *= count_encountered_trees(5, 1, &map);
    solution *= count_encountered_trees(7, 1, &map);
    solution *= count_encountered_trees(1, 2, &map);
    return solution;
}
//end::star2[]
