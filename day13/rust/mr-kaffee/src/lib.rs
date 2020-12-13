use std::cmp::Ordering;
use itertools::Itertools;

pub fn parse(content: &str) -> (i64, Vec<Option<i64>>) {
    let mut lines = content.lines();

    let earliest = lines.next().expect("No earliest value")
        .parse().expect("Could not parse earliest value");

    let ids_line = String::from(lines.next().expect("No ids"));
    let ids = ids_line.split(",").map(
        |id| match id {
            "x" => None,
            v => Some(v.parse().expect("Could not parse id")),
        }
    ).collect();

    (earliest, ids)
}

// tag::find_earliest_departure[]
pub fn find_earliest_departure(earliest: i64, ids: &[Option<i64>]) -> (i64, i64) {
    ids.iter().filter(|id| id.is_some()).map(|id|
        if let Some(id) = *id {
            (id, ((earliest + id - 1) / id) * id)
        } else {
            panic!("Could not unwrap");
        }
    ).min_by(|a, b|
        if a.1 > b.1 { Ordering::Greater } else if a.1 < b.1 { Ordering::Less } else { Ordering::Equal }
    ).expect("No min found")
}
// end::find_earliest_departure[]

/// Calculate multiplicate inverse of a modulo m
/// See https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm: Extended
/// Euclidean algorithm
///
/// # Panics
/// if a and m are not co-prime
pub fn mul_inverse_mod(a: i64, m: i64) -> i64 {
    let mut t = 1i64;
    let mut old_t = 0i64;

    let mut r = a;
    let mut old_r = m;

    let mut quotient: i64;
    let mut temp: i64;

    while r != 0 {
        quotient = old_r / r;

        temp = old_r;
        old_r = r;
        r = temp - quotient * r;

        temp = old_t;
        old_t = t;


        t = temp - quotient * t;
    }

    // s, oldS are not calculated as they are not needed
    // oldS * size + old_t * fac = gcd(size, fac) = old_r
    // modulo size: old_t * fac = old_r % size

    // if GCD != 1, there is no inverse
    if old_r != 1 {
        panic!(format!("a = {} and m = {} are not co-prime (GCD = {})", a, m, old_r));
    }

    old_t
}

// tag::find_time[]
/// Find time which satisfied `(t + off[i]) % id[i] == 0` for all ship ids
///
/// # Algorithm
///
/// The algorithm update the time `t` for every position solving equations of the form
/// `(a k + b) % m = 0` for k which is not an x as follows.
///
/// ## Initial Step
/// ``
///   a[0] = 1
///   k[0] = 0
///   t[0] = 0
/// ``
///
/// ## Loop (i >= 1)
/// ``
///   a[i] = id[i - 1] * a[i - 1]
///   k[i]: solve (t[i - 1] + k[i] * a[i] + pos[i]) % id[i] == 0
///   t[i] = t[i - 1] + k[i] * a[i]
/// ``
///
/// # Panics
/// if any of the ids are not co-prime or the first id is an `x`
///
pub fn find_time(ids: &[Option<i64>]) -> i64 {
    assert!(ids[0].is_some(), "First entry must not be a None value");

    let (t, ..) = ids.iter().enumerate()
        .batching(|it|
            loop {
                return match it.next() {
                    None => None,
                    Some((pos, Some(id))) => Some((pos as i64, *id)),
                    _ => continue
                };
            })
        .skip(1).fold(
        (0, 1, ids[0].unwrap()),
        |(t, a, last_id), (pos, id)| {
            let a = last_id * a;
            let k = ((-mul_inverse_mod(a, id) * (t + pos)) % id + id) % id;
            let t = t + k * a;
            (t, a, id)
        });

    t
}
// end::find_time[]

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "939
7,13,x,x,59,x,31,19";

    fn bus_ids() -> Vec<Option<i64>> {
        vec![
            Some(7),
            Some(13),
            None,
            None,
            Some(59),
            None,
            Some(31),
            Some(19),
        ]
    }

    #[test]
    fn test_parse() {
        let (earliest, ids) = parse(CONTENT);
        assert_eq!(earliest, 939);
        assert_eq!(ids, bus_ids());
    }

    #[test]
    fn test_find_earliest_departure() {
        let earliest = 939;
        let ids = bus_ids();
        let (id, departure) = find_earliest_departure(earliest, &ids);
        assert_eq!(id, 59);
        assert_eq!(departure, 944);
    }

    #[test]
    fn test_find_time() {
        let ids = bus_ids();
        let t = find_time(&ids);
        assert_eq!(t, 1_068_781);
    }
}