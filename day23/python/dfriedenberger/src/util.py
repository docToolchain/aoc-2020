import re
import copy

# tag::play[]

def play(cups,current,count):

  minVal = min(cups.keys())
  maxVal = max(cups.keys())

  #print("minVal",minVal,"maxVal",maxVal)

  for _ in range(count):
    #print("current",current)

    #select
    selected = []
    next = cups[current]
    selected.append(next) #1
    next = cups[next]
    selected.append(next) #2
    next = cups[next]
    selected.append(next) #3
    next = cups[next]

    cups[current] = next  #adjust
    #print("selected",selected)

    #calulate destination
    dest = current
    while dest in selected or dest == current:
        dest = dest - 1
        if dest < minVal: dest = maxVal
    #print("dest",dest)
    
    #insert
    save = cups[dest]
    cups[dest] = selected[0]
    cups[selected[2]] = save

    #next 
    current = cups[current]
  
# end::play[]

  
