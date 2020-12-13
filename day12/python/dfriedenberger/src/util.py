import re
import numpy as np


def read_file_to_list(filename):
        """Read file to map"""
        rows = []
        file = open(filename, "r")
        for line in file:
            m = re.search("^([A-Z])([0-9]+)$", line)
            if not m: raise Exception(line)
            rows.append({"type": m.group(1) , "value": int(m.group(2))})
        file.close()
        return rows

# tag::Ship[]
class Ship():

    def __init__(self):
        self.mx = 1
        self.my = 0
        self.x = 0
        self.y = 0

    def rotateRight(self,angle):
        if angle % 90 != 0:
            raise Exception(angle)
        for r in range(0,angle,90):
            if self.mx == 1:
                self.mx = 0
                self.my = -1
                continue;
            if self.my == -1:
                self.mx = -1
                self.my = 0
                continue;
            if self.mx == -1:
                self.mx = 0
                self.my = 1
                continue;
            if self.my == 1:
                self.mx = 1
                self.my = 0
                continue;


    def process(self,command):
        if(command["type"] == "N"): self.y += command["value"]
        if(command["type"] == "S"): self.y -= command["value"]
        if(command["type"] == "E"): self.x += command["value"]
        if(command["type"] == "W"): self.x -= command["value"]
        if(command["type"] == "L"): self.rotateRight(360 - command["value"])
        if(command["type"] == "R"): self.rotateRight(command["value"])
        if(command["type"] == "F"): 
            self.x += self.mx * command["value"]
            self.y += self.my * command["value"]

        return 

    def manhattan(self):
        return abs(self.x) + abs(self.y)
# tag::Ship[]

# tag::ShipV2[]
class ShipV2():

    def __init__(self):
        self.w  = np.array([10  , 1 ])
        self.p = np.array([0  , 0 ])

    def cosinus(self,angle):
        return int(np.cos(np.deg2rad(angle)));

    def sinus(self,angle):
        return int(np.sin(np.deg2rad(angle)));

    # tag::rotate[]
    def rotate(self,angle):
            #https://en.wikipedia.org/wiki/Rotation_of_axes
            A = np.array([[ self.cosinus(angle) , self.sinus(angle)], 
                          [ -1 * self.sinus(angle)   , self.cosinus(angle)]])
            self.w = A.dot(self.w)
            return
           
    # end::rotate[]

    def process(self,command):
        if(command["type"] == "N"): self.w[1] += command["value"]
        if(command["type"] == "S"): self.w[1] -= command["value"]
        if(command["type"] == "E"): self.w[0] += command["value"]
        if(command["type"] == "W"): self.w[0] -= command["value"]
        if(command["type"] == "L"): self.rotate(-1 * command["value"])
        if(command["type"] == "R"): self.rotate(command["value"])
        if(command["type"] == "F"): 
            #move forward to the waypoint a number of times equal to the given value
            self.p += self.w * command["value"]
        return 

    def manhattan(self):
        return abs(self.p[0]) + abs(self.p[1])
# tag::Ship[]