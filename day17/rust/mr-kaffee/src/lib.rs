use std::collections::HashSet;
use std::cmp::{min, max};

#[derive(Debug, PartialEq)]
pub struct BBox3 {
    x_rg: (isize, isize),
    y_rg: (isize, isize),
    z_rg: (isize, isize),
}

impl Default for BBox3 {
    fn default() -> Self {
        BBox3 {
            x_rg: (isize::MAX, isize::MIN),
            y_rg: (isize::MAX, isize::MIN),
            z_rg: (isize::MAX, isize::MIN),
        }
    }
}

impl BBox3 {
    pub fn update(&mut self, x: isize, y: isize, z: isize) {
        self.x_rg = (min(self.x_rg.0, x), max(self.x_rg.1, x + 1));
        self.y_rg = (min(self.y_rg.0, y), max(self.y_rg.1, y + 1));
        self.z_rg = (min(self.z_rg.0, z), max(self.z_rg.1, z + 1));
    }
}

pub fn parse3(content: &str, z: isize) -> (HashSet<(isize, isize, isize)>, BBox3) {
    let mut map = HashSet::new();
    let mut bbox = BBox3::default();
    content.lines().enumerate().for_each(|(y, line)| {
        line.chars().enumerate().for_each(|(x, c)|
            {
                if c == '#' {
                    map.insert((x as isize, y as isize, z));
                    bbox.update(x as isize, y as isize, z);
                }
            }
        );
    });
    (map, bbox)
}

pub fn update_steps3(map: &HashSet<(isize, isize, isize)>, bbox: &BBox3, steps: isize)
                     -> (HashSet<(isize, isize, isize)>, BBox3) {
    assert!(steps > 0, "steps > 0 required");

    let (mut map, mut bbox) = update3(map, bbox);
    for _ in 1..steps {
        let (map_upd, bbox_upd) = update3(&map, &bbox);
        map = map_upd;
        bbox = bbox_upd;
    }
    (map, bbox)
}

pub fn update3(map: &HashSet<(isize, isize, isize)>, bbox: &BBox3)
               -> (HashSet<(isize, isize, isize)>, BBox3) {
    let mut map_upd = HashSet::new();
    let mut bbox_upd = BBox3::default();

    for x in bbox.x_rg.0 - 1..bbox.x_rg.1 + 1 {
        for y in bbox.y_rg.0 - 1..bbox.y_rg.1 + 1 {
            for z in bbox.z_rg.0 - 1..bbox.z_rg.1 + 1 {
                let mut cnt = 0;
                for k in 0..27 {
                    if k == 13 {
                        continue;
                    }
                    let dx = k % 3 - 1;
                    let dy = (k % 9) / 3 - 1;
                    let dz = k / 9 - 1;

                    if map.contains(&(x + dx, y + dy, z + dz)) {
                        cnt += 1;
                        if cnt > 3 {
                            break;
                        }
                    }
                }
                let active = map.contains(&(x, y, z));
                if (active && cnt >= 2 && cnt <= 3) || (!active && cnt == 3) {
                    map_upd.insert((x, y, z));
                    bbox_upd.update(x, y, z);
                }
            }
        }
    };

    (map_upd, bbox_upd)
}

#[derive(Debug, PartialEq)]
pub struct BBox4 {
    x_rg: (isize, isize),
    y_rg: (isize, isize),
    z_rg: (isize, isize),
    w_rg: (isize, isize),
}

impl Default for BBox4 {
    fn default() -> Self {
        BBox4 {
            x_rg: (isize::MAX, isize::MIN),
            y_rg: (isize::MAX, isize::MIN),
            z_rg: (isize::MAX, isize::MIN),
            w_rg: (isize::MAX, isize::MIN),
        }
    }
}

impl BBox4 {
    pub fn update(&mut self, x: isize, y: isize, z: isize, w: isize) {
        self.x_rg = (min(self.x_rg.0, x), max(self.x_rg.1, x + 1));
        self.y_rg = (min(self.y_rg.0, y), max(self.y_rg.1, y + 1));
        self.z_rg = (min(self.z_rg.0, z), max(self.z_rg.1, z + 1));
        self.w_rg = (min(self.w_rg.0, w), max(self.w_rg.1, w + 1));
    }
}

// tag::parse[]
pub fn parse4(content: &str, z: isize, w: isize) -> (HashSet<(isize, isize, isize, isize)>, BBox4) {
    let mut map = HashSet::new();
    let mut bbox = BBox4::default();
    content.lines().enumerate().for_each(|(y, line)| {
        line.chars().enumerate().for_each(|(x, c)|
            {
                if c == '#' {
                    map.insert((x as isize, y as isize, z, w));
                    bbox.update(x as isize, y as isize, z, w);
                }
            }
        );
    });
    (map, bbox)
}
// end::parse[]

pub fn update_steps4(map: &HashSet<(isize, isize, isize, isize)>, bbox: &BBox4, steps: isize)
                     -> (HashSet<(isize, isize, isize, isize)>, BBox4) {
    assert!(steps > 0, "steps > 0 required");

    let (mut map, mut bbox) = update4(map, bbox);
    for _ in 1..steps {
        let (map_upd, bbox_upd) = update4(&map, &bbox);
        map = map_upd;
        bbox = bbox_upd;
    }
    (map, bbox)
}

