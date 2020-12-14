/// Parse input to earliest timestamp and vector of ids as `Option<i64>`.
///
/// Ids `"x"` result in `None` values, integer ids result in `Some<i64>` values.
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
/// Find earliest departure after timestamp `earliest`
pub fn find_earliest_departure(earliest: i64, ids: &[Option<i64>]) -> (i64, i64) {
    ids.iter()
        .filter_map(|id| id.map(|id| (id, ((earliest + id - 1) / id) * id)))
        .min_by(|(_, a), (_, b)| a.cmp(b))
        .expect("No min found")
}
// end::find_earliest_departure[]

/// Calculate multiplicate inverse of `a` modulo `m`
/// with the [Extended Euclidean Algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)
///
/// The result is in the range `-(m-1)..m` (inclusive lower, exclusive upper bound)
///
/// # Examples
///
/// ```
/// let a = 2;
/// let m = 13;
///
/// // the result of `mul_inverse_mod` is in the range -(m-1)..m, normalize by adding `m` to
/// // negative results
/// let a_inv = match mr_kaffee_2020_13::mul_inverse_mod(a, m) {
///     v if v < 0 => v + m,
///     v => v
/// };
///
/// // `a_inv` and `a` are both positive, remainder and modulo yield the same result
/// assert_eq!((a_inv * a) % m, 1)
/// ```
///
/// # Panics
/// The function panics if `a` and `m` are not co-prime
/// ```should_panic
/// let a = 15;
/// let m = 27;
/// let a_inv = mr_kaffee_2020_13::mul_inverse_mod(a, m);
/// ```
pub fn mul_inverse_mod(a: i64, m: i64) -> i64 {
    // tuples allow for simultaneous update without temporary variables
    let mut t = (0, 1);
    let mut r = (m, a);

    while r.1 != 0 {
        let quotient = r.0 / r.1;

        r = (r.1, r.0 - quotient * r.1);
        t = (t.1, t.0 - quotient * t.1);
    }

    // if GCD != 1, there is no inverse
    if r.0 != 1 {
        panic!(format!("a = {} = {} * {} and m = {} = {} * {} are not co-prime",
                       a, a / r.0, r.0, m, m / r.0, r.0));
    }

    t.0
}

/// a modulo trait
///
/// The generic parameter Value is not strictly needed in this crate since it is only used for i64.
/// But AoC is for learning, right?
trait Modulo {
    type Value;

    fn modulo(self, m: Self::Value) -> Self::Value;
}

/// implementation of the modulo trait for i64
///
/// allows to call the modulo function on any i64 value
impl Modulo for i64 {
    type Value = i64;

    fn modulo(self, m: i64) -> i64 {
        // a % m yields remainder
        // a % m + m > 0 for m > 0
        (self % m + m) % m
    }
}

// tag::find_time[]
/// Find time which satisfied `(t + pos[i]) % id[i] == 0` for all ship ids
///
/// # Algorithm
///
/// The algorithm updates the time `t` for every position `pos[i]` where
/// `id[i] = id[pos[i]] != "x"`, solving equations of the form `(a k + b) % m = 0` for `k` as
/// follows.
///
/// ## Initial Step
///
/// 1. `t[0] = 0`
/// 2. `a[0] = 1`
///
/// ## Loop (`i >= 0`)
///
/// 1. solve `(t[i - 1] + k * a[i - 1] + pos[i]) % id[i] == 0` for `k`
/// 2. `t[i] = t[i - 1] + k * a[i - 1]`
/// 3. `a[i] = id[i - 1] * a[i - 1]`
///
/// ## Solving linear equations with modulo
///
/// The solution of `(a k + b) % m = 0` for `k` generally requires `a` and `m` to be co-prime and
/// is done with a multiplicative inverse `a` modulo `m`. See [`mul_inverse_mod`]
///
/// # Panics
/// if any of the ids are not co-prime
///
pub fn find_time(ids: &[Option<i64>]) -> i64 {
    let (t, ..) = ids.iter().enumerate()
        .filter_map(|(pos, v)| v.map(|v| (pos as i64, v)))
        .fold((0, 1),
              |(t, a), (pos, id)| {
                  let k = (-mul_inverse_mod(a, id) * (t + pos)).modulo(id);
                  (t + k * a, a * id)
              });

    t
}
// end::find_time[]

// tag::find_time_iteratively[]
/// Solution idea of James Hockenberry re-implemented in rust
///
/// Instead of calculating the multiplicative inverse, solves equations
/// `(k a + c) % m = 0` for `k` by linear search.
pub fn find_time_iteratively(ids: &[Option<i64>]) -> i64 {
    let (t, ..) = ids.iter().enumerate()
        .filter_map(|(pos, v)| v.map(|v| (pos as i64, v)))
        .fold((0, 1),
              |(t, a), (pos, id)| {
                  let mut k = 0;
                  while (t + k * a + pos) % id != 0 { k += 1; };
                  (t + k * a, a * id)
              });

    t
}
// end::find_time_iteratively[]

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

    #[test]
    fn test_find_time_iteratively() {
        let ids = bus_ids();
        let t = find_time_iteratively(&ids);
        assert_eq!(t, 1_068_781);
    }
}