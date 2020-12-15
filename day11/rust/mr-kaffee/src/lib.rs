#[derive(Debug, PartialEq)]
pub struct Grid {
    pub data: Vec<char>,
    pub width: usize,
    pub height: usize,
}

impl Grid {
    pub const DLT: [(isize, isize); 8] = [
        // east
        (1, 0),
        // north-east
        (1, 1),
        // north
        (0, 1),
        // north-west
        (-1, 1),
        // west
        (-1, 0),
        // south-west
        (-1, -1),
        // south
        (0, -1),
        // south-east
        (1, -1)];

    pub fn parse(content: &str) -> Grid {
        let mut data = Vec::new();
        let mut width = 0;
        let mut height = 0;
        for line in content.lines() {
            height += 1;
            if height == 1 {
                width = line.len();
            } else {
                assert_eq!(width, line.len());
            }
            for char in line.chars() {
                data.push(char);
            }
        };
        Grid { data, width, height }
    }

    pub fn count_occupied(&self) -> usize {
        self.data.iter().filter(|c| **c == '#').count()
    }

    // tag::stationary[]
    /// Get a stationary grid
    /// Return `None` if self is already stationary or a `Some(grid)` with a new, stationary grid.
    ///
    /// This function returns an Option<Grid>, since it cannot return self which was not moved
    /// into the function.
    pub fn stationary(&self, depth: usize, threshold: usize) -> Option<Grid> {
        // if grid is already stationary return `None`
        let mut grid = match self.update(depth, threshold) {
            Some(grid) => grid,
            None => return None,
        };

        // update grid until it is stationary
        loop {
            grid = match grid.update(depth, threshold) {
                Some(grid) => grid,
                None => break,
            };
        };

        // return stationary grid
        Some(grid)
    }
    // end::stationary[]

    // tag::update[]
    /// Perform update step.
    ///
    /// Returns an Option<Grid> which is `Some(grid)` in case the grid was actually updated and
    /// `None` if the self is not changed by an update.
    ///
    /// # Examples
    ///
    /// ```
    /// let g1 = mr_kaffee_2020_11::Grid::parse("#.\n.L");
    /// let mut g2 = g1.update(1, 4);
    /// while let Some(g) = g2 {
    ///     assert_ne!(g, g1);
    ///     g2 = g.update(1, 4);
    /// }
    /// ```
    pub fn update(&self, depth: usize, threshold: usize) -> Option<Grid> {
        let mut changed = false;
        let data = self.data.iter().enumerate().map(|(i, v)|
            match v {
                'L' if self.count_occupied_at(i, depth) == 0 => {
                    changed = true;
                    '#'
                }
                '#' if self.count_occupied_at(i, depth) >= threshold => {
                    changed = true;
                    'L'
                }
                v => *v,
            }).collect();

        if changed {
            Some(Grid { data, ..*self })
        } else {
            None
        }
    }
    // end::update[]

    // tag::count_occupied[]
    fn count_occupied_at(&self, i: usize, depth: usize) -> usize {
        let x = i % self.width;
        let y = i / self.width;
        Grid::DLT
            .iter()
            .map(
                |(dx, dy)|
                    self.is_next_occupied(x, y, *dx, *dy, depth) as usize
            ).sum()
    }
    // end::count_occupied[]

    // tag::is_next_occupied[]
    fn is_next_occupied(&self, x: usize, y: usize, dx: isize, dy: isize, depth: usize) -> bool {
        let mut x = x as isize;
        let mut y = y as isize;
        let mut d = 0;
        loop {
            d += 1;
            x += dx;
            y += dy;
            if d > depth ||
                x < 0 || x >= self.width as isize ||
                y < 0 || y >= self.height as isize {
                return false;
            }

            return match self.data[x as usize + self.width * y as usize] {
                '#' => true,
                'L' => false,
                _ => continue,
            };
        }
    }
    // end::is_next_occupied[]
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT0: &str = "L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL";

    const CONTENT1: &str = "#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##";

    const CONTENT2: &str = "#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##";

    const CONTENT3: &str = "#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#";

    const CONTENT4: &str = "#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#";

    const CONTENT5: &str = ".......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....";

    #[test]
    fn test_grid_parse() {
        let grid = Grid::parse(CONTENT0);
        assert_eq!(grid.width, 10);
        assert_eq!(grid.height, 10);
    }

    #[test]
    fn test_grid_update_part1() {
        let grid = Grid::parse(CONTENT0);
        let grid = grid.update(1, 4).unwrap();
        assert_eq!(grid, Grid::parse(CONTENT1));
        let grid = grid.update(1, 4).unwrap();
        assert_eq!(grid, Grid::parse(CONTENT2));
    }

    #[test]
    fn test_grid_run_part1() {
        let grid = Grid::parse(CONTENT0);
        let grid = grid.stationary(1, 4).unwrap();

        assert_eq!(grid.count_occupied(), 37);
    }

    #[test]
    fn test_grid_count_occupied_1() {
        let grid = Grid::parse(CONTENT1);
        let cnt = grid.count_occupied_at(9, grid.data.len());
        println!("Found {} occupied seats", cnt);
        assert!(cnt < 5);
    }

    #[test]
    fn test_grid_count_occupied_2() {
        let grid = Grid::parse(CONTENT5);
        let (idx, _) = grid.data.iter().enumerate().find(|(_, v)| **v == 'L').expect("No empty seat!");
        println!("Empty seat at {}", idx);
        assert_eq!(grid.count_occupied_at(idx, grid.data.len()), 8);
    }

    #[test]
    fn test_grid_update_part2() {
        let grid = Grid::parse(CONTENT0);
        let grid = grid.update(grid.data.len(), 5).unwrap();
        assert_eq!(grid, Grid::parse(CONTENT1), "step 1");
        let grid = grid.update(grid.data.len(), 5).unwrap();
        assert_eq!(grid, Grid::parse(CONTENT3), "step 2");
        let grid = grid.update(grid.data.len(), 5).unwrap();
        assert_eq!(grid, Grid::parse(CONTENT4), "step 3");
    }

    #[test]
    fn test_grid_run_part2() {
        let grid = Grid::parse(CONTENT0);
        let depth = grid.data.len();
        let grid = grid.stationary(depth, 5).unwrap();

        assert_eq!(grid.count_occupied(), 26);
    }
}
