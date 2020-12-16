use itertools::Itertools;

// tag::solve_with_while[]
/// Return the product on the combination of `n` numbers in list that sum up to 2020.
///
/// The solution uses a while loop which updates indices for all elements of the combination.
///
/// # Examples
///
/// ```
/// let list: Vec<i32> = vec![1721, 979, 366, 299, 675, 1456];
/// let prod2 = mr_kaffee_2020_01::solve_with_while(&list, 2);
/// assert_eq!(prod2, 514_579);
/// let prod3 = mr_kaffee_2020_01::solve_with_while(&list, 3);
/// assert_eq!(prod3, 241_861_950);
/// ```
pub fn solve_with_while(list: &[i32], n: usize) -> i32 {
    let mut indices: Vec<usize> = (0..n).collect();
    while indices[n - 1] <= list.len() {
        // if sum matches, return product
        if indices.iter().fold(0, |sum, idx| sum + list[*idx]) == 2020 {
            return indices.iter().fold(1, |prod, idx| prod * list[*idx]);
        }

        // update indices
        let mut i = 0;
        // find first index which can be incremented
        while i < indices.len() - 1 && indices[i] == indices[i + 1] - 1 {
            i += 1;
        }
        // increment index
        indices[i] += 1;
        // reset all lower indices
        for j in 0..i {
            indices[j] = j;
        }
    }

    panic!("Nothing found.");
}
// end::solve_with_while[]

// tag::solve_with_itertools[]
/// Return the product on the combination of `n` numbers in list that sum up to 2020.
///
/// The solution uses itertools::combinations to iterate through the combinations.
///
/// # Examples
///
/// ```
/// let list: Vec<i32> = vec![1721, 979, 366, 299, 675, 1456];
/// let prod2 = mr_kaffee_2020_01::solve_with_itertools(&list, 2);
/// assert_eq!(prod2, 514_579);
/// let prod3 = mr_kaffee_2020_01::solve_with_itertools(&list, 3);
/// assert_eq!(prod3, 241_861_950);
/// ```
pub fn solve_with_itertools(list: &[i32], n: usize) -> i32 {
    list.iter().combinations(n)
        .find(|v| v.iter().map(|a| *a).sum::<i32>() == 2020)
        .expect("Nothing found").into_iter()
        .product()
}
// end::solve_with_itertools[]

// tag::solve_n2[]
/// Return the product of the two numbers in list that sum up to 2020.
///
/// # Examples
///
/// ```
/// let list: Vec<i32> = vec![1721, 979, 366, 299, 675, 1456];
/// let prod = mr_kaffee_2020_01::solve_n2(&list);
/// assert_eq!(prod, 514_579);
/// ```
pub fn solve_n2(list: &[i32]) -> i32 {
    let (a, b) = list.iter().tuple_combinations()
        .find(|(a, b)| *a + *b == 2020)
        .expect("Nothing found.");

    a * b
}
// end::solve_n2[]

// tag::solve_n3[]
/// Return the product of the three numbers in list that sum up to 2020.
///
/// # Examples
///
/// ```
/// let list: Vec<i32> = vec![1721, 979, 366, 299, 675, 1456];
/// let prod = mr_kaffee_2020_01::solve_n3(&list);
/// assert_eq!(prod, 241_861_950);
/// ```
pub fn solve_n3(list: &[i32]) -> i32 {
    let (a, b, c) = list.iter().tuple_combinations()
        .find(|(a, b, c)| *a + *b + *c == 2020)
        .expect("Nothing found");

    a * b * c
}
// end::solve_n3[]
