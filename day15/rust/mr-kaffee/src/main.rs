use mr_kaffee_2020_15::*;
use std::time::Instant;

fn main() {
    let instant_main = Instant::now();

    let content = "0,6,1,7,2,19,20";

    let (mut map,  last) = init(content);
    let start = map.len() as isize + 1;

    // solve part 1
    let instant_part = Instant::now();
    let last = play(&mut map, last, start, 2020);
    println!("Solution part 1 done in {:?}: {}", instant_part.elapsed(), last);
    assert_eq!(last, 706);

    // solve part 2
    let instant_part = Instant::now();
    let last = play(&mut map, last, 2020, 30_000_000);
    println!("Solution part 2 done in {:?}: {}", instant_part.elapsed(), last);
    assert_eq!(last, 19_331);

    println!("Total time: {:?}", instant_main.elapsed());
}
