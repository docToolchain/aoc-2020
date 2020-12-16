use regex::Regex;

// tag::Step[]
/// single step for the ship
#[derive(Debug, PartialEq)]
pub enum Step {
    North(i32),
    South(i32),
    East(i32),
    West(i32),
    Fwd(i32),
    Reverse,
    Left,
    Right,
}
// end::Step[]

// tag::Heading[]
/// Heading of the ship
///
/// Modeling the heading as an enum allows to use Rust's type system to ensure the heading is
/// always valid. Once the input is successfully parsed, Rust ensures at compile time that the
/// data will always be valid
#[derive(Debug, PartialEq)]
pub enum Heading {
    East,
    South,
    West,
    North,
}
// end::Heading[]

impl Heading {
    /// turn left (counter-clockwise)
    pub fn left(&self) -> Heading {
        match self {
            Heading::East => Heading::North,
            Heading::South => Heading::East,
            Heading::West => Heading::South,
            Heading::North => Heading::West,
        }
    }

    /// turn right (counter-clockwise)
    pub fn right(&self) -> Heading {
        match self {
            Heading::East => Heading::South,
            Heading::South => Heading::West,
            Heading::West => Heading::North,
            Heading::North => Heading::East,
        }
    }

    /// reverse direction
    pub fn reverse(&self) -> Heading {
        match self {
            Heading::East => Heading::West,
            Heading::South => Heading::North,
            Heading::West => Heading::East,
            Heading::North => Heading::South,
        }
    }
}

impl Step {
    /// Parse a vector of steps from an input string
    ///
    /// # Examples
    /// ```
    /// let input = "N5 S6 L90 R270 F1";
    /// let steps = mr_kaffee_2020_12::Step::parse(&input);
    /// assert_eq!(steps, vec![
    ///     mr_kaffee_2020_12::Step::North(5),
    ///     mr_kaffee_2020_12::Step::South(6),
    ///     mr_kaffee_2020_12::Step::Left,
    ///     mr_kaffee_2020_12::Step::Left,
    ///     mr_kaffee_2020_12::Step::Fwd(1),
    /// ]);
    /// ```
    ///
    /// # Panics
    ///
    /// If the input string does not contain of a valid character (N, S, E, W, F, L, R) followed by
    /// a positive integer number or if the number following any L or R is not a multiple of 90.
    ///
    pub fn parse(input: &str) -> Vec<Step> {
        let re = Regex::new(r"(\w)(\d+)\s*").expect("Illegal regular expression");
        let mut list = Vec::new();

        for cap in re.captures_iter(input) {
            let val = cap[2].parse().expect("Could not parse number");
            list.push(match &cap[1] {
                "N" => Step::North(val),
                "S" => Step::South(val),
                "E" => Step::East(val),
                "W" => Step::West(val),
                "F" => Step::Fwd(val),
                "L" if (360 + val % 360) % 390 == 0 => Step::Fwd(0),
                "L" if (360 + val % 360) % 360 == 90 => Step::Left,
                "L" if (360 + val % 360) % 360 == 180 => Step::Reverse,
                "L" if (360 + val % 360) % 360 == 270 => Step::Right,
                "R" if (360 + val % 360) % 360 == 0 => Step::Fwd(0),
                "R" if (360 + val % 360) % 360 == 90 => Step::Right,
                "R" if (360 + val % 360) % 360 == 180 => Step::Reverse,
                "R" if (360 + val % 360) % 360 == 270 => Step::Left,
                _ => panic!(format!("Unknown instruction {} with value {}", &cap[1], val)),
            });
        };

        list
    }
}

// tag::Ship[]
/// a ship with heading, position, and waypoint position
#[derive(Debug, PartialEq)]
pub struct Ship {
    heading: Heading,

    pos: (i32, i32),

    wp: (i32, i32),
}
// end::Ship[]

impl Ship {
    /// create a new ship in the initial configuration (heading: East, position: 0, waypoint
    /// position: North 10, East 1)
    pub fn new() -> Ship {
        Ship { heading: Heading::East, pos: (0, 0), wp: (10, 1) }
    }

