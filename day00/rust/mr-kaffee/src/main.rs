const FERRIS: &str = r"    _~^~^~_
\) /  o o  \ (/
  '_   ¬   _'
  \ '-----' /";

fn main() {
    println!("This year I became a Rustacian!");
    println!("{}", FERRIS);
}

// tag::test[]
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn expect_ok() {
        println!("This will work\n{}", FERRIS);
    }

    #[should_panic]
    #[test]
    fn expect_fail() {
        panic!("This will panic!");
    }
}
// end::test[]
