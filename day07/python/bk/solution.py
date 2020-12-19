from utils import *

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
        self.__rootBags=[]
        self.__parse()        
    def __parse(self):
        for d in data:
            splittedBags=d.split("contain")
            containingColors=self.__parseContainingColors(splittedBags[1])
            rootBag=self.__parseRootBag(splittedBags[0])
            rootBag.containingColors=containingColors
            self.__rootBags.append(rootBag)
        for rootBag in self.__rootBags:
            for color in rootBag.containingColors:
                bag=self.__getBagByColor(color)
                if bag != None and self.__containsBag(rootBag, bag) == False:
                    rootBag.containingBags.append(bag)
    def __getBagByColor(self, color):
        bags = [bag for bag in self.__rootBags if bag.color==color]
        if len(bags) == 0:
            return None
        return bags[0]
    def __containsBag(self, rootBag, bag):
        bags = [x for x in rootBag.containingBags if x.color==bag.color]
        if len(bags) == 0:
            return False
        return True
    def __parseContainingColors(self, value):
        splittedBags=value.split(",")
        colors=[]
        for bagAsString in splittedBags:
            splitted=bagAsString.split()
            color="{} {}".format(splitted[1], splitted[2])
            colors.append(color)
        return colors
    def __parseRootBag(self, value):
        splitted=value.split()
        color="{} {}".format(splitted[0], splitted[1])
        rootBag=Bag()
        rootBag.color=color
        rootBag.isRoot=True
        return rootBag
    def getRootBags(self):
        return self.__rootBags

class BagsSearcher:
    def __init__(self, rootBags):
        self.__rootBags=rootBags
        self.colors=[]
    def searchBagColorsForContainingBag(self, containingBagColor):    
        for rootBag in self.__rootBags:
            if self.__checkIfBagContainsColor(rootBag, containingBagColor) == True:
                self.__addColor(rootBag.color)
    def __checkIfBagContainsColor(self, bag, color):
        found=False
        for containingColor in bag.containingColors:
            if containingColor == color:
                found=True
                break
        if found == False:
            for childBag in bag.containingBags:
                if self.__checkIfBagContainsColor(childBag, color):
                    found = True
                    break
        return found
    def __addColor(self, color):
        if color not in self.colors:
            self.colors.append(color)                   

f=open("input.txt","r")
data=f.readlines()
p=BagParser(data)
s=BagsSearcher(p.getRootBags())
s.searchBagColorsForContainingBag("shiny gold")
print("Answer 1: {}".format(len(s.colors)))