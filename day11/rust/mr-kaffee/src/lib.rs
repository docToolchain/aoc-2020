#[derive(Debug, PartialEq)]
pub struct Grid {
    pub data: Vec<char>,
    pub width: usize,
    pub height: usize,
}

impl Grid {
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

    // tag::run[]
    pub fn run(&self, depth: usize, threshold: usize) -> usize {
        let mut cnt = 1;
        let mut upd = self.update(depth, threshold);
        while upd.1 {
            cnt += 1;
            upd = upd.0.update(depth, threshold);
        };

        println!("Settled after {} rounds with depth: {}, threshold: {}.",
                 cnt, depth, threshold);

        upd.0.data.iter().filter(|c| **c == '#').count()
    }
    // end::run[]

    // tag::update[]
    /// Perform update step.
    ///
    /// Returns a pair `(updated_grid: Grid, changed: bool)`, where `updated_grid` is a new grid
    /// instance with an updated version of `self` and `changed` is a flag indicating whether the
    /// grid actually changed.
    ///
    /// # Examples
    ///
    /// ```
    /// let g1 = mr_kaffee_2020_11::Grid::parse("#.\n.L");
    /// let (g2, changed) = g1.update(1, 4);
    /// assert_eq!(changed, g1 != g2);
    /// ```
    pub fn update(&self, depth: usize, threshold: usize) -> (Grid, bool) {
        let mut data = Vec::new();
        for i in 0..self.width * self.height {
            data.push(match self.data[i] {
                '.' => '.',
                'L' if self.count_occupied(i, depth) == 0 => '#',
                '#' if self.count_occupied(i, depth) >= threshold => 'L',
                v => v,
            });
        };
        let grid = Grid { data, width: self.width, height: self.height };
        let changed = &grid != self;
        (grid, changed)
    }
    // end::update[]

    // tag::count_occupied[]
    fn count_occupied(&self, i: usize, depth: usize) -> usize {
        let x = i % self.width;
        let y = i / self.width;

        let mut cnt = 0;
        cnt += self.is_next_occupied(x, y, 1, 1, depth) as usize;
        cnt += self.is_next_occupied(x, y, 1, 0, depth) as usize;
        cnt += self.is_next_occupied(x, y, 1, -1, depth) as usize;
        cnt += self.is_next_occupied(x, y, -1, 1, depth) as usize;
        cnt += self.is_next_occupied(x, y, -1, 0, depth) as usize;
        cnt += self.is_next_occupied(x, y, -1, -1, depth) as usize;
        cnt += self.is_next_occupied(x, y, 0, 1, depth) as usize;
        cnt += self.is_next_occupied(x, y, 0, -1, depth) as usize;
        cnt
    }
    // end::count_occupied[]

    // tag::is_next_occupied[]
    fn is_next_occupied(&self, x: usize, y: usize, dx: isize, dy: isize, depth: usize) -> bool {
        let mut x = x as isize;
        let mut y = y as isize;
        let mut cnt = 0;
        loop {
            cnt += 1;
            x += dx;
            y += dy;
            if cnt > depth ||
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
        let (grid, ..) = grid.update(1, 4);
        assert_eq!(grid, Grid::parse(CONTENT1));
        let (grid, ..) = grid.update(1, 4);
        assert_eq!(grid, Grid::parse(CONTENT2));
    }

    #[test]
    fn test_grid_run_part1() {
        let grid = Grid::parse(CONTENT0);
        let cnt = grid.run(1, 4);

        assert_eq!(cnt, 37);
    }

    #[test]
    fn test_grid_count_occupied_1() {
        let grid = Grid::parse(CONTENT1);
        let cnt = grid.count_occupied(9, grid.data.len());
        println!("Found {} occupied seats", cnt);
        assert!(cnt < 5);
    }

    #[test]
    fn test_grid_count_occupied_2() {
        let grid = Grid::parse(CONTENT5);
        let (idx, _) = grid.data.iter().enumerate().find(|(_, v)| **v == 'L').expect("No empty seat!");
        println!("Empty seat at {}", idx);
        assert_eq!(grid.count_occupied(idx, grid.data.len()), 8);
    }

    #[test]
    fn test_grid_update_part2() {
        let grid = Grid::parse(CONTENT0);
        let (grid, ..) = grid.update(grid.data.len(), 5);
        assert_eq!(grid, Grid::parse(CONTENT1), "step 1");
        let (grid, ..) = grid.update(grid.data.len(), 5);
        assert_eq!(grid, Grid::parse(CONTENT3), "step 2");
        let (grid, ..) = grid.update(grid.data.len(), 5);
        assert_eq!(grid, Grid::parse(CONTENT4), "step 3");
    }

    #[test]
    fn test_grid_run_part2() {
        let grid = Grid::parse(CONTENT0);
        let cnt = grid.run(grid.data.len(), 5);

        assert_eq!(cnt, 26);
    }
}
