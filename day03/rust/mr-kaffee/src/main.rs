use std::fs;

fn main() {
    // read contents from file
    let content = fs::read_to_string("input.txt")
        .expect("Could not read file");

    // parse grid
    let grid = Grid::parse(&content)
        .expect("Could not parse grid");

    // calculate trees for slope 3-1 (part 1)
    let slope = Slope { right: 3, down: 1 };
    let trees = grid.count_trees(&slope);
    println!("See {} trees with {:?}", trees, &slope);
    assert_eq!(trees, 164);

    // calculate product of trees for all slopes
    let prod = grid.product(&vec![
        Slope { right: 1, down: 1 },
        Slope { right: 3, down: 1 },
        Slope { right: 5, down: 1 },
        Slope { right: 7, down: 1 },
        Slope { right: 1, down: 2 },
    ]);
    println!("Product is {}", prod);
    assert_eq!(prod, 5_007_658_656);
}

#[derive(Debug, PartialEq)]
struct Grid {
    data: Vec<char>,
    width: usize,
    height: usize,
}

#[derive(Debug, PartialEq)]
struct Slope {
    right: usize,
    down: usize,
}

impl Grid {
    // tag::product[]
    fn product(&self, slopes: &[Slope]) -> u64 {
        // calculate product converting u32 -> u64 on the way
        slopes.iter()
            .map(|slope| self.count_trees(slope) as u64)
            .product()
    }
    // end::product[]

    fn count_trees(&self, slope: &Slope) -> u32 {
        let mut x: usize = 0;
        let mut y: usize = 0;

        let mut count: u32 = 0;

        while y < self.height {
            if self.data[x + self.width * y] == '#' {
                count += 1;
            }

            x = (x + slope.right) % self.width;
            y += slope.down;
        };

        count
    }

    fn parse(content: &str) -> Result<Grid, String> {
        let mut data = Vec::new();
        let mut width: usize = 0;
        let mut height: usize = 0;

        for (idx, line) in content.lines().enumerate() {
            if idx == 0 {
                width = line.len();
            } else if width != line.len() {
                return Err(format!("Line {}: {} has length {}, expected {}",
                                   idx, line, line.len(), width));
            }

            height += 1;

            for c in line.chars() {
                data.push(c);
            }
        };

        Ok(Grid { data, width, height })
    }
}

#[cfg(test)]
mod tests {
    use std::iter::FromIterator;
    use super::*;

    const CONTENT: &str = "..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#";
    const DATA: &str = "..##.......\
#...#...#..\
.#....#..#.\
..#.#...#.#\
.#...##..#.\
..#.##.....\
.#.#.#....#\
.#........#\
#.##...#...\
#...##....#\
.#..#...#.#";

    #[test]
    fn test_grid_parse() {
        let grid = Grid::parse(CONTENT).expect("Could not parse grid.");

        assert_eq!(grid.width, 11);
        assert_eq!(grid.height, 11);
        assert_eq!(grid.data, Vec::from_iter(DATA.chars()));
    }

    #[test]
    fn test_grid_count_trees() {
        let grid = Grid {
            data: Vec::from_iter(DATA.chars()),
            width: 11,
            height: 11,
        };

        assert_eq!(grid.count_trees(&Slope { right: 3, down: 1 }), 7);
    }

    #[test]
    fn test_grid_prod() {
        let slopes = vec![
            Slope { right: 1, down: 1 },
            Slope { right: 3, down: 1 },
            Slope { right: 5, down: 1 },
            Slope { right: 7, down: 1 },
            Slope { right: 1, down: 2 },
        ];

        let grid = Grid {
            data: Vec::from_iter(DATA.chars()),
            width: 11,
            height: 11,
        };

        assert_eq!(grid.product(&slopes), 336);
    }
}
