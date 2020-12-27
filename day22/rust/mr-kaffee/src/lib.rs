use std::collections::{VecDeque, HashSet};

pub fn parse(content: &str) -> (VecDeque<usize>, VecDeque<usize>) {
    let mut parts = content.split("\n\n");
    let deck0: VecDeque<_> = parts.next()
        .expect("Nothing for first player").lines().skip(1)
        .map(|line| line.parse::<usize>().unwrap()).collect();
    let deck1: VecDeque<_> = parts.next()
        .expect("Nothing for second player").lines().skip(1)
        .map(|line| line.parse::<usize>().unwrap()).collect();
    (deck0, deck1)
}

fn calc_score(deck: &VecDeque<usize>) -> usize {
    deck.iter().enumerate().fold(0, |score, (pos, card)|
        score + (deck.len() - pos) * card)
}

// tag::play_recursive[]
/// Play Recursive Combat
///
/// Returns a tuple of a flag indicating the winning player (true for player 1, false for player
/// two) and the winning player's score
pub fn play_recursive(mut decks: (VecDeque<usize>, VecDeque<usize>)) -> (bool, usize) {
    // holds games played before
    let mut seen = HashSet::new();

    while !decks.0.is_empty() && !decks.1.is_empty() {
        // make sure game does not repeat
        if seen.contains(&decks) {
            return (true, calc_score(&decks.0));
        }
        seen.insert(decks.clone());

        // deal first card
        let a = decks.0.pop_front().unwrap();
        let b = decks.1.pop_front().unwrap();
        let mut a_wins = a > b;

        if a <= decks.0.len() && b <= decks.1.len() {
            // recurse
            a_wins = play_recursive((decks.0.iter().take(a).cloned().collect(),
                                     decks.1.iter().take(b).cloned().collect())).0;
        }

        // winner takes cards
        if a_wins {
            decks.0.push_back(a);
            decks.0.push_back(b);
        } else {
            decks.1.push_back(b);
            decks.1.push_back(a);
        }
    }

    (!decks.0.is_empty(), calc_score(if decks.0.is_empty() { &decks.1 } else { &decks.0 }))
}
// end::play_recursive[]

// tag::play[]
/// Play Combat
///
/// Returns a tuple of a flag indicating the winning player (true for player 1, false for player
/// two) and the winning player's score
pub fn play(mut decks: (VecDeque<usize>, VecDeque<usize>)) -> (bool, usize) {
    while !decks.0.is_empty() && !decks.1.is_empty() {
        let a = decks.0.pop_front().unwrap();
        let b = decks.1.pop_front().unwrap();
        if a > b {
            decks.0.push_back(a);
            decks.0.push_back(b);
        } else {
            decks.1.push_back(b);
            decks.1.push_back(a);
        }
    }

    (!decks.0.is_empty(), calc_score(if decks.0.is_empty() { &decks.1 } else { &decks.0 }))
}
// end::play[]

#[cfg(test)]
mod tests {
    use super::*;

    const CONTENT: &str = "Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10";

    const CONTENT2: &str = "Player 1:
43
19

Player 2:
2
29
14";

    #[test]
    fn test_parse() {
        let (deck1, deck2) = parse(CONTENT);
        assert_eq!(deck1, vec![9usize, 2, 6, 3, 1].iter().cloned().collect::<VecDeque<usize>>());
        assert_eq!(deck2, vec![5usize, 8, 4, 7, 10].iter().cloned().collect::<VecDeque<usize>>());
    }

    #[test]
    fn test_play() {
        let decks = parse(CONTENT);
        let result = play(decks);
        assert_eq!(result, (false, 306));
    }

    #[test]
    fn test_play_recursive_inf() {
        let decks = parse(CONTENT2);
        let (winner, _) = play_recursive(decks);
        assert_eq!(winner, true);
    }

    #[test]
    fn test_play_recursive() {
        let decks = parse(CONTENT);
        let result = play_recursive(decks);
        assert_eq!(result, (false, 291));
    }
}