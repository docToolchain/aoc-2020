const MONSTER: &str = "                  # #    ##    ##    ### #  #  #  #  #  #   ";
const MONSTER_WIDTH: usize = 20;

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct Tile {
    id: usize,
    n: usize,
    data: Vec<char>,
}

impl Tile {
    pub fn parse(input: &str) -> Vec<Tile> {
        let mut tiles = Vec::new();

        let tile_parts = input.split("\n\n");
        for part in tile_parts {
            if part.len() == 0 {
                continue;
            }
            let mut parts = part.split(":\n");
            let id = parts.next().expect("No ID part")[5..]
                .parse::<usize>()
                .expect("Could not parse ID");
            let data = parts.next().expect("No data part");
            let len0 = data.len();
            let data: Vec<_> = data.replace("\n", "").chars().collect();
            let n = len0 - data.len() + 1;
            tiles.push(Tile { id, n, data });
        }

        tiles
    }

    // tag::get[]
    fn get(&self, idx: isize, t: usize) -> char {
        // idx = x + n * y
        // x = idx % n
        // y = idx / n
        //
        // 0 identity:    (x, y) -> (      x,       y), idx =>       x + n * (        y)
        // 1 rot_90:      (x, y) -> (n-1 - y,       x), idx => n-1 - y + n * (        x)
        // 2 rot_180:     (x, y) -> (n-1 - x, n-1 - y), idx => n-1 - x + n * (n - 1 - y)
        // 3 rot_270:     (x, y) -> (      y, n-1 - x), idx =>       y + n * (n - 1 - x)
        // 4 flip         (x, y) -> (n-1 - x,       y), idx => n-1 - x + n * (        Y)
        // 5 flop_rot_90  (x, y) -> (n-1 - y, n-1 - x), idx => n-1 - y + n * (n - 1 - x)
        // 6 flip_rot_180 (x, y) -> (      x, n-1 - y), idx =>       x + n * (n - 1 - y)
        // 7 flip_rot_270 (x, y) -> (      y,       x), idx =>       y + n * (        x)

        let n = self.n as isize;

        let idx = match t {
            0 => idx,
            1 => n - 1 - idx / n + n * (idx % n),
            2 => n - 1 - idx % n + n * (n - 1 - idx / n),
            3 => idx / n + n * (n - 1 - idx % n),
            4 => n - 1 - idx % n + n * (idx / n),
            5 => n - 1 - idx / n + n * (n - 1 - idx % n),
            6 => idx % n + n * (n - 1 - idx / n),
            7 => idx / n + n * (idx % n),
            _ => panic!("Illegal transformation"),
        };

        self.data[idx as usize]
    }
    // end::get[]

    // tag::match[]
    pub fn matches(&self, other: &Self, t: usize, side: usize) -> Option<usize> {
        if self.n != other.n {
            return None;
        }

        let n = self.n as isize;

        let (f1, f2) = match side {
            0 => ((0, 1), (n * (n - 1), 1)),
            1 => ((n - 1, n), (0, n)),
            2 => ((n * (n - 1), 1), (0, 1)),
            3 => ((0, n), (n - 1, n)),
            _ => panic!("Illegal side"),
        };

        (0..8).find(|t_other| (0..n).all(|k|
            self.get(f1.0 + f1.1 * k, t) == other.get(f2.0 + f2.1 * k, *t_other)))
    }
    // end::match[]

