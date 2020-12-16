use std::collections::HashMap;

// tag::init[]
/// Initialize map for memory game
///
/// The input is expected to be a comma separated list of integers
/// The function returns a map where the values in the input list are the keys and their position's
/// in the input list are their values. The last value is not in the map but returned in addition to
/// the map
pub fn init(line: &str) -> (HashMap<isize, isize>, isize) {
    let mut last = 0;
    let mut map: HashMap<_, _> = String::from(line).split(",")
        .map(|v| v.parse::<isize>().expect("Could not parse number"))
        .enumerate()
        .map(|(a, b)| {
            last = b;
            (b, a as isize)
        })
        .collect();
    map.remove(&last);
    (map, last)
}
// end::init[]

// tag::play[]
/// Play memory game rounds
///
/// Arguments:
///
/// `map`   map as created by [`init`]
/// `last`  last value soken
/// `start` start round (inclusive, initially length of the input)
/// `end`   end round (exclusive)
///
/// Returns: the value spoken in the round end - 1
///
/// # Examples
///
/// ```
/// let (mut map, last) = mr_kaffee_2020_15::init("0,3,6");
/// let last = mr_kaffee_2020_15::play(&mut map, last, 3, 7);
/// assert_eq!(last, 1);
/// let last = mr_kaffee_2020_15::play(&mut map, last, 7, 10);
/// assert_eq!(last, 0);
/// ```
pub fn play(map: &mut HashMap<isize, isize>, last: isize, start: isize, end: isize) -> isize {
    let mut last = last;

    for turn in start..end {
        last = match map.insert(last, turn - 1) {
            Some(value) => turn - 1 - value,
            None => 0,
        };
    }

    last
}
// end::play[]

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_init() {
        let content = "0,3,6";
        let (map, last) = init(content);

        let mut exp_map: HashMap<isize, isize> = HashMap::new();
        exp_map.insert(0, 0);
        exp_map.insert(3, 1);

        assert_eq!(map, exp_map);
        assert_eq!(last, 6);
    }

    #[test]
    fn test_play_single() {
        let content = "0,3,6";
        let (mut map, mut last) = init(content);

        last = play(&mut map, last, 3, 4);
        assert_eq!(last, 0);

        last = play(&mut map, last, 4, 5);
        assert_eq!(last, 3);

        last = play(&mut map, last, 5, 6);
        assert_eq!(last, 3);

        last = play(&mut map, last, 6, 7);
        assert_eq!(last, 1);

        last = play(&mut map, last, 7, 8);
        assert_eq!(last, 0);

        last = play(&mut map, last, 8, 9);
        assert_eq!(last, 4);

        last = play(&mut map, last, 9, 10);
        assert_eq!(last, 0);
    }
}
