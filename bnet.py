class Node
    def __init__(self):
        self.probTable = [0.0 for i in range(0,26)]
    ## P(self | parent)
    def prob(self, parent):
        return self.probTable[parent]

class Network:
    def __init__(self):
        self.level = []