    // tag::find_pattern[]
    pub fn find_pattern(&self, t: usize, pattern: &[char], width: usize, idx0: usize)
                        -> Option<usize>
    {
        let w_pat = width as isize;
        let h_pat = pattern.len() as isize / w_pat;
        let w_tile = self.n as isize;

        let mut idx_tile_start = idx0 as isize;
        while idx_tile_start < w_tile * w_tile {
            if idx_tile_start / w_tile + h_pat > w_tile {
                // pattern height does not fit, give up
                break;
            }
            if idx_tile_start % w_tile + w_pat > w_tile {
                // pattern width does not fit, go to next row
                idx_tile_start = w_tile * (idx_tile_start / w_tile + 1);
                continue;
            }

            let mut found = true;
            for idx_pat in 0..h_pat * w_pat {
                if pattern[idx_pat as usize] == ' ' {
                    // if pattern character is blank, ignore character in picture
                    continue;
                }

                // determine idx in tile
                let x_pat = idx_pat % w_pat;
                let y_pat = idx_pat / w_pat;
                let idx_tile = idx_tile_start + x_pat + y_pat * w_tile;

                // apply transformation
                if self.get(idx_tile, t) != '#' {
                    // no '#' => not found
                    found = false;
                    break;
                }
            }

            // still found after all checks => match
            if found {
                return Some(idx_tile_start as usize);
            }

            // search in next position
            idx_tile_start += 1;
        }

        // nothing found
        None
    }
}
// end::find_pattern[]

// tag::find_corner[]
pub fn find_corner(tiles: &[Tile]) -> (usize, usize) {
    let (tile_id, neighbors) = tiles.iter().enumerate().map(|(k, tile1)| {
        (k, (0..4).map(|side| {
            let found = tiles.iter()
                .enumerate()
                .filter(|(j, _)| *j != k)
                .any(|(_, tile2)| tile1.matches(tile2, 0, side).is_some());
            (found as usize) << side
        }).sum::<usize>())
    }).find(|(_, dirs)| dirs.count_ones() == 2).unwrap();

    let t = match neighbors {
        0b0011 => 3,
        0b0110 => 0,
        0b1100 => 1,
        0b1001 => 2,
        _ => panic!("Illegal unmatched boundary combination"),
    };

    (tile_id, t)
}
// end::find_corner[]

pub fn corners_checksum(width: usize, solution: &[(Tile, usize)]) -> usize {
    let mut checksum = solution[0].0.id;
    checksum *= solution[width - 1].0.id;
    checksum *= solution[width * (width - 1)].0.id;
    checksum *= solution[width * width - 1].0.id;
    checksum
}

// tag::solve[]
pub fn solve(tiles: &[Tile]) -> (usize, Vec<(Tile, usize)>) {
    let mut tiles: Vec<_> = tiles.iter().map(|tile| tile.clone()).collect();

    // determine puzzle dimension
    let width = (0..tiles.len()).find(|width| {
        width * width == tiles.len()
    }).expect("No valid puzzle dimensions");

    let mut solution: Vec<(Tile, usize)> = Vec::with_capacity(width * width);

    // top left corner
    let (top_left, t) = find_corner(&tiles);
    let tile = tiles.remove(top_left);
    solution.push((tile, t));

    // top row
    for k in 1..width {
        // move on to the right => side = 1
        let (pos, t) = tiles.iter().enumerate().map(|(pos, tile2)| {
            let (tile1, t) = &solution[k - 1];
            (pos, tile1.matches(tile2, *t, 1))
        }).find(|(_, t)| t.is_some()).unwrap();
        let t = t.unwrap();
        let tile = tiles.remove(pos);
        solution.push((tile, t));
    }

    for y in 1..width {
        // first element in row, move down from previous row => side = 2
        let (pos, t) =
            tiles.iter().enumerate().map(|(pos, tile2)| {
                let (tile1, t) = &solution[width * (y - 1)];
                (pos, tile1.matches(tile2, *t, 2))
            }).find(|(_, t)| t.is_some()).unwrap();
        let t = t.unwrap();
        let tile = tiles.remove(pos);
        solution.push((tile, t));

        for x in 1..width {
            // find tiles which match to the left and to the top
            let idx = x + width * y;
            let up = idx - width;
            let left = idx - 1;
            let (pos, t, _) =
                tiles.iter().enumerate().map(|(pos, tile2)| {
                    let (tile_up, t_up) = &solution[up];
                    let (tile_left, t_left) = &solution[left];
                    (
                        pos,
                        tile_up.matches(tile2, *t_up, 2),
                        tile_left.matches(tile2, *t_left, 1)
                    )
                }).find(|(_, t_up, t_left)|
                    t_up.is_some() && t_left.is_some() &&
                        t_up.unwrap() == t_left.unwrap()).unwrap();
            let t = t.unwrap();
            let tile = tiles.remove(pos);
            solution.push((tile, t))
        }
    }

    (width, solution)
}
// end::solve[]

