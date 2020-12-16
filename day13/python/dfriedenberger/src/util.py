

# tag::Schedule[]
class Schedule():

    def loadFromFile(self, filename):
        """Read file to map"""
        file = open(filename, "r")
        lines = file.readlines() 
        file.close()
        self.arival = int(lines[0])
        self.busses = lines[1].split(',')
        return

    
    def getNextDepartment(self):
        department = None
        for bus in self.busses:
            if bus == 'x': continue;
            nr = int(bus)
            cnt = int(self.arival / nr)
            last = cnt * nr
            if last != self.arival:
                next = last + nr;
           
            if department == None or next < department["time"]:
                department = { "bus": nr , "time" : next};
            
        return department

  


# tag::Schedule[]
