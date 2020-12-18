use std::collections::HashSet;
use std::cmp::{min, max};
use std::hash::Hash;
use std::fmt::Debug;

// tag::coordinate[]
pub trait Coordinate<T> {
    fn to_index(&self, x: &Self, offset: &Self) -> T;
    fn to_coord(&self, idx: T, offset: &Self) -> Self;
    fn set_to_min(&mut self, other: &Self);
    fn set_to_max(&mut self, other: &Self);
    fn subtract(&self, other: &Self) -> Self;
    fn add_scalar(&self, inc: T) -> Self;
    fn prod(&self) -> T;
    fn set(&mut self, pos: usize, value: T);
    fn min() -> Self;
    fn max() -> Self;
    fn zero() -> Self;
}

impl Coordinate<isize> for (isize, isize, isize) {
    fn to_index(&self, x: &Self, offset: &Self) -> isize {
        let mut idx = x.2 - offset.2;
        idx = (idx * self.1) + x.1 - offset.1;
        idx = (idx * self.0) + x.0 - offset.0;
        idx
    }

    fn to_coord(&self, idx: isize, offset: &Self) -> Self {
        let mut idx = idx;
        let x = idx % self.0 + offset.0;
        idx /= self.0;
        let y = idx % self.1 + offset.1;
        idx /= self.1;
        let z = idx % self.2 + offset.2;
        (x, y, z)
    }

    fn set_to_min(&mut self, other: &Self) {
        self.0 = min(self.0, other.0);
        self.1 = min(self.1, other.1);
        self.2 = min(self.2, other.2);
    }

    fn set_to_max(&mut self, other: &Self) {
        self.0 = max(self.0, other.0);
        self.1 = max(self.1, other.1);
        self.2 = max(self.2, other.2);
    }

    fn subtract(&self, other: &Self) -> Self {
        (self.0 - other.0, self.1 - other.1, self.2 - other.2)
    }

    fn add_scalar(&self, inc: isize) -> Self {
        (self.0 + inc, self.1 + inc, self.2 + inc)
    }

    fn prod(&self) -> isize {
        self.0 * self.1 * self.2
    }

    fn set(&mut self, pos: usize, value: isize) {
        match pos {
            0 => self.0 = value,
            1 => self.1 = value,
            2 => self.2 = value,
            _ => panic!(format!("Index out of bounds: {}", pos)),
        }
    }

    fn min() -> Self {
        (isize::MIN, isize::MIN, isize::MIN)
    }

    fn max() -> Self {
        (isize::MAX, isize::MAX, isize::MAX)
    }

    fn zero() -> Self {
        (0, 0, 0)
    }
}

impl Coordinate<isize> for (isize, isize, isize, isize) {
    fn to_index(&self, x: &Self, offset: &Self) -> isize {
        let mut idx = x.3 - offset.3;
        idx = (idx * self.2) + x.2 - offset.2;
        idx = (idx * self.1) + x.1 - offset.1;
        idx = (idx * self.0) + x.0 - offset.0;
        idx
    }

    fn to_coord(&self, idx: isize, offset: &Self) -> Self {
        let mut idx = idx;
        let x = idx % self.0 + offset.0;
        idx /= self.0;
        let y = idx % self.1 + offset.1;
        idx /= self.1;
        let z = idx % self.2 + offset.2;
        idx /= self.2;
        let w = idx % self.3 + offset.3;
        (x, y, z, w)
    }

    fn set_to_min(&mut self, other: &Self) {
        self.0 = min(self.0, other.0);
        self.1 = min(self.1, other.1);
        self.2 = min(self.2, other.2);
        self.3 = min(self.3, other.2);
    }

    fn set_to_max(&mut self, other: &Self) {
        self.0 = max(self.0, other.0);
        self.1 = max(self.1, other.1);
        self.2 = max(self.2, other.2);
        self.3 = max(self.3, other.2);
    }

    fn subtract(&self, other: &Self) -> Self {
        (self.0 - other.0, self.1 - other.1, self.2 - other.2, self.3 - other.3)
    }

    fn add_scalar(&self, inc: isize) -> Self {
        (self.0 + inc, self.1 + inc, self.2 + inc, self.3 + inc)
    }

    fn prod(&self) -> isize {
        self.0 * self.1 * self.2 * self.3
    }

