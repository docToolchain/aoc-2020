use std::collections::{HashMap, HashSet};

/// parse content in a vector of tuples (ingredients, allergens)
pub fn parse(content: &str) -> Vec<(HashSet<&str>, HashSet<&str>)> {
    content.lines().map(|line| {
        let mut parts = line.split(" (contains ");
        let ingredients: HashSet<_> = parts.next().expect("No ingredients")
            .split(" ").collect();
        let allergens: HashSet<_> = parts.next()
            .map(|part| part[..part.len() - 1].split(", ").collect())
            .unwrap_or(HashSet::new());
        (ingredients, allergens)
    }).collect()
}

// tag::build_allergen_map[]
/// Constructs a map with all allergens as keys and sets of candidate ingredients as values
pub fn build_allergen_map<'a>(foods: &[(HashSet<&'a str>, HashSet<&'a str>)])
                              -> HashMap<&'a str, HashSet<&'a str>> {
    let mut allergen_map: HashMap<&str, HashSet<&str>> = HashMap::new();
    for (ingredients, allergens) in foods {
        for allergen in allergens {
            if let Some(candidates) = allergen_map.get_mut(allergen) {
                candidates.retain(|c| ingredients.contains(c));
            } else {
                let candidates: HashSet<_> =
                    ingredients.iter().map(|v| *v).collect();
                allergen_map.insert(allergen, candidates);
            }
        }
    }

    allergen_map
}
// end::build_allergen_map[]

// tag::count_without_allergens[]
/// Count ingredients without allergens
pub fn count_without_allergens(foods: &[(HashSet<&str>, HashSet<&str>)],
                               allergen_map: &HashMap<&str, HashSet<&str>>) -> usize {
    let mut with_allergens: HashSet<&str> = HashSet::new();
    allergen_map.iter().for_each(|(_, ingredients)|
        with_allergens.extend(ingredients.iter()));

    foods.iter().map(|(ingredients, _)| ingredients.iter()
        .filter(|ingredient| !with_allergens.contains(*ingredient))
        .count()).sum()
}
// end::count_without_allergens[]

// tag::reduce_allergen_map[]
/// Reduce the map allergen -> ingredient candidates to a map allergen -> ingredient
pub fn reduce_allergen_map<'a>(mut map: HashMap<&'a str, HashSet<&'a str>>)
                               -> HashMap<&'a str, &'a str> {
    let mut reduced: HashMap<&str, &str> = HashMap::new();

    let mut changed = true;
    while changed {
        changed = false;

        for (allergen, ingredients) in &mut map {
            for (_, ingredient) in &reduced {
                ingredients.remove(ingredient);
            }
            if ingredients.len() == 1 {
                reduced.insert(allergen, ingredients.iter().next().unwrap());
                changed = true;
            } else if ingredients.len() == 0 {
                panic!(format!("No remaining ingredients for {}", allergen));
            }
        }

        map.retain(|allergen, _| !reduced.contains_key(allergen));
    }

    // everything from map should be consumed
    assert_eq!(map.len(), 0);

    reduced
}
// end::reduce_allergen_map[]

// tag::assemble_list[]
/// Build the _canonical dangerous ingredient list_
pub fn assemble_list(map: &HashMap<&str, &str>) -> String {
    let mut flat: Vec<_> = map.iter()
        .map(|(allergen, ingredient)| (*allergen, *ingredient))
        .collect();

    flat.sort_by(|(a, _), (b, _)| a.cmp(b));

    let mut list = flat.iter()
        .fold(String::new(), |mut list, (_, ingredient)| {
            list.extend(ingredient.chars());
            list.push(',');
            list
        });
    // remove trailing ','
    list.truncate(list.len() - 1);

    list
}
// end::assemble_list[]

#[cfg(test)]
mod tests {
    const CONTENT: &str = "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)";

    use super::*;

    #[test]
    fn test_count_without_allergens() {
        let foods = parse(CONTENT);
        let map = build_allergen_map(&foods);
        let cnt = count_without_allergens(&foods, &map);
        assert_eq!(cnt, 5);
    }

    #[test]
    fn test_build_allergen_map() {
        let foods = parse(CONTENT);
        let map = build_allergen_map(&foods);
        assert!(map.get("dairy").unwrap().contains("mxmxvkd"));
        assert!(map.get("fish").unwrap().contains("sqjhc"));
        assert!(map.get("soy").unwrap().contains("fvjkl"));
    }

    #[test]
    fn test_reduce_allergen_map() {
        let foods = parse(CONTENT);
        let map = build_allergen_map(&foods);
        let map = reduce_allergen_map(map);
        let mut exp_map = HashMap::new();
        exp_map.insert("dairy", "mxmxvkd");
        exp_map.insert("fish", "sqjhc");
        exp_map.insert("soy", "fvjkl");
        assert_eq!(map, exp_map);
    }

    #[test]
    fn test_assemble_list() {
        let foods = parse(CONTENT);
        let map = build_allergen_map(&foods);
        let map = reduce_allergen_map(map);
        let list = assemble_list(&map);
        assert_eq!(list, String::from("mxmxvkd,sqjhc,fvjkl"));
    }

    #[test]
    fn test_parse() {
        let foods = parse(CONTENT);
        assert_eq!(foods, vec![
            (vec!["mxmxvkd", "kfcds", "sqjhc", "nhms"].into_iter().collect::<HashSet<_>>(),
             vec!["dairy", "fish"].into_iter().collect::<HashSet<_>>()),
            (vec!["trh", "fvjkl", "sbzzf", "mxmxvkd"].into_iter().collect::<HashSet<_>>(),
             vec!["dairy"].into_iter().collect::<HashSet<_>>()),
            (vec!["sqjhc", "fvjkl"].into_iter().collect::<HashSet<_>>(),
             vec!["soy"].into_iter().collect::<HashSet<_>>()),
            (vec!["sqjhc", "mxmxvkd", "sbzzf"].into_iter().collect::<HashSet<_>>(),
             vec!["fish"].into_iter().collect::<HashSet<_>>()),
        ]);
    }
}