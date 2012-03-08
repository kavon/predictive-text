class Node
    def __init__(self, par):
        self.parent = par
        self.children = []
    def addChild(self, x):
        self.children.append(x)
    def prob(self):
        if len(self.children > 0):
            product = 1.0
            for child in self.children
                product = product * child.prob()
            return product
        ## probably should multiply something with
        ## product and return it. and take care of
        ## case of no children.