    fn set(&mut self, pos: usize, value: isize) {
        match pos {
            0 => self.0 = value,
            1 => self.1 = value,
            2 => self.2 = value,
            3 => self.3 = value,
            _ => panic!(format!("Index out of bounds: {}", pos)),
        }
    }

    fn min() -> Self {
        (isize::MIN, isize::MIN, isize::MIN, isize::MIN)
    }

    fn max() -> Self {
        (isize::MAX, isize::MAX, isize::MAX, isize::MAX)
    }

    fn zero() -> Self {
        (0, 0, 0, 0)
    }
}
// end::coordinate[]

#[derive(Debug, PartialEq)]
pub struct BBox<T>
    where T: Coordinate<isize> + Debug
{
    min: T,
    max: T,
}

impl<T> BBox<T>
    where T: Coordinate<isize> + Debug
{
    pub fn from(min: T, max: T) -> Self {
        BBox { min, max }
    }

    pub fn update(&mut self, x: &T) {
        self.max.set_to_max(&x.add_scalar(1));
        self.min.set_to_min(x);
    }

    pub fn width(&self) -> T {
        self.max.subtract(&self.min)
    }
}

// tag::parse[]
pub fn parse<T>(content: &str, z: &[isize]) -> (HashSet<T>, BBox<T>)
    where T: Coordinate<isize> + Eq + Hash + Debug
{
    let mut map = HashSet::new();
    let mut bbox = BBox::from(T::max(), T::min());
    content.lines().enumerate().for_each(|(y, line)| {
        line.chars().enumerate().for_each(|(x, c)|
            {
                if c == '#' {
                    let mut val = T::zero();
                    val.set(0, x as isize);
                    val.set(1, y as isize);
                    for k in 0..z.len() {
                        val.set(2 + k, z[k]);
                    }
                    bbox.update(&val);
                    map.insert(val);
                }
            }
        );
    });
    (map, bbox)
}
// end::parse[]

pub fn update_steps<T>(map: &HashSet<T>, bbox: &BBox<T>, steps: isize) -> (HashSet<T>, BBox<T>)
    where T: Coordinate<isize> + Eq + Hash + Debug
{
    assert!(steps > 0, "steps > 0 required");

    let (mut map, mut bbox) = update(map, bbox);
    for _ in 1..steps {
        let (map_upd, bbox_upd) = update(&map, &bbox);
        map = map_upd;
        bbox = bbox_upd;
    }
    (map, bbox)
}

