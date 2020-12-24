use mr_kaffee_2020_23::*;
use std::time::Instant;

const DATA: [usize; 9] = [4, 8, 7, 9, 1, 2, 3, 6, 5];

fn main() {
    // start timer
    let instant_main = Instant::now();

    // solve part 1
    let instant_part = Instant::now();
    let (list, _, low) = play_rounds(&DATA, DATA.len(), 100);
    let sol = get_checksum_1(&list, low);
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 89_573_246);

    // solve part 2
    let instant_part = Instant::now();
    let (list, _, low) = play_rounds(&DATA, 1_000_000, 10_000_000);
    let sol = get_checksum_2(&list, low);
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), sol);
    assert_eq!(sol, 2_029_056_128);

    // print elapsed time
    println!("Total time: {:?}", instant_main.elapsed());
}
