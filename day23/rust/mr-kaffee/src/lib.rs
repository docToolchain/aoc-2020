use std::cell::RefCell;
use std::cmp::min;

// tag::play_round[]
pub fn play_round(list: &[Item], curr: usize) -> usize {
    // get current item
    let curr = &list[curr];
    let curr_next = curr.next.borrow().clone();

    // get next three items
    let n1 = &list[*curr.next.borrow()];
    let n2 = &list[*n1.next.borrow()];
    let n3 = &list[*n2.next.borrow()];
    let n3_next = *n3.next.borrow();

    // find destination item
    let mut dest = *curr.low.borrow();
    while &list[dest] == n1 || &list[dest] == n2 || &list[dest] == n3 {
        dest = *list[dest].low.borrow();
    }
    let dest = &list[dest];
    let dest_next = *dest.next.borrow();

    // update next links
    // [.. curr] [n1 n2 n3] [.. dest] => [.. curr] [.. dest] [n1 n2 n3]
    curr.next.replace(n3_next);
    dest.next.replace(curr_next);
    n3.next.replace(dest_next);

    // update current
    *curr.next.borrow()
}
// end::play_round[]

pub fn play_rounds(data: &[usize], len: usize, rounds: usize) -> (Vec<Item>, usize, usize) {
    let (mut list, mut head, low) = Item::from(data, len);
    for _ in 0..rounds {
        head = play_round(&mut list, head);
    }
    (list, head, low)
}

pub fn get_checksum_1(list: &[Item], low: usize) -> usize {
    let low = &list[low];
    let mut curr = &list[*low.next.borrow()];
    let mut checksum = 0;
    loop {
        checksum = checksum * 10 + curr.value;
        curr = &list[*curr.next.borrow()];
        if curr == low {
            break;
        }
    }
    checksum
}

pub fn get_checksum_2(list: &[Item], low: usize) -> usize {
    let low = &list[low];
    let n1 = &list[*low.next.borrow()];
    let n2 = &list[*n1.next.borrow()];
    n1.value * n2.value
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_item_from() {
        let data = vec![3, 8, 9, 1, 2, 5, 4, 6, 7];
        let len = 20;
        let (list, _head, _low) = Item::from(&data, len);
        for k in 0..len {
            assert_eq!(*list[k].next.borrow(), (k + 1) % len);
            assert_eq!(list[*list[k].low.borrow()].value, (list[k].value + len - 2) % len + 1);
        }
    }

    #[test]
    fn test_play_round() {
        let data = vec![3, 8, 9, 1, 2, 5, 4, 6, 7];
        let (list, mut head, _low) = Item::from(&data, data.len());
        let exp = vec![
            vec![2, 8, 9, 1, 5, 4, 6, 7, 3],
            vec![5, 4, 6, 7, 8, 9, 1, 3, 2],
            vec![8, 9, 1, 3, 4, 6, 7, 2, 5],
            vec![4, 6, 7, 9, 1, 3, 2, 5, 8],
            vec![1, 3, 6, 7, 9, 2, 5, 8, 4],
            vec![9, 3, 6, 7, 2, 5, 8, 4, 1],
            vec![2, 5, 8, 3, 6, 7, 4, 1, 9],
            vec![6, 7, 4, 1, 5, 8, 3, 9, 2],
            vec![5, 7, 4, 1, 8, 3, 9, 2, 6],
            vec![8, 3, 7, 4, 1, 9, 2, 6, 5],
        ];

        for exp in exp {
            head = play_round(&list, head);

            let mut curr = head;
            let mut act = Vec::with_capacity(exp.len());
            loop {
                act.push(list[curr].value);
                curr = *list[curr].next.borrow();
                if curr == head {
                    break;
                }
            }

            assert_eq!(exp, act);
        }
    }

    #[test]
    fn test_get_checksum_1() {
        let data = vec![3, 8, 9, 1, 2, 5, 4, 6, 7];
        let (list, _, low) = play_rounds(&data, data.len(), 10);
        let checksum = get_checksum_1(&list, low);
        assert_eq!(checksum, 92_658_374);
    }
}

// tag::item[]
#[derive(Debug, Eq, PartialEq)]
pub struct Item {
    next: RefCell<usize>,
    low: RefCell<usize>,
    value: usize,
}

impl Item {
    fn new(value: usize) -> Self {
        Item { value, next: RefCell::new(0), low: RefCell::new(0) }
    }

    pub fn from(data: &[usize], len: usize) -> (Vec<Item>, usize, usize) {
        // build list of items
        let list: Vec<_> = (0..len)
            .map(|k| if k >= data.len() { k + 1 } else { data[k] })
            .map(|v| Item::new(v)).collect();

        // set next links
        for k in 0..len {
            list[k].next.replace((k + 1) % len);
        }

        // set low links for tail part, which is sorted
        for k in data.len() + 1..len {
            list[k].low.replace(k - 1);
        }

        // set low links for head part, which is unsorted
        for k in 0..min(len, data.len() + 2) {
            let pos = list.iter().position(|v|
                v.value == if list[k].value == 1 { list.len() } else { list[k].value - 1 })
                .unwrap();
            list[k].low.replace(pos);
        }

        let low = list.iter().position(|v| v.value == 1).unwrap();
        (list, 0, low)
    }
}
// end::item[]