// tag::update[]
pub fn update<T>(map: &HashSet<T>, bbox: &BBox<T>) -> (HashSet<T>, BBox<T>)
    where T: Coordinate<isize> + Eq + Hash + Debug
{
    let mut map_upd = HashSet::new();
    let mut bbox_upd = BBox::from(T::max(), T::min());

    let bbox_search = BBox::from(bbox.min.add_scalar(-1), bbox.max.add_scalar(1));
    let width_search = bbox_search.width();
    let n_search = width_search.prod();

    for idx in 0..n_search {
        let coord = width_search.to_coord(idx, &bbox_search.min);

        let bbox_dlt = BBox::from(coord.add_scalar(-1), coord.add_scalar(2));
        let width_dlt = bbox_dlt.width();
        let n_dlt = width_dlt.prod();

        let mut cnt = 0;
        for k in 0..n_dlt {
            if k == n_dlt / 2 { continue; }

            if map.contains(&width_dlt.to_coord(k, &bbox_dlt.min)) {
                cnt += 1;
                if cnt > 3 { break; }
            }
        }

        if cnt == 3 || (cnt == 2 && map.contains(&coord)) {
            bbox_upd.update(&coord);
            map_upd.insert(coord);
        }
    }

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
    fn test_parse_3() {
        let (map, bbox) = parse(CONTENT, &[0; 1]);
        assert_eq!(map, exp_map3());
        assert_eq!(bbox, BBox { min: (0, 0, 0), max: (3, 3, 1) })
    }

    fn exp_map_upd_3() -> HashSet<(isize, isize, isize)> {
        let mut map = HashSet::new();

        let cont1 = "...\n#..\n..#\n.#.";
        let cont2 = "...\n#.#\n.##\n.#.";

        for z in -1..2 {
            let (layer, _) = if z == 0 {
                parse::<(isize, isize, isize)>(cont2, &[z; 1])
            } else {
                parse(cont1, &[z; 1])
            };
            map.extend(layer);
        }

        map
    }

    #[test]
    fn test_update_3() {
        let (map, bbox) = parse::<(isize, isize, isize)>(CONTENT, &[0; 1]);

        println!("{:?}", map);
        let (map, bbox) = update(&map, &bbox);

        println!("{:?}", bbox);
        for z in bbox.min.2..bbox.max.2 {
            println!("z = {}", z);
            for y in bbox.min.1..bbox.max.1 {
                print!(" ");
                for x in bbox.min.0..bbox.max.0 {
                    if map.contains(&(x, y, z)) { print!("#"); } else { print!(".") }
                }
                println!();
            }
            println!();
        }

        assert_eq!(map, exp_map_upd_3());
    }

    fn exp_map_upd_4() -> HashSet<(isize, isize, isize, isize)> {
        let mut map = HashSet::new();

        let cont1 = "...\n#..\n..#\n.#.";
        let cont2 = "...\n#.#\n.##\n.#.";

        for z in -1..2 {
            for w in -1..2 {
                let (layer, _) = if z == 0 && w == 0 {
                    parse::<(isize, isize, isize, isize)>(cont2, &[z, w])
                } else {
                    parse(cont1, &[z, w])
                };
                map.extend(layer);
            }
        }

        map
    }

    #[test]
    fn test_update_4() {
        let (map, bbox) = parse(CONTENT, &[0, 0]);

        println!("{:?}", map);
        let (map, bbox) = update::<(isize, isize, isize, isize)>(&map, &bbox);

        println!("{:?}", bbox);
        for w in bbox.min.3..bbox.max.3 {
            for z in bbox.min.2..bbox.max.2 {
                println!("z = {}, w = {}", z, w);
                for y in bbox.min.1..bbox.max.1 {
                    print!(" ");
                    for x in bbox.min.0..bbox.max.0 {
                        if map.contains(&(x, y, z, w)) { print!("#"); } else { print!(".") }
                    }
                    println!();
                }
                println!();
            }
        }

        assert_eq!(map, exp_map_upd_4());
    }

    #[test]
    fn test_coord_to_coord() {
        let min = (-1, -1, -1);
        let width = (3 as isize, 3 as isize, 3 as isize);
        assert_eq!(width.to_coord(0, &min), (-1, -1, -1));
        assert_eq!(width.to_coord(3, &min), (-1, 0, -1));
        assert_eq!(width.to_coord(9, &min), (-1, -1, 0));
        assert_eq!(width.to_coord(18 + 6 + 1, &min), (0, 1, 1));

        for x in -1..2 {
            for y in -1..2 {
                for z in -1..2 {
                    let idx = width.to_index(&(x, y, z), &min);
                    let c = width.to_coord(idx, &min);
                    assert_eq!(c, (x, y, z));
                }
            }
        }

        let width = (3, 3, 3, 3);
        let min = (-1 as isize, -1 as isize, -1 as isize, -1 as isize);
        for x in -1..2 {
            for y in -1..2 {
                for z in -1..2 {
                    for w in -1..2 {
                        let idx = width.to_index(&(x, y, z, w), &min);
                        let c = width.to_coord(idx, &min);
                        assert_eq!(c, (x, y, z, w));
                    }
                }
            }
        }
    }

    #[test]
    fn test_coord_to_idx() {
        let min = (-1, -1, -1);
        let width = (3 as isize, 3 as isize, 3 as isize);
        assert_eq!(width.to_index(&(-1, -1, -1), &min), 0);
        assert_eq!(width.to_index(&(-1, 0, -1), &min), 3);
        assert_eq!(width.to_index(&(-1, -1, 0), &min), 9);
        assert_eq!(width.to_index(& (0, 1, 1), &min), 18 + 6 + 1);

        for idx in 0..width.prod() {
            let c = width.to_coord(idx, &min);
            let i = width.to_index(&c, &min);
            assert_eq!(i, idx);
        }

        let width = (3, 3, 3, 3);
        let min = (-1 as isize, -1 as isize, -1 as isize, -1 as isize);
        for idx in 0..width.prod() {
            let c = width.to_coord(idx, &min);
            let i = width.to_index(&c, &min);
            assert_eq!(i, idx);
        }
    }
}