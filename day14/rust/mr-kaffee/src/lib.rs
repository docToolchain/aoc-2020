use std::collections::HashMap;

// tag::bitmask[]
/// A bitmask
#[derive(Debug, PartialEq, Copy, Clone)]
pub struct BitMask {
    ones: u64,
    zeros: u64,
}
// end::bitmask[]

// tag::instruction[]
/// An instruction, with variants `BitMask` for [`BitMask`] values and `Write` for
/// tuple `(usize, u64)` values
#[derive(Debug, PartialEq)]
pub enum Instruction {
    BitMask(BitMask),
    Write((u64, u64)),
}
// end::instruction[]

// tag::bitmask_nones[]
/// An iterator over all nones of a bit-mask
pub struct BitMaskNones {
    bits: u64,
    bits_max: u64,
    mask: u64,
    nones: Vec<u64>,
}
// end::bitmask_nones[]

impl BitMask {
    /// mask for all bits set
    pub const ALL: u64 = (1 << 36) - 1;

    /// parse a `BitMask` from a textual input
    pub fn parse(line: &str) -> BitMask {
        let mut msk = BitMask { ones: 0, zeros: 0 };
        for c in line.chars() {
            match c {
                '1' => {
                    msk.zeros = msk.zeros << 1;
                    msk.ones = (msk.ones << 1) | 1;
                }
                '0' => {
                    msk.zeros = (msk.zeros << 1) | 1;
                    msk.ones = msk.ones << 1;
                }
                'X' => {
                    msk.zeros = msk.zeros << 1;
                    msk.ones = msk.ones << 1;
                }
                c => panic!(format!("Unexpected char: '{}'", c)),
            }
        }
        msk
    }

    /// Apply the bit-mask (protocol V1)
    pub fn apply(&self, v: u64) -> u64 {
        (v & !self.zeros) | self.ones
    }

    // tag::nones[]
    /// Get a all none bits as a `Vec<u64>` (protocol V2)
    pub fn nones(&self) -> Vec<u64> {
        let mut nones = Vec::new();

        let mask = !self.zeros & !self.ones & BitMask::ALL;
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
        let mut instructions = Vec::new();

        for line in content.lines() {
            let mut parts = line.split(" = ");
            let left = parts.next().expect("No LHS");
            let right = parts.next().expect("No RHS");

            instructions.push(match left {
                "mask" => Instruction::BitMask(BitMask::parse(right)),
                left =>
                    Instruction::Write((
                        left[4..left.len() - 1].parse().expect("Could not parse address"),
                        right.parse().expect("Could not parse value"))),
            });
        };

        instructions
    }
}

impl BitMaskNones {
    // tag::bitmask_nones_from[]
    /// Construct from `[BitMask]`
    pub fn from(mask: &BitMask) -> BitMaskNones {
        let nones = mask.nones();
        let bits_max = 1 << nones.len();
        BitMaskNones {
            bits: 0,
            bits_max,
            mask: !mask.zeros & !mask.ones & BitMask::ALL,
            nones
        }
    }
    // end::bitmask_nones_from[]
}

// tag::iterator_impl[]
impl Iterator for BitMaskNones {
    type Item = (u64, u64);

    fn next(&mut self) -> Option<(u64, u64)> {
        if self.bits >= self.bits_max {
            // all values consumed
            return None;
        }

        // combine all nones for which the corresponding bit is set in `k` with bitwise or
        let nones = self.nones.iter()
            .enumerate()
            .fold(0,
                  |nones, (pos, none)|
                      nones | (((self.bits as u64 >> pos) & 1) * *none));

        // update counter
        self.bits += 1;

        // return mask and none
        Some((self.mask, nones))
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
                let address = *address as u64 | mask.ones;
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
            Instruction::BitMask(BitMask {
                ones: 0b100_0000,
                zeros: 0b10,
            }),
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
        assert_eq!(list, vec![(0b10_0001, 0b0), (0b10_0001, 0b1), (0b10_0001, 0b10_0000), (0b10_0001, 0b10_0001)]);
    }

    #[test]
    fn test_run_v2() {
        let instructions = Instruction::parse(CONTENT_V2);
        let sum: u64 = run_v2(&instructions).values().sum();
        assert_eq!(sum, 208);
    }
}