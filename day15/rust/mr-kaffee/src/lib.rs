use std::collections::HashMap;

// tag::init[]
/// Initialize map for memory game
///
/// The input is expected to be a comma separated list of integers
/// The function returns a map where the values in the input list are the keys and their position's
/// in the input list are their values. The last value is not in the map but returned in addition to
/// the map. The third return value is the number of the round to start playing on this map.
///
/// # Panics
///
/// This function panics if the input list is not a comma separated list of distinct integer values
pub fn init(line: &str) -> (HashMap<isize, isize>, isize, isize) {
    let mut last = 0;

    let mut map: HashMap<_, _> = String::from(line).split(",")
        .map(|v| v.parse::<isize>().expect("Could not parse number"))
        .enumerate()
        .map(|(pos, value)| {
            last = value;
            (value, pos as isize)
        }).collect();

    let start = map.remove(&last).unwrap() + 1;

    assert_eq!(start as usize, map.len() + 1, "Initialization from non-unique numbers not allowed.");

    (map, last, start)
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
/// let (mut map, last, start) = mr_kaffee_2020_15::init("0,3,6");
/// let last = mr_kaffee_2020_15::play(&mut map, last, start, 7);
/// assert_eq!(last, 1);
/// let last = mr_kaffee_2020_15::play(&mut map, last, 7, 10);
/// assert_eq!(last, 0);
/// ```
pub fn play(map: &mut HashMap<isize, isize>, last: isize, start: isize, end: isize) -> isize {
    (start - 1..end - 1).fold(last, |last, turn|
        turn - map.insert(last, turn).unwrap_or(turn))
}
// end::play[]

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_init() {
        let content = "0,3,6";
        let (map, last, start) = init(content);

        let mut exp_map: HashMap<isize, isize> = HashMap::new();
        exp_map.insert(0, 0);
        exp_map.insert(3, 1);

        assert_eq!(map, exp_map);
        assert_eq!(last, 6);
        assert_eq!(start, 3);
    }

    #[test]
    fn test_play_single() {
        let content = "0,3,6";
        let (mut map, mut last, mut start) = init(content);

        last = play(&mut map, last, start, start + 1);
        assert_eq!(last, 0);
        start += 1;

        last = play(&mut map, last, start, start + 1);
        assert_eq!(last, 3);
        start += 1;

        last = play(&mut map, last, start, start + 1);
        assert_eq!(last, 3);
        start += 1;

        last = play(&mut map, last, start, start + 1);
        assert_eq!(last, 1);
        start += 1;

        last = play(&mut map, last, start, start + 1);
        assert_eq!(last, 0);
        start += 1;

        last = play(&mut map, last, start, start + 1);
        assert_eq!(last, 4);
        start += 1;

        last = play(&mut map, last, start, start + 1);
        assert_eq!(last, 0);
    }
}
