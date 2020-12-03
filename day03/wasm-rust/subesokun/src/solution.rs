//tag::star1[]
struct Map {
    map: std::vec::Vec<std::vec::Vec<bool>>,
    fragment_width: usize,
    height: usize
}

impl Map {
    pub fn get(&self, x: usize, y: usize) -> bool {
        return self.map[y % self.height][x % self.fragment_width]
    }
}

fn generate_map(puzzle_input: std::vec::Vec<String>) -> Map {
    let height = puzzle_input.len();
    let mut iter = puzzle_input.iter().peekable();
    let fragment_width = iter.peek().unwrap().len();
    let mut map = vec![vec![false; fragment_width]; height]; // true means empty
    for (pos_y, line) in iter.enumerate() {
        for (pos_x, grid_value) in line.chars().enumerate() {
            if grid_value == '#' {
                map[pos_y][pos_x] = true;
            }
        }
    }
    return Map {
        map: map,
        fragment_width: fragment_width,
        height: height
    }
}

fn count_encountered_trees(step_x: usize, step_y: usize, map: &Map) -> u32 {
    let mut pos_x = 0;
    let mut pos_y = 0;
    let mut encountered_trees = 0;
    let map_height = map.height;
    while pos_y < map_height {
        if map.get(pos_x, pos_y) {
            encountered_trees += 1;
        }
        pos_x += step_x;
        pos_y += step_y;
    }
    return encountered_trees;
}

pub fn run_star1(puzzle_input: std::vec::Vec<String>) -> u32 {
    let map = generate_map(puzzle_input);
    let solution: u32 = count_encountered_trees(3, 1, &map);
    return solution;
}
//end::star1[]

//tag::star2[]
pub fn run_star2(puzzle_input: std::vec::Vec<String>) -> u32 {
    let map = generate_map(puzzle_input);
    let mut solution = 1;
    solution *= count_encountered_trees(1, 1, &map);
    solution *= count_encountered_trees(3, 1, &map);
    solution *= count_encountered_trees(5, 1, &map);
    solution *= count_encountered_trees(7, 1, &map);
    solution *= count_encountered_trees(1, 2, &map);
    return solution;
}
//end::star2[]
