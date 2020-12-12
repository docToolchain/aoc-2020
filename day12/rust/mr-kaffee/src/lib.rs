use regex::Regex;

// tag::Instr[]
#[derive(Debug, PartialEq)]
pub enum Instr {
    N(i32),
    S(i32),
    E(i32),
    W(i32),
    L(i32),
    R(i32),
    F(i32),
}
// end::Instr[]

impl Instr {
    pub fn parse(input: &str) -> Vec<Instr> {
        let re = Regex::new(r"(\w)(\d+)\s*").expect("Illegal regular expression");
        let mut list = Vec::new();

        for cap in re.captures_iter(input) {
            let val = cap[2].parse().expect("Could not parse number");
            list.push(match &cap[1] {
                "N" => Instr::N(val),
                "S" => Instr::S(val),
                "E" => Instr::E(val),
                "W" => Instr::W(val),
                "L" => Instr::L(val),
                "R" => Instr::R(val),
                "F" => Instr::F(val),
                _ => panic!(format!("Unknown instruction {}", &cap[1])),
            });
        };

        list
    }
}

// tag::Ship[]
#[derive(Debug, PartialEq, Default)]
pub struct Ship {
    heading: i32,

    pos: (i32, i32),

    wp: (i32, i32),
}
// end::Ship[]

impl Ship {
    pub fn new() -> Ship {
        Ship { heading: 90, pos: (0, 0), wp: (10, 1) }
    }

    // tag::apply[]
    pub fn apply(&mut self, instr: &Instr, use_wp: bool) {
        if use_wp {
            match instr {
                Instr::N(v) => self.wp.1 += v,
                Instr::S(v) => self.wp.1 -= v,
                Instr::E(v) => self.wp.0 += v,
                Instr::W(v) => self.wp.0 -= v,
                Instr::L(0) | Instr::R(0) => (),
                Instr::L(90) | Instr::R(270) => self.wp = (-self.wp.1, self.wp.0),
                Instr::L(180) | Instr::R(180) => self.wp = (-self.wp.0, -self.wp.1),
                Instr::L(270) | Instr::R(90) => self.wp = (self.wp.1, -self.wp.0),
                Instr::F(v) => self.pos =
                    (self.pos.0 + v * self.wp.0, self.pos.1 + v * self.wp.1),
                Instr::R(_) | Instr::L(_) =>
                    panic!(format!("Cannot execute {:?}", instr)),
            };
        } else {
            match instr {
                Instr::N(v) => self.pos.1 += v,
                Instr::S(v) => self.pos.1 -= v,
                Instr::E(v) => self.pos.0 += v,
                Instr::W(v) => self.pos.0 -= v,
                Instr::L(v) => self.heading = (self.heading - v + 360) % 360,
                Instr::R(v) => self.heading = (self.heading + v + 360) % 360,
                Instr::F(v) if self.heading == 0 => self.pos.1 += v,
                Instr::F(v) if self.heading == 90 => self.pos.0 += v,
                Instr::F(v) if self.heading == 180 => self.pos.1 -= v,
                Instr::F(v) if self.heading == 270 => self.pos.0 -= v,
                Instr::F(v) => panic!(format!("Cannot turn by {}", v))
            }
        };
    }
    // end::apply[]

    pub fn apply_all(&mut self, list: &[Instr], use_wp: bool) {
        list.iter().fold((), |_, v| self.apply(v, use_wp));
    }

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

    fn instructions() -> Vec<Instr> {
        vec![Instr::F(10), Instr::N(3), Instr::F(7), Instr::R(90), Instr::F(11)]
    }

    #[test]
    fn test_instr_parse() {
        let list = Instr::parse(CONTENT);
        assert_eq!(list, instructions());
    }

    #[test]
    fn test_ship_apply_all_1() {
        let mut ship = Ship::new();
        ship.apply_all(&instructions(), false);
        assert_eq!(ship.distance(), 25);
    }

    #[test]
    fn test_ship_apply_all_2() {
        let mut ship = Ship::new();
        ship.apply_all(&instructions(), true);
        assert_eq!(ship.distance(), 286);
    }

    #[test]
    fn test_ship_apply_2() {
        let mut ship = Ship::new();

        ship.apply(&Instr::F(10), true);
        assert_eq!(ship.pos, (100, 10));

        ship.apply(&Instr::N(3), true);
        assert_eq!(ship.wp, (10, 4));

        ship.apply(&Instr::F(7), true);
        assert_eq!(ship.pos, (170, 38));
    }
}