// tag::get_picture[]
pub fn get_picture(width: usize, solution: &[(Tile, usize)]) -> Tile {
    let width = width as isize;
    let n = solution[1].0.n as isize;
    let w = width * (n - 2);
    let mut picture = Vec::with_capacity((w * w) as usize);
    for _ in 0..w * w { picture.push('.') };

    for row in 0..width {
        for col in 0..width {
            for y_tile in 1..n - 1 {
                for x_tile in 1..n - 1 {
                    let y = row * (n - 2) + y_tile - 1;
                    let x = col * (n - 2) + x_tile - 1;
                    let (tile, t) = &solution[(col + width * row) as usize];
                    picture[(x + w * y) as usize] = tile.get(x_tile + n * y_tile, *t);
                }
            }
        }
    }

    Tile { id: 0, n: w as usize, data: picture }
}
// end::get_picture[]

pub fn find_monsters(picture: &Tile) -> (Vec<usize>, usize) {
    let monster: Vec<_> = MONSTER.chars().collect();

    let mut monsters = Vec::new();
    for t in 0..8 {
        let mut idx = 0;
        while let Some(i) = picture.find_pattern(
            t, &monster, MONSTER_WIDTH, idx,
        ) {
            monsters.push(i);
            idx = i + 1;
        }
        if monsters.len() > 0 {
            return (monsters, t);
        }
    }

    (monsters, 0)
}

// tag::get_roughness[]
pub fn get_roughness(picture: &Tile, monsters: usize) -> usize {
    let a = MONSTER.chars().filter(|c| *c == '#').count();
    let b = picture.data.iter().filter(|c| **c == '#').count();
    b - monsters * a
}
// end::get_roughness[]

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    const CONTENT: &str = "Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...";

    #[test]
    fn test_tile_parse() {
        let tiles = Tile::parse(CONTENT);
        assert_eq!(tiles.len(), 9);

        let ids: Vec<_> = tiles.iter().map(|tile| tile.id).collect();
        assert_eq!(ids, vec![2311, 1951, 1171, 1427, 1489, 2473, 2971, 2729, 3079]);


        assert!(tiles.iter().all(|tile| tile.n == 10));
    }

    #[test]
    fn test_matches() {
        let tiles = Tile::parse(CONTENT);
        let map: HashMap<_, _> = tiles.iter().map(|tile| (tile.id, tile)).collect();

        let tile_1951 = map.get(&1951).unwrap(); // top left, 6
        let tile_2311 = map.get(&2311).unwrap(); // top right, 6
        let tile_2729 = map.get(&2729).unwrap(); // bottom left, 6
        let tile_1427 = map.get(&1427).unwrap(); // bottom right, 6

        assert_eq!(tile_1951.matches(tile_2311, 6, 1), Some(6));
        assert_eq!(tile_1951.matches(tile_2729, 6, 2), Some(6));
        assert_eq!(tile_2729.matches(tile_1427, 6, 1), Some(6));
        assert_eq!(tile_2311.matches(tile_1427, 6, 2), Some(6));
    }

    #[test]
    fn test_corners_checksum() {
        let tiles = Tile::parse(CONTENT);
        let (width, solution) = solve(&tiles);
        assert_eq!(corners_checksum(width, &solution), 20_899_048_083_289);
    }

    #[test]
    fn test_get_picture() {
        let tiles = Tile::parse(CONTENT);
        let (width, solution) = solve(&tiles);
        let tile = get_picture(width, &solution);
        for y in 0..tile.n {
            for x in 0..tile.n {
                print!("{}", tile.data[x + tile.n * y]);
            }
            println!();
        }
    }

    #[test]
    fn test_tile_find_monsters() {
        let tiles = Tile::parse(CONTENT);
        let (width, solution) = solve(&tiles);
        let picture = get_picture(width, &solution);
        let (monsters, _) = find_monsters(&picture);
        assert_eq!(monsters.len(), 2);
        assert_eq!(get_roughness(&picture, monsters.len()), 273);
    }
}