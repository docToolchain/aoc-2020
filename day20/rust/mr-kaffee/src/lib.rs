pub const MONSTER: &str = r"                  _ \    /\    /\    /o> \  /  \  /  \  /   ";
pub const MONSTER_WIDTH: usize = 20;

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
            if part.len() == 0 { continue; }

            let mut parts = part.split(":\n");

            let id = parts.next().expect("No ID part")[5..]
                .parse::<usize>()
                .expect("Could not parse ID");
            let data = parts.next().expect("No data part");

            let len = data.len();

            let data: Vec<_> = data.replace("\n", "").chars().collect();

            tiles.push(Tile { id, n: len - data.len() + 1, data });
        }

        tiles
    }

    // tag::get_set_transform[]
    fn transform(&self, idx: usize, t: usize) -> usize {
        // idx = x + n * y
        // x = idx % n
        // y = idx / n
        //
        // 0 identity:    (x, y) -> (      x,       y), idx =>       x + n * (        y)
        // 1 rot_90:      (x, y) -> (n-1 - y,       x), idx => n-1 - y + n * (        x)
        // 2 rot_180:     (x, y) -> (n-1 - x, n-1 - y), idx => n-1 - x + n * (n - 1 - y)
        // 3 rot_270:     (x, y) -> (      y, n-1 - x), idx =>       y + n * (n - 1 - x)
        // 4 flip         (x, y) -> (n-1 - x,       y), idx => n-1 - x + n * (        y)
        // 5 flip_rot_90  (x, y) -> (n-1 - y, n-1 - x), idx => n-1 - y + n * (n - 1 - x)
        // 6 flip_rot_180 (x, y) -> (      x, n-1 - y), idx =>       x + n * (n - 1 - y)
        // 7 flip_rot_270 (x, y) -> (      y,       x), idx =>       y + n * (        x)

        match t {
            0 => idx,
            1 => self.n - 1 - idx / self.n + self.n * (idx % self.n),
            2 => self.n - 1 - idx % self.n + self.n * (self.n - 1 - idx / self.n),
            3 => idx / self.n + self.n * (self.n - 1 - idx % self.n),
            4 => self.n - 1 - idx % self.n + self.n * (idx / self.n),
            5 => self.n - 1 - idx / self.n + self.n * (self.n - 1 - idx % self.n),
            6 => idx % self.n + self.n * (self.n - 1 - idx / self.n),
            7 => idx / self.n + self.n * (idx % self.n),
            _ => panic!("Illegal transformation"),
        }
    }

    fn get(&self, idx: usize, t: usize) -> char {
        self.data[self.transform(idx, t)]
    }

    fn set(&mut self, idx: usize, t: usize, c: char) {
        let idx = self.transform(idx, t);
        self.data[idx] = c;
    }
    // end::get_set_transform[]

    pub fn print(&self, t: usize) {
        for col in 0..self.n {
            for row in 0..self.n {
                print!("{}", self.get(row + self.n * col, t));
            }
            println!();
        }
    }

    // tag::match[]
    pub fn matches(&self, other: &Self, t: usize, side: usize) -> Option<usize> {
        if self.n != other.n {
            return None;
        }

        let (f1, f2) = match side {
            0 => ((0, 1), (self.n * (self.n - 1), 1)),
            1 => ((self.n - 1, self.n), (0, self.n)),
            2 => ((self.n * (self.n - 1), 1), (0, 1)),
            3 => ((0, self.n), (self.n - 1, self.n)),
            _ => panic!("Illegal side"),
        };

        (0..8).find(|t_other| (0..self.n).all(|k|
            self.get(f1.0 + f1.1 * k, t) == other.get(f2.0 + f2.1 * k, *t_other)))
    }
    // end::match[]

    // tag::find_pattern[]
    pub fn find_pattern(&self, t: usize, pattern: &[char], width: usize, idx0: usize)
                        -> Option<usize>
    {
        let w_pat = width;
        let h_pat = pattern.len() / w_pat;
        let n_tile = self.n;

        let mut idx_tile_start = idx0;
        loop {
            if idx_tile_start / n_tile + h_pat > n_tile {
                // pattern height does not fit, give up
                break;
            }
            if idx_tile_start % n_tile + w_pat > n_tile {
                // pattern width does not fit, go to next row
                idx_tile_start = n_tile * (idx_tile_start / n_tile + 1);
                continue;
            }

            let mut found = true;
            for idx_pat in 0..h_pat * w_pat {
                if pattern[idx_pat] == ' ' {
                    // if pattern character is blank, ignore character in picture
                    continue;
                }

                // determine idx in tile
                let x_pat = idx_pat % w_pat;
                let y_pat = idx_pat / w_pat;
                let idx_tile = idx_tile_start + x_pat + y_pat * n_tile;

                // apply transformation
                if self.get(idx_tile, t) != '#' {
                    // no '#' => not found
                    found = false;
                    break;
                }
            }

            // still found after all checks => match
            if found {
                return Some(idx_tile_start);
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
    let (pos, neighbors) = tiles.iter().enumerate().map(|(pos1, tile1)| {
        (pos1, (0..4).map(|side| {
            let found = tiles.iter().enumerate()
                .filter(|(pos2, _)| *pos2 != pos1)
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

    (pos, t)
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
    solution.push((tiles.remove(top_left), t));

    // top row
    for k in 1..width {
        // move on to the right => side = 1
        let (tile1, t) = &solution[k - 1];
        let (pos, t) = tiles.iter().enumerate().map(|(pos, tile2)|
            (pos, tile1.matches(tile2, *t, 1)))
            .filter_map(|(pos, t)| t.map(|t| (pos, t))).next().unwrap();
        solution.push((tiles.remove(pos), t));
    }

    for y in 1..width {
        // first element in row, move down from previous row => side = 2
        let (tile1, t) = &solution[width * (y - 1)];
        let (pos, t) = tiles.iter().enumerate().map(|(pos, tile2)|
            (pos, tile1.matches(tile2, *t, 2)))
            .filter_map(|(pos, t)| t.map(|t| (pos, t))).next().unwrap();
        solution.push((tiles.remove(pos), t));

        for x in 1..width {
            // find tiles which match to the left and to the top
            let idx = x + width * y;
            let (tile_up, t_up) = &solution[idx - width];
            let (tile_left, t_left) = &solution[idx - 1];
            let (pos, t) =
                tiles.iter().enumerate().map(|(pos, tile2)| (
                    pos,
                    tile_up.matches(tile2, *t_up, 2),
                    tile_left.matches(tile2, *t_left, 1)
                ))
                    .filter(|(_, t_up, t_left)| t_up == t_left)
                    .filter_map(|(pos, t, _)| t.map(|t| (pos, t)))
                    .next().unwrap();
            solution.push((tiles.remove(pos), t))
        }
    }

    (width, solution)
}
// end::solve[]

// tag::get_picture[]
pub fn get_picture(width: usize, solution: &[(Tile, usize)]) -> Tile {
    let width = width;
    let n = solution[1].0.n;
    let w = width * (n - 2);
    let mut picture = Vec::with_capacity(w * w);
    for _ in 0..w * w { picture.push('.') };

    for row in 0..width {
        for col in 0..width {
            for y_tile in 1..n - 1 {
                for x_tile in 1..n - 1 {
                    let y = row * (n - 2) + y_tile - 1;
                    let x = col * (n - 2) + x_tile - 1;
                    let (tile, t) = &solution[col + width * row];
                    picture[x + w * y] = tile.get(x_tile + n * y_tile, *t);
                }
            }
        }
    }

    Tile { id: 0, n: w, data: picture }
}
// end::get_picture[]

pub fn find_monsters(picture: &Tile, monster: &str, width: usize) -> (Vec<usize>, usize) {
    let monster: Vec<_> = monster.chars().collect();

    let mut monsters = Vec::new();

    for t in 0..8 {
        let mut idx_start = 0;
        while let Some(idx) = picture.find_pattern(
            t, &monster, width, idx_start,
        ) {
            monsters.push(idx);
            idx_start = idx + 1;
        }

        if monsters.len() > 0 { return (monsters, t); }
    }

    (monsters, 0)
}

// tag::get_roughness[]
pub fn get_roughness(picture: &Tile, monsters: usize) -> usize {
    let a = MONSTER.chars().filter(|c| *c != ' ').count();
    let b = picture.data.iter().filter(|c| **c == '#').count();
    b - monsters * a
}
// end::get_roughness[]

pub fn substitute_monsters(
    picture: &Tile, t: usize, monsters: &[usize], monster: &str, width: usize) -> Tile
{
    let mut picture = picture.clone();
    let monster: Vec<_> = monster.chars().collect();

    for idx in monsters {
        for y in 0..monster.len() / width {
            for x in 0..width {
                if monster[x + width * y] != ' ' {
                    picture.set(idx + x + picture.n * y, t, monster[x + width * y]);
                }
            }
        }
    }

    picture
}

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
        let (monsters, _) = find_monsters(&picture, MONSTER, MONSTER_WIDTH);
        assert_eq!(monsters.len(), 2);
        assert_eq!(get_roughness(&picture, monsters.len()), 273);
    }

    #[test]
    fn test_substitute_monsters() {
        let tiles = Tile::parse(CONTENT);
        let (width, solution) = solve(&tiles);
        let picture = get_picture(width, &solution);
        let (monsters, t) = find_monsters(&picture, MONSTER, MONSTER_WIDTH);
        let picture = substitute_monsters(&picture, t, &monsters, MONSTER, MONSTER_WIDTH);
        assert_eq!(picture.data.iter().filter(|c| **c == '#').count(), 273);
    }
}
