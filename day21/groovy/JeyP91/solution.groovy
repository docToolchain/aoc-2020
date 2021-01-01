testPart1()
testPart2()
solve()

static void solve() {
    // tag::splitInput[]
    ArrayList<String> input = Arrays.asList(new File('input.txt').text.split(System.getProperty("line.separator")))
    println("Solution Part 1: " + solvePart1(input))
    println("Solution Part 2: " + solvePart2(input))
    // end::splitInput[]
}

static Long solvePart1(ArrayList<String> input) {
    // tag::solvePart1[]
    TreeMap<String, HashSet> allergensIngredients = getAllergensIngredients(input)
    ArrayList<String> allIngredients = getAllIngredients(input)
    allergensIngredients.values().forEach{
        allIngredients.removeAll(it)
    }
    return allIngredients.size()
    // end::solvePart1[]
}

static String solvePart2(ArrayList<String> input) {
    // tag::solvePart2[]
    TreeMap<String, HashSet> allergensIngredients = getAllergensIngredients(input)
    ArrayList<String> allIngredients = getAllIngredients(input)
    filterAllergensIngredients(allergensIngredients)
    return allergensIngredients.values()
            .collect{it.join(",")}
            .join(",")
    // end::solvePart2[]
}

static HashSet getIngredients(String input) {
    return new HashSet(Arrays.asList(input.split(" \\(")[0].split(" ")))
}

static HashSet getAllergens(String input) {
    return new HashSet(Arrays.asList(input.split(" \\(contains ")[1].replace(")", "").split(", ")))
}

static ArrayList<String> getAllIngredients(ArrayList<String> input) {
    ArrayList<String> allIngredients = new ArrayList<>()
    input.forEach{String food ->
        HashSet ingredients = getIngredients(food)
        allIngredients.addAll(ingredients)
    }
    return allIngredients
}

static TreeMap<String, HashSet> getAllergensIngredients(ArrayList<String> input) {
    TreeMap<String, HashSet> allergensIngredients = new TreeMap<>()
    input.forEach{String food ->
        HashSet ingredients = getIngredients(food)
        HashSet allergens = getAllergens(food)
        allergens.forEach{String allergen ->
            if(!allergensIngredients.containsKey(allergen)) {
                allergensIngredients.put(allergen, ingredients)
            } else {
                allergensIngredients.put(allergen, ingredients.intersect(allergensIngredients.get(allergen)) as HashSet)
            }
        }
    }
    return allergensIngredients
}

static void filterAllergensIngredients(TreeMap<String, HashSet> allergensIngredients) {
    while(!isFinished(allergensIngredients)) {
        allergensIngredients.keySet().forEach{String allergen ->
            if(allergensIngredients.get(allergen).size() == 1) {
                String ingredient = allergensIngredients.get(allergen).first()
                allergensIngredients.values().forEach{HashSet set ->
                    if (set.size() > 1) set.remove(ingredient)
                }
            }
        }
    }
}

static boolean isFinished(TreeMap<String, HashSet> allergensIngredients) {
    boolean finished = true
    allergensIngredients.values().forEach{
        if(it.size() > 1) finished = false
    }
    return finished
}

static void testPart1() {
    ArrayList<String> input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator")))
    HashSet ingredients = getIngredients(input.get(0))
    assert ingredients.size() == 4
    HashSet allergens = getAllergens(input.get(0))
    assert allergens.size() == 2
    assert solvePart1(input) == 5
}

static void testPart2() {
    ArrayList<String> input = Arrays.asList(new File("input_test_1.txt").text.split(System.getProperty("line.separator")))
    assert solvePart2(input) == "mxmxvkd,sqjhc,fvjkl"
}
