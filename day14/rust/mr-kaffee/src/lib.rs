use std::collections::HashMap;

// tag::bitmask[]
/// A bitmask
///
/// Bits are stored in two integers, `ones` for all one bits, `zeros` for all zero bits. The unset
/// bits can be obtained as `nones = BitMask::ALL & !ones & !zeros`.
#[derive(Debug, PartialEq, Copy, Clone)]
pub struct BitMask {
    ones: u64,
    zeros: u64,
}
// end::bitmask[]

// tag::instruction[]
/// An instruction, with variants `BitMask` for [`BitMask`] values and `Write` for
/// tuple `(u64, u64)` values representing address and value
#[derive(Debug, PartialEq)]
pub enum Instruction {
    BitMask(BitMask),
    Write((u64, u64)),
}
// end::instruction[]

// tag::bitmask_nones[]
/// An Iterator over all possible states the none bits of a [`BitMask`] may take
pub struct BitMaskNones {
    current: u64,
    max: u64,
    mask: u64,
    nones: Vec<u64>,
}
// end::bitmask_nones[]

impl BitMask {
    /// Number of bits
    pub const BITS: usize = 36;

    /// Mask for all bits set
    pub const ALL: u64 = (1 << BitMask::BITS) - 1;

    /// Parse a `BitMask` from a textual input
    ///
    /// Valid lines are composed of exactly [`BitMask::BITS'] characters, each one of '1', '0',
    /// and 'X'
    ///
    /// # Panics
    ///
    /// This function panics if the length of the line is not equal to [`BitMask::BITS'] or it
    /// contains any character other than '0', '1', or 'X'
    pub fn parse(line: &str) -> BitMask {
        assert_eq!(line.len(), BitMask::BITS, "Line length must be equal to BitMask::BITS");

        let (zeros, ones) = line.chars().fold(
            (0, 0),
            |(zeros, ones), c| match c {
                '0' => ((zeros << 1) | 1, ones << 1),
                '1' => (zeros << 1, (ones << 1) | 1),
                'X' => (zeros << 1, ones << 1),
                _ => panic!(format!("Unexpected char: '{}'", c)),
            });

        BitMask { zeros, ones }
    }

    /// Apply the bit-mask (protocol V1)
    pub fn apply(&self, v: u64) -> u64 {
        (v & !self.zeros) | self.ones
    }

    // tag::nones[]
    /// Get a all none bits as a `Vec<u64>` of masks with one bit set in every mask (protocol V2)
    pub fn nones(&self) -> Vec<u64> {
        let mut nones = Vec::new();

        let mask = BitMask::ALL & !self.zeros & !self.ones;
        let mut candidate = 1;
        while candidate < mask {
            if mask & candidate > 0 {
                nones.push(candidate);
            }
            candidate <<= 1;
        }

        nones
    }
    // end::nones[]
}

impl Instruction {
    /// Parse instructions
    pub fn parse(content: &str) -> Vec<Instruction> {
        content.lines().map(|line| {
            // split
            let mut parts = line.split(" = ");

            // assign parts
            let (lhs, rhs) =
                (parts.next().expect("No LHS"), parts.next().expect("No RHS"));

            // parse parts
            match lhs {
                "mask" => Instruction::BitMask(BitMask::parse(rhs)),
                lhs =>
                    Instruction::Write((
                        lhs[4..lhs.len() - 1].parse().expect("Could not parse address"),
                        rhs.parse().expect("Could not parse value")
                    )),
            }
        }).collect()
    }
}

impl BitMaskNones {
    // tag::bitmask_nones_from[]
    /// Construct instance from `[BitMask]`
    pub fn from(mask: &BitMask) -> BitMaskNones {
        let nones = mask.nones();
        BitMaskNones {
            current: 0,
            max: 1 << nones.len(),
            mask: !mask.zeros & !mask.ones & BitMask::ALL,
            nones,
        }
    }
    // end::bitmask_nones_from[]
}

// tag::iterator_impl[]
impl Iterator for BitMaskNones {
    type Item = (u64, u64);

