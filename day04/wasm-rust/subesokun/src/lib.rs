mod utils;
mod solution;

use wasm_bindgen::prelude::*;


// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

fn read_puzzle_input(content: String) -> std::vec::Vec<String> {
    let mut vec = Vec::new();
    for line in content.lines() {
        let line_value: String = line.parse().unwrap();
        vec.push(line_value);
    }
    return vec
}

#[wasm_bindgen]
pub fn run_solution_star1(input_txt_string: String) -> u32 {
    return solution::run_star1(read_puzzle_input(input_txt_string));
}

#[wasm_bindgen]
pub fn run_solution_star2(input_txt_string: String) -> u32 {
    return solution::run_star2(read_puzzle_input(input_txt_string));
}
