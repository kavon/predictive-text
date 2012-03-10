###
#   Using a Hidden Markov Model
###

from radix_tree import RadixTree

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


class Network:

    def __init__(self):
        self.root = []              # start empty, we can't account for every character
                                    # initially, and even case matters!
        
        self.observations = []      # stack of observed nodes to simulate recursion

        self.seenWords = RadixTree()


    def observe(self, char):
        if char == ' ':
            # pop everything off the observed stack while updating each node's value
            # and collecting the total probability of that sequence.
            # then insert the word that was observed and its probability into the radix tree
        
        elif char == '\b': #backspace
            # pop and discard the value on the stack

        else:
            

    def suggest(self, num=1):
        # return the best 'num' word(s). default is 1

        infinity = 20 ## XXX temporary, obviously

        prefix = ""
        for node in self.observations
            prefix += node.letter

        possibilities = self.seenWords.search_prefix(prefix, infinity)
        orderedPos = sorted(possibilities, key=lambda item: item[1])

        return orderedPos[:num]





