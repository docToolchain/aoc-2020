use std::collections::HashSet;
use std::cmp::{min, max};

#[macro_use]
extern crate itertools;

#[derive(Debug, PartialEq)]
pub struct BBox {
    lims: Vec<(isize, isize)>,
}

impl BBox {
    pub fn of_dim(dim: usize) -> Self {
        BBox { lims: (0..dim).map(|_| (isize::MAX, isize::MIN)).collect() }
    }

    pub fn update(&mut self, x: &[isize]) {
        assert_eq!(self.lims.len(), x.len());

        for d in 0..self.lims.len() {
            self.lims[d] = (min(self.lims[d].0, x[d]), max(self.lims[d].1, x[d] + 1));
        }
    }
}

pub fn parse3(content: &str, z: isize) -> (HashSet<(isize, isize, isize)>, BBox) {
    let mut map = HashSet::new();
    let mut bbox = BBox::of_dim(3);
    content.lines().enumerate().for_each(|(y, line)| {
        line.chars().enumerate().for_each(|(x, c)|
            {
                if c == '#' {
                    map.insert((x as isize, y as isize, z));
                    bbox.update(&[x as isize, y as isize, z]);
                }
            }
        );
    });
    (map, bbox)
}

pub fn update_steps3(map: &HashSet<(isize, isize, isize)>, bbox: &BBox, steps: isize)
                     -> (HashSet<(isize, isize, isize)>, BBox) {
    assert!(steps > 0, "steps > 0 required");

    let (mut map, mut bbox) = update3(map, bbox);
    for _ in 1..steps {
        let (map_upd, bbox_upd) = update3(&map, &bbox);
        map = map_upd;
        bbox = bbox_upd;
    }
    (map, bbox)
}

pub fn update3(map: &HashSet<(isize, isize, isize)>, bbox: &BBox)
               -> (HashSet<(isize, isize, isize)>, BBox) {
    let mut map_upd = HashSet::new();
    let mut bbox_upd = BBox::of_dim(3);

    for (x, y, z) in iproduct!(
            bbox.lims[0].0 - 1..bbox.lims[0].1 + 1,
            bbox.lims[1].0 - 1..bbox.lims[1].1 + 1,
            bbox.lims[2].0 - 1..bbox.lims[2].1 + 1)
    {
        let mut cnt = 0;
        for k in 0..27 {
            if k == 13 { continue; }

            if map.contains(&(x + k % 3 - 1,
                              y + (k / 3) % 3 - 1,
                              z + k / 9 - 1)) {
                cnt += 1;
                if cnt > 3 { break; }
            }
        }
        if cnt == 3 || (cnt == 2 && map.contains(&(x, y, z))) {
            map_upd.insert((x, y, z));
            bbox_upd.update(&[x, y, z]);
        }
    };

    (map_upd, bbox_upd)
}

// tag::parse[]
pub fn parse4(content: &str, z: isize, w: isize) -> (HashSet<(isize, isize, isize, isize)>, BBox) {
    let mut map = HashSet::new();
    let mut bbox = BBox::of_dim(4);
    content.lines().enumerate().for_each(|(y, line)| {
        line.chars().enumerate().for_each(|(x, c)|
            {
                if c == '#' {
                    map.insert((x as isize, y as isize, z, w));
                    bbox.update(&[x as isize, y as isize, z, w]);
                }
            }
        );
    });
    (map, bbox)
}
// end::parse[]

pub fn update_steps4(map: &HashSet<(isize, isize, isize, isize)>, bbox: &BBox, steps: isize)
                     -> (HashSet<(isize, isize, isize, isize)>, BBox) {
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
pub fn update4(map: &HashSet<(isize, isize, isize, isize)>, bbox: &BBox)
               -> (HashSet<(isize, isize, isize, isize)>, BBox) {
    let mut map_upd = HashSet::new();
    let mut bbox_upd = BBox::of_dim(4);

    for (x, y, z, w) in iproduct!(
            bbox.lims[0].0 - 1..bbox.lims[0].1 + 1,
            bbox.lims[1].0 - 1..bbox.lims[1].1 + 1,
            bbox.lims[2].0 - 1..bbox.lims[2].1 + 1,
            bbox.lims[3].0 - 1..bbox.lims[3].1 + 1)
    {
        let mut cnt = 0;
        for k in 0..81 {
            if k == 40 { continue; }

            if map.contains(&(x + k % 3 - 1,
                              y + (k / 3) % 3 - 1,
                              z + (k / 9) % 3 - 1,
                              w + k / 27 - 1)) {
                cnt += 1;
                if cnt > 3 { break; }
            }
        }
        if cnt == 3 || (cnt == 2 && map.contains(&(x, y, z, w))) {
            map_upd.insert((x, y, z, w));
            bbox_upd.update(&[x, y, z, w]);
        }
    };

    (map_upd, bbox_upd)
}
// end::update[]

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = ".#.\n..#\n###";

    fn exp_map3() -> HashSet<(isize, isize, isize)> {
        let mut map = HashSet::new();
        map.insert((1, 0, 0));
        map.insert((2, 1, 0));
        map.insert((0, 2, 0));
        map.insert((1, 2, 0));
        map.insert((2, 2, 0));
        map
    }

    #[test]
    fn test_parse3() {
        let (map, bbox) = parse3(CONTENT, 0);
        assert_eq!(map, exp_map3());
        assert_eq!(bbox, BBox { lims: vec![(0, 3), (0, 3), (0, 1)] })
    }

    fn exp_map_upd3() -> HashSet<(isize, isize, isize)> {
        let mut map = HashSet::new();

        let cont1 = "...\n#..\n..#\n.#.";
        let cont2 = "...\n#.#\n.##\n.#.";

        for z in -1..2 {
            let (layer, _) = if z == 0 {
                parse3(cont2, z)
            } else {
                parse3(cont1, z)
            };
            map.extend(layer);
        }

        map
    }

    #[test]
    fn test_update3() {
        let (map, bbox) = parse3(CONTENT, 0);

        println!("{:?}", map);
        let (map, bbox) = update3(&map, &bbox);

        println!("{:?}", bbox);
        for z in bbox.lims[2].0..bbox.lims[2].1 {
            println!("z = {}", z);
            for y in bbox.lims[1].0..bbox.lims[1].1 {
                print!(" ");
                for x in bbox.lims[0].0..bbox.lims[0].1 {
                    if map.contains(&(x, y, z)) { print!("#"); } else { print!(".") }
                }
                println!();
            }
            println!();
        }

        assert_eq!(map, exp_map_upd3());
    }

    fn exp_map_upd4() -> HashSet<(isize, isize, isize, isize)> {
        let mut map = HashSet::new();

        let cont1 = "...\n#..\n..#\n.#.";
        let cont2 = "...\n#.#\n.##\n.#.";

        for z in -1..2 {
            for w in -1..2 {
                let (layer, _) = if z == 0 && w == 0 {
                    parse4(cont2, z, w)
                } else {
                    parse4(cont1, z, w)
                };
                map.extend(layer);
            }
        }

        map
    }

    #[test]
    fn test_update4() {
        let (map, bbox) = parse4(CONTENT, 0, 0);

        println!("{:?}", map);
        let (map, bbox) = update4(&map, &bbox);

        println!("{:?}", bbox);
        for w in bbox.lims[3].0..bbox.lims[3].1 {
            for z in bbox.lims[2].0..bbox.lims[2].1 {
                println!("z = {}, w = {}", z, w);
                for y in bbox.lims[1].0..bbox.lims[1].1 {
                    print!(" ");
                    for x in bbox.lims[0].0..bbox.lims[0].1 {
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