    fn next(&mut self) -> Option<(u64, u64)> {
        if self.current >= self.max {
            // all values consumed
            return None;
        }

        // combine all nones for which the corresponding bit is set in `k` with bitwise or
        let nones = self.nones.iter()
            .enumerate()
            .filter(|(pos, _)| (self.current >> pos) & 1 == 1)
            .fold(0, |nones, (_, none)| nones | none);

        // update counter
        self.current += 1;

        // return mask and none
        Some((self.mask, nones))
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.max - self.current;
        if remaining > usize::MAX as u64 {
            (usize::MAX, None)
        } else {
            (remaining as usize, Some(remaining as usize))
        }
    }
}
// end::iterator_impl[]

// tag::run_v1[]
/// Solve part 1
pub fn run_v1(instructions: &[Instruction]) -> HashMap<u64, u64> {
    // memory map: address -> value
    let mut memory = HashMap::new();

    // current mask
    let mut mask = BitMask { ones: BitMask::ALL, zeros: 0 };

    for instruction in instructions {
        // update mask or insert value with current mask applied
        match instruction {
            Instruction::BitMask(new_mask) => mask = *new_mask,
            Instruction::Write((address, value)) =>
                { memory.insert(*address, mask.apply(*value)); }
        }
    }

    // return memory
    memory
}
// end::run_v1[]

// tag::run_v2[]
/// Solve part 1
///
/// Iterating over all combinations of floating bits is done with my first own Iterator in Rust.
/// See [`BitMaskNones`].
pub fn run_v2(instructions: &[Instruction]) -> HashMap<u64, u64> {
    // memory map: address -> value
    let mut memory = HashMap::new();

    // current mask
    let mut mask = BitMask { ones: BitMask::ALL, zeros: 0 };

    for instruction in instructions {
        match instruction {
            // update mask or insert value at all relevant addresses
            Instruction::BitMask(new_mask) => mask = *new_mask,
            Instruction::Write((address, value)) => {
                // apply ones to address
                let address = *address | mask.ones;
                // iterate over all combinations of floating bits and add value to memory addresses
                for (mask, none) in BitMaskNones::from(&mask) {
                    memory.insert((address & !mask) | none, *value);
                }
            }
        }
    }

    // return memory
    memory
}
// end::run_v2[]

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT_V1: &str = "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0";

    const CONTENT_V2: &str = "mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1";

    fn exp_instructions() -> Vec<Instruction> {
        vec![
            Instruction::BitMask(BitMask { ones: 0b100_0000, zeros: 0b10 }),
            Instruction::Write((8, 11)),
            Instruction::Write((7, 101)),
            Instruction::Write((8, 0)),
        ]
    }

    #[test]
    fn test_bitmask_parse()
    {
        let msk = BitMask::parse("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X");
        assert_eq!(msk.zeros, 0b10);
        assert_eq!(msk.ones, 0b100_0000);
    }

    #[test]
    fn test_bitmask_apply() {
        let msk = BitMask::parse("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X");
        assert_eq!(msk.apply(11), 73);
        assert_eq!(msk.apply(101), 101);
        assert_eq!(msk.apply(0), 64);
    }

    #[test]
    fn test_instruction_parse() {
        let instructions = Instruction::parse(CONTENT_V1);
        assert_eq!(instructions, exp_instructions());
    }

    #[test]
    fn test_run_v1() {
        let mems = run_v1(&exp_instructions());

        assert_eq!(mems.values().sum::<u64>(), 165);

        let mut exp_mems: HashMap<u64, u64> = HashMap::new();
        exp_mems.insert(7, 101);
        exp_mems.insert(8, 64);
        assert_eq!(mems, exp_mems);
    }

    #[test]
    fn test_bitmask_nones() {
        let msk = BitMask::parse("000000000000000000000000000000X1001X");
        let nones = msk.nones();
        assert_eq!(nones, vec![0b1, 0b10_0000]);
    }

    #[test]
    fn test_bitmask_nones_iterator() {
        let msk = BitMask::parse("000000000000000000000000000000X1001X");
        let list: Vec<_> = BitMaskNones::from(&msk).collect();
        assert_eq!(list, vec![
            (0b10_0001, 0b0),
            (0b10_0001, 0b1),
            (0b10_0001, 0b10_0000),
            (0b10_0001, 0b10_0001)]);
    }

    #[test]
    fn test_run_v2() {
        let instructions = Instruction::parse(CONTENT_V2);
        let sum: u64 = run_v2(&instructions).values().sum();
        assert_eq!(sum, 208);
    }
}