import re
import copy




def insert(cups,selected,dest):
    l = len(cups)
    for i in range(l):
        if cups[i] == dest:
            for x in range(3):
                cups.insert(i+x+1,selected[x])
            break


def play(cups):
  current = cups.pop(0)

  #select
  selected = []
  for i in range(3):
        selected.append(cups.pop(0))

  #print("current",current)
  #print("pickup",selected)

  dest = current
  while (dest not in cups):
      dest = dest - 1
      if dest == 0: dest = 9

  insert(cups,selected,dest)
  cups += [current]

def label(cups):
    ix = 1
    s = ["",""]
    for cup in cups:
        if cup == 1: ix = 0; continue
        s[ix] += str(cup)
    return s[0] + s[1]
  
