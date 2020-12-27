class AllergenMap
  attr_reader :allergens
  def initialize(list)
    @list = list
    @allergens = Hash.new # allergen -> [[ingredients1], [ingredients2]]
    for line in list
      ingredients, allergens = line.split(" (contains ")
      ingredients = ingredients.split(" ")
      allergens = allergens[0..-2].split(", ")
      for a in allergens
        if @allergens[a].nil?
          @allergens[a] = [ingredients]
        else
          @allergens[a] += [ingredients]
        end
      end
    end
    # reduce the list of possible ingredients by taking those that only occur in all lists
    for k in @allergens.keys
      superset = @allergens[k].flatten
      itemCount = @allergens[k].size
      occursInAllLists = Array.new
      for a in superset.uniq
        if superset.count(a) == itemCount
          occursInAllLists.append(a)
        end
      @allergens[k] = occursInAllLists
      end
    end
    # reduce the list of possible ingredients by picking those that do not overlap with other allergens
    usedIngredients = []
    allergensFound = 0
    while allergensFound < @allergens.size
      sortedKeys = @allergens.keys
      .sort{|a,b| @allergens[a].size > @allergens[b].size ? 1 : -1} # those with least options first
      for k in sortedKeys
        for ix in 0..(@allergens[k].size-1)
          i = @allergens[k][ix]
          if usedIngredients.include?(i)
            @allergens[k].delete_at(ix)
          end
        end
        if @allergens[k].kind_of?(Array) && @allergens[k].size == 1
          @allergens[k] = @allergens[k][0]
          allergensFound += 1
          usedIngredients.append(@allergens[k])
        end
      end
    end
  end
end