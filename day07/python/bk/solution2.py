from utils import *

class CountBag:
    def __init__(self, count, bag):
        self.count=count
        self.bag=bag

class CountColor:
    def __init__(self, count, color):
        self.count=count
        self.color=color

class Bag:
    def __init__(self):
        self.isRoot=False
        self.containingBags=[]
        self.containingColors=[]
        self.color=""
        self.count=0

class BagParser:
    def __init__(self, data):
        self.__data=data
        self.__rootCountBags=[]
        self.__parse()        
    def __parse(self):
        for d in data:
            splittedBags=d.split("contain")
            containingColors=self.__parseContainingColors(splittedBags[1])
            rootCountBag=self.__parseRootBag(splittedBags[0])
            rootCountBag.bag.containingColors=containingColors
            self.__rootCountBags.append(rootCountBag)
        for rootCountBag in self.__rootCountBags:
            for countColor in rootCountBag.bag.containingColors:
                bag=self.__getBagByColor(countColor.color)
                if bag != None and self.__containsBag(rootCountBag, bag) == False:
                    countBag=CountBag(countColor.count, bag)
                    rootCountBag.bag.containingBags.append(countBag)
    def __getBagByColor(self, color):
        childCountBags = [rootCountBag for rootCountBag in self.__rootCountBags if rootCountBag.bag.color==color]
        if len(childCountBags) == 0:
            return None
        return childCountBags[0].bag
    def __containsBag(self, rootBag, bag):
        bags = [x for x in rootBag.bag.containingBags if x.bag.color==bag.color]
        if len(bags) == 0:
            return False
        return True
    def __parseContainingColors(self, value):
        splittedBags=value.split(",")
        colors=[]
        for bagAsString in splittedBags:
            splitted=bagAsString.split()
            color="{} {}".format(splitted[1], splitted[2])
            if splitted[0] != "no":
                countColor=CountColor(int(splitted[0]), color)
                colors.append(countColor)
        return colors
    def __parseRootBag(self, value):
        splitted=value.split()
        color="{} {}".format(splitted[0], splitted[1])
        rootBag=Bag()
        rootBag.color=color
        rootBag.isRoot=True
        countBag=CountBag(1, rootBag)
        return countBag
    def getCountRootBags(self):
        return self.__rootCountBags

class BagsSearcher:
    def __init__(self, countRootBags):
        self.__countRootBags=countRootBags
        self.colors=[]
        self.count=0
    def searchBagColorsForContainingBag(self, containingBagColor):    
        shinyGoldBag = [x for x in self.__countRootBags if x.bag.color==containingBagColor]
        print(shinyGoldBag[0].bag.color)        
        for countBag in shinyGoldBag[0].bag.containingBags:
            self.count+=countBag.count*self.__countBags(countBag)

    def __countBags(self, countBag):
        if len(countBag.bag.containingBags)==0:
            return 1

        count=1
        for innerCountBag in countBag.bag.containingBags:    
            count+=innerCountBag.count*self.__countBags(innerCountBag)
        return count

f=open("input.txt","r")
data=f.readlines()
p=BagParser(data)
s=BagsSearcher(p.getCountRootBags())
s.searchBagColorsForContainingBag("shiny gold")
print("Answer 2: {}".format(s.count))