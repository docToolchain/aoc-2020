pub const SUBJECT: usize = 7;
pub const MOD: usize = 20201227;

/// parse two public keys from two lines of text
pub fn get_public_keys(content: &str) -> (usize, usize) {
    let mut lines = content.lines();
    let key1 = lines.next().unwrap().parse().unwrap();
    let key2 = lines.next().unwrap().parse().unwrap();
    (key1, key2)
}

// tag::solution[]
/// transform: `subject -> (subject^loop_size) % `[`MOD`]
pub fn transform(subject: usize, loop_size: usize) -> usize {
    (0..loop_size).fold(1, |val, _| (val * subject) % MOD)
}

/// find the loop size which transforms the given `subject` to the given `result`
/// this is somehow `(log_subject(result)) % `[`MOD`]
pub fn find_loop_size(subject: usize, result: usize) -> usize {
    let mut cnt = 1;
    let mut val = subject;
    while val != result {
        val = (val * subject) % MOD;
        cnt += 1;
    }
    cnt
}

/// recover encryption key from two public keys
pub fn get_encryption_key(key1: usize, key2: usize) -> usize {
    transform(key1, find_loop_size(7, key2))
}
// end::solution[]

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_transform() {
        assert_eq!(transform(7, 8), 5764801);
        assert_eq!(transform(7, 11), 17807724);
    }

    #[test]
    fn test_find_loop_size() {
        assert_eq!(find_loop_size(7, 5764801), 8);
        assert_eq!(find_loop_size(7, 17807724), 11);
    }

    #[test]
    fn test_get_encryption_key() {
        assert_eq!(get_encryption_key(5764801, 17807724), 14897079);
    }
}