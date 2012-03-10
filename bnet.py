###
#   Using a Hidden Markov Model
###

class Node:

    def __init__(self, key):
        self.letter = key           # letter this node represents
        self.obs = 0                # observations of this node
        self.children = []          # ordered list of children of this node
        self.childObs = 0           # total number of observations the children have had
        self.longestPath = None     # child leading to the longest observed string of nodes

    # Less than method used by list.sort() to keep nodes sorted.
    # Sorts by number of observations
    def __lt__(self, other):
        return self.obs < other.obs

    def addChild(self, kid):
        self.childObs += kid.obs
        self.children.append(kid)
        self.children.sort()

    # have node check itself out in the mirror
    # kind of useless at the moment lol
    def observe(self):
        self.obs += 1


class Network:
    def __init__(self):
        # make 26 nodes etc

    def observe(letter):
        # recursive?