// tag::update[]
pub fn update4(map: &HashSet<(isize, isize, isize, isize)>, bbox: &BBox4)
               -> (HashSet<(isize, isize, isize, isize)>, BBox4) {
    let mut map_upd = HashSet::new();
    let mut bbox_upd = BBox4::default();

    for x in bbox.x_rg.0 - 1..bbox.x_rg.1 + 1 {
        for y in bbox.y_rg.0 - 1..bbox.y_rg.1 + 1 {
            for z in bbox.z_rg.0 - 1..bbox.z_rg.1 + 1 {
                for w in bbox.w_rg.0 - 1..bbox.w_rg.1 + 1 {
                    let mut cnt = 0;
                    for k in 0..81 {
                        if k == 40 {
                            continue;
                        }
                        let dx = k % 3 - 1;
                        let dy = (k % 9) / 3 - 1;
                        let dz = (k % 27) / 9 - 1;
                        let dw = k / 27 - 1;

                        if map.contains(&(x + dx, y + dy, z + dz, w + dw)) {
                            cnt += 1;
                            if cnt > 3 {
                                break;
                            }
                        }
                    }
                    let active = map.contains(&(x, y, z, w));
                    if (active && cnt >= 2 && cnt <= 3) || (!active && cnt == 3) {
                        map_upd.insert((x, y, z, w));
                        bbox_upd.update(x, y, z, w);
                    }
                }
            }
        }
    };

    (map_upd, bbox_upd)
}
// end::update[]

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = ".#.
..#
###";

    fn exp_map() -> HashSet<(isize, isize, isize)> {
        let mut map = HashSet::new();
        map.insert((1, 0, 0));
        map.insert((2, 1, 0));
        map.insert((0, 2, 0));
        map.insert((1, 2, 0));
        map.insert((2, 2, 0));
        map
    }

    #[test]
    fn test_parse() {
        let (map, bbox) = parse3(CONTENT, 0);
        assert_eq!(map, exp_map());
        assert_eq!(bbox, BBox3 { x_rg: (0, 3), y_rg: (0, 3), z_rg: (0, 1) })
    }

    fn exp_map_upd() -> HashSet<(isize, isize, isize)> {
        let mut map = HashSet::new();

        map.insert((0, 1, -1));
        map.insert((2, 2, -1));
        map.insert((1, 3, -1));

        map.insert((0, 1, 0));
        map.insert((2, 1, 0));
        map.insert((1, 2, 0));
        map.insert((2, 2, 0));
        map.insert((1, 3, 0));

        map.insert((0, 1, 1));
        map.insert((2, 2, 1));
        map.insert((1, 3, 1));

        map
    }

    #[test]
    fn test_update() {
        let (map, bbox) = parse3(CONTENT, 0);

        println!("{:?}", map);
        let (map, bbox) = update3(&map, &bbox);

        println!("{:?}", bbox);
        for z in bbox.z_rg.0..bbox.z_rg.1 {
            println!("z = {}", z);
            for y in bbox.y_rg.0..bbox.y_rg.1 {
                print!(" ");
                for x in bbox.x_rg.0..bbox.x_rg.1 {
                    if map.contains(&(x, y, z)) { print!("#"); } else { print!(".") }
                }
                println!();
            }
            println!();
        }

        assert_eq!(map, exp_map_upd());
    }

    fn exp_map_upd4() -> HashSet<(isize, isize, isize, isize)> {
        let mut map = HashSet::new();

        map.insert((0, 1, -1, -1));
        map.insert((2, 2, -1, -1));
        map.insert((1, 3, -1, -1));

        map.insert((0, 1, 0, -1));
        map.insert((2, 2, 0, -1));
        map.insert((1, 3, 0, -1));

        map.insert((0, 1, 1, -1));
        map.insert((2, 2, 1, -1));
        map.insert((1, 3, 1, -1));

        map.insert((0, 1, -1, 0));
        map.insert((2, 2, -1, 0));
        map.insert((1, 3, -1, 0));

        map.insert((0, 1, 0, 0));
        map.insert((2, 1, 0, 0));
        map.insert((1, 2, 0, 0));
        map.insert((2, 2, 0, 0));
        map.insert((1, 3, 0, 0));

        map.insert((0, 1, 1, 0));
        map.insert((2, 2, 1, 0));
        map.insert((1, 3, 1, 0));

        map.insert((0, 1, -1, 1));
        map.insert((2, 2, -1, 1));
        map.insert((1, 3, -1, 1));

        map.insert((0, 1, 0, 1));
        map.insert((2, 2, 0, 1));
        map.insert((1, 3, 0, 1));

        map.insert((0, 1, 1, 1));
        map.insert((2, 2, 1, 1));
        map.insert((1, 3, 1, 1));

        map
    }

    #[test]
    fn test_update4() {
        let (map, bbox) = parse4(CONTENT, 0, 0);

        println!("{:?}", map);
        let (map, bbox) = update4(&map, &bbox);

        println!("{:?}", bbox);
        for w in bbox.w_rg.0..bbox.w_rg.1 {
            for z in bbox.z_rg.0..bbox.z_rg.1 {
                println!("z = {}, w = {}", z, w);
                for y in bbox.y_rg.0..bbox.y_rg.1 {
                    print!(" ");
                    for x in bbox.x_rg.0..bbox.x_rg.1 {
                        if map.contains(&(x, y, z, w)) { print!("#"); } else { print!(".") }
                    }
                    println!();
                }
                println!();
            }
        }

        assert_eq!(map, exp_map_upd4());
    }
}