    // tag::apply[]
    /// apply a single step to the ship with or without waypoint (for part 1 and part 2
    /// respectively)
    ///
    /// # Examples
    /// ```
    /// let mut ship = mr_kaffee_2020_12::Ship::new();
    ///
    /// // ship starts at (0, 0)
    /// assert_eq!(ship.distance(), 0);
    ///
    /// ship.apply(&mr_kaffee_2020_12::Step::North(20), false);
    /// // ship will be at (0, 10)
    /// assert_eq!(ship.distance(), 20);
    ///
    /// ship.apply(&mr_kaffee_2020_12::Step::Fwd(1), false);
    /// // waypoint is at (10, 1) -> ship will be at (10, 11)
    /// assert_eq!(ship.distance(), 21);
    /// ```
    pub fn apply(&mut self, instr: &Step, use_wp: bool) {
        if use_wp {
            match instr {
                Step::North(v) => self.wp.1 += v,
                Step::South(v) => self.wp.1 -= v,
                Step::East(v) => self.wp.0 += v,
                Step::West(v) => self.wp.0 -= v,
                Step::Left => self.wp = (-self.wp.1, self.wp.0),
                Step::Reverse => self.wp = (-self.wp.0, -self.wp.1),
                Step::Right => self.wp = (self.wp.1, -self.wp.0),
                Step::Fwd(v) => self.pos =
                    (self.pos.0 + v * self.wp.0, self.pos.1 + v * self.wp.1),
            };
        } else {
            match instr {
                Step::North(v) => self.pos.1 += v,
                Step::South(v) => self.pos.1 -= v,
                Step::East(v) => self.pos.0 += v,
                Step::West(v) => self.pos.0 -= v,
                Step::Left => self.heading = self.heading.left(),
                Step::Reverse => self.heading = self.heading.reverse(),
                Step::Right => self.heading = self.heading.right(),
                Step::Fwd(v) => self.pos = match self.heading {
                    Heading::East => (self.pos.0 + v, self.pos.1),
                    Heading::South => (self.pos.0, self.pos.1 - v),
                    Heading::West => (self.pos.0 - v, self.pos.1),
                    Heading::North => (self.pos.0, self.pos.1 + v),
                }
            }
        };
    }
    // end::apply[]

    /// apply a series of steps in sequence  with or without waypoint (for part 1 and part 2
    /// respectively)
    pub fn apply_all(&mut self, list: &[Step], use_wp: bool) {
        list.iter().fold((), |_, v| self.apply(v, use_wp));
    }

    /// calculate the Manhattan distance of the ship to the origin
    pub fn distance(&self) -> i32 {
        self.pos.0.abs() + self.pos.1.abs()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "F10
N3
F7
R90
F11";

    fn steps() -> Vec<Step> {
        vec![Step::Fwd(10), Step::North(3), Step::Fwd(7), Step::Right, Step::Fwd(11)]
    }

    #[test]
    fn test_instr_parse() {
        let steps = Step::parse(CONTENT);
        assert_eq!(steps, steps());
    }

    #[test]
    fn test_ship_apply_all_1() {
        let mut ship = Ship::new();
        ship.apply_all(&steps(), false);
        assert_eq!(ship.distance(), 25);
    }

    #[test]
    fn test_ship_apply_all_2() {
        let mut ship = Ship::new();
        ship.apply_all(&steps(), true);
        println!("{:?}", ship);
        assert_eq!(ship.distance(), 286);
    }

    #[test]
    fn test_ship_apply_2() {
        let mut ship = Ship::new();

        println!("Initial: {:?}", ship);

        ship.apply(&Step::Fwd(10), true);
        println!("After Fwd(10): {:?}", ship);
        assert_eq!(ship.pos, (100, 10));

        ship.apply(&Step::North(3), true);
        println!("After North(3): {:?}", ship);
        assert_eq!(ship.wp, (10, 4));

        ship.apply(&Step::Fwd(7), true);
        println!("After Fwd(7): {:?}", ship);
        assert_eq!(ship.pos, (170, 38));

        ship.apply(&Step::Right, true);
        println!("After Right: {:?}", ship);
        assert_eq!(ship.wp, (4, -10));

        ship.apply(&Step::Fwd(11), true);
        println!("After Fwd(11): {:?}", ship);
        assert_eq!(ship.pos, (214, -72));
    }
}