use mr_kaffee_2020_21::*;
use std::time::Instant;
use std::fs;

fn read_input() -> String {
    fs::read_to_string("input.txt")
        .expect("Could not read from file.")
}

fn main() {
    // start timer
    let instant_main = Instant::now();

    // read file
    let content = read_input();

    // parse
    let foods = parse(&content);

    // solve part 1
    let instant_part = Instant::now();
    let map = build_allergen_map(&foods);
    let sol = count_without_allergens(&foods, &map);
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 2_614);

    // solve part 2
    let instant_part = Instant::now();
    let map = reduce_allergen_map(map);
    let sol = assemble_list(&map);
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(&sol, "qhvz,kbcpn,fzsl,mjzrj,bmj,mksmf,gptv,kgkrhg");

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
