use regex::Regex;
use std::collections::HashSet;
use std::cmp::{max, min};

// tag::get_coords[]
pub fn get_coords(content: &str) -> Vec<(i32, i32)> {
    let re = Regex::new(r"(e)|(se)|(sw)|(w)|(nw)|(ne)")
        .expect("Illegal regex");

    content.lines().map(|line|
        re.find_iter(line).fold((0, 0), |(x, y), m|
            match m.as_str() {
                "e" => (x + 2, y),
                "se" => (x + 1, y + 1),
                "sw" => (x - 1, y + 1),
                "w" => (x - 2, y),
                "nw" => (x - 1, y - 1),
                "ne" => (x + 1, y - 1),
                _ => panic!("Illegal direction: {:?}", m),
            },
        )).collect()
}
// end::get_coords[]

// tag::flip_tiles[]
pub fn flip_tiles(coords: &[(i32, i32)]) -> HashSet<(i32, i32)> {
    let mut blacks = HashSet::new();
    coords.iter().for_each(|value| if !blacks.remove(value) { blacks.insert(*value); });
    blacks
}
// end::flip_tiles[]

// tag::update_step[]
pub fn update_step(blacks: &HashSet<(i32, i32)>) -> HashSet<(i32, i32)> {
    // determine bounds
    let (min_x, max_x, min_y, max_y) = blacks.iter()
        .fold((i32::MAX, i32::MIN, i32::MAX, i32::MIN),
              |(min_x, max_x, min_y, max_y), (x, y)|
                  (min(min_x, *x), max(max_x, *x + 1),
                   min(min_y, *y), max(max_y, *y + 1)));

    // closure to check whether tile at coordinate is black
    // check whether it is in range first
    let is_black = |(x, y)| x >= min_x && x < max_x && y >= min_y && y < max_x &&
        blacks.contains(&(x, y));

    // valid coordinates: even row -> even column, odd row -> odd column
    // in even rows, start from largest even x which is less than min_x
    // in odd rows, start from largest odd xx which is less then min_x
    let d = if min_x & 1 == 0 { [-2, -1] } else { [-1, -2] };

    let mut blacks_upd = HashSet::new();

    // search directions
    let dlts = [(2, 0), (1, 1), (1, -1), (-2, 0), (-1, -1), (-1, 1)];

    for y in min_y - 1..max_y + 1 {
        for x in (min_x + d[(y & 1) as usize]..max_x + 1).step_by(2) {
            // is currently black
            let black = is_black((x, y));

            // count black adjacents
            let cnt = dlts.iter()
                .filter(|&(dx, dy)| is_black((x + dx, y + dy)))
                .count();

            // apply update rules
            if black && cnt > 0 && cnt <= 2 {
                blacks_upd.insert((x, y));
            } else if !black && cnt == 2 {
                blacks_upd.insert((x, y));
            }
        }
    }

    blacks_upd
}
// end::update_step[]

pub fn update(blacks: &HashSet<(i32, i32)>, rounds: usize) -> HashSet<(i32, i32)> {
    let mut blacks_upd = blacks.clone();
    for _ in 0..rounds {
        blacks_upd = update_step(&blacks_upd);
    }
    blacks_upd
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew";

    #[test]
    fn test_get_coords() {
        let coords = get_coords("esew");
        assert_eq!(coords, vec![(1, 1)]);

        let coords = get_coords("nwwswee");
        assert_eq!(coords, vec![(0, 0)]);
    }

    #[test]
    fn test_flip_tiles() {
        let blacks = flip_tiles(&get_coords(CONTENT));
        assert_eq!(blacks.len(), 10);
    }

    #[test]
    fn test_update_step() {
        let mut blacks = flip_tiles(&get_coords(CONTENT));
        let exp = vec![15, 12, 25, 14, 23, 28, 41, 37, 49, 37];
        for k in 0..exp.len() {
            blacks = update_step(&blacks);
            assert_eq!(blacks.len(), exp[k], "Mismatch at {}", k);
        }
    }

    #[test]
    fn test_update() {
        let mut blacks = flip_tiles(&get_coords(CONTENT));
        blacks = update(&blacks, 100);
        assert_eq!(blacks.len(), 2208);
    }
}
