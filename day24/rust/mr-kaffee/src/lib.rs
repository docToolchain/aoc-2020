use regex::Regex;
use std::collections::HashSet;
use std::cmp::{max, min};

// search directions
const DLTS: [(i32, i32); 6] = [(2, 0), (1, 1), (1, -1), (-2, 0), (-1, -1), (-1, 1)];

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

    // closure to check whether tile at coordinate is black, pre-check range
    let is_black = |(x, y)| (min_x..max_x).contains(&x)
        && (min_y..max_y).contains(&y) && blacks.contains(&(x, y));

    // even row: lowest even x >= min_x - 1; odd row: lowest odd x >= min_x - 1
    let off_min_x = if min_x & 1 == 0 { [0, 1] } else { [1, 0] };

    let mut blacks_upd = HashSet::new();

    for y in min_y - 1..max_y + 1 {
        for x in (min_x - off_min_x[(y & 1) as usize]..max_x + 1).step_by(2) {
            // is currently black
            let black = is_black((x, y));

            // count black adjacents; if 3 found stop counting
            let cnt = DLTS.iter()
                .filter(|&(dx, dy)| is_black((x + dx, y + dy))).take(3).count();

            // apply update rules
            if (black && cnt == 1) || cnt == 2 { blacks_upd.insert((x, y)); }
        }
    }

    blacks_upd
}
// end::update_step[]

pub fn update(blacks: &HashSet<(i32, i32)>, rounds: usize) -> HashSet<(i32, i32)> {
    (0..rounds).fold(blacks.clone(), |blacks, _| update_step(&blacks))
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
