use std::cmp::min;

// tag::play_round[]
pub fn play_round(list: &mut Vec<Item>, curr: usize) -> usize {
    // get current item
    let curr_next = list[curr].next;

    // get next three items
    let n1 = curr_next;
    let n2 = list[n1].next;
    let n3 = list[n2].next;
    let n3_next = list[n3].next;

    // find destination item
    let mut dest = list[curr].low;
    while dest == n1 || dest == n2 || dest == n3 {
        dest = list[dest].low;
    }
    let dest_next = list[dest].next;

    // update next links
    // [.. curr] [n1 n2 n3] [.. dest] => [.. curr] [.. dest] [n1 n2 n3]
    list[curr].next = n3_next;
    list[dest].next = curr_next;
    list[n3].next = dest_next;

    // update current
    list[curr].next
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
    let mut curr = list[low].next;
    let mut checksum = 0;
    loop {
        checksum = checksum * 10 + list[curr].value;
        curr = list[curr].next;
        if curr == low {
            break;
        }
    }
    checksum
}

pub fn get_checksum_2(list: &[Item], low: usize) -> usize {
    let n1 = list[low].next;
    let n2 = list[n1].next;
    list[n1].value * list[n2].value
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
            assert_eq!(list[k].next, (k + 1) % len);
            assert_eq!(list[list[k].low].value, (list[k].value + len - 2) % len + 1);
        }
    }

    #[test]
    fn test_play_round() {
        let data = vec![3, 8, 9, 1, 2, 5, 4, 6, 7];
        let (mut list, mut head, _low) = Item::from(&data, data.len());
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
            head = play_round(&mut list, head);

            let mut curr = head;
            let mut act = Vec::with_capacity(exp.len());
            loop {
                act.push(list[curr].value);
                curr = list[curr].next;
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
    next: usize,
    low: usize,
    value: usize,
}

impl Item {
    fn new(value: usize) -> Self {
        Item { value, next: 0, low: 0 }
    }

    pub fn from(data: &[usize], len: usize) -> (Vec<Item>, usize, usize) {
        // build list of items
        let mut list: Vec<_> = (0..len)
            .map(|k| if k >= data.len() { k + 1 } else { data[k] })
            .map(|v| Item::new(v)).collect();

        // set next links
        for k in 0..len {
            list[k].next = (k + 1) % len;
        }

        // set low links for tail part, which is sorted
        for k in data.len() + 1..len {
            list[k].low = k - 1;
        }

        // set low links for head part, which is unsorted
        for k in 0..min(len, data.len() + 2) {
            let pos = list.iter().position(|v|
                v.value == if list[k].value == 1 { list.len() } else { list[k].value - 1 })
                .unwrap();
            list[k].low = pos;
        }

        let low = list.iter().position(|v| v.value == 1).unwrap();
        (list, 0, low)
    }
}
// end::item[]
