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
        self.currentPrefix = ''
        self.seenWords = RadixTree()


    def observe(self, char):
        assert len(char) == 1

        # if you find this character in the string of all whitespace characters
        # so, when the char is a whitespace
        if string.find(string.whitespace, char) != -1:
            # pop everything off the observed stack while updating each node's value
            # and collecting the total probability of that sequence.
            # then insert the word that was observed and its probability into the radix tree
        
        elif char == '\b': #backspace
            # pop and discard the value on the stack

        else:
            self.currentPrefix += char
            
            if(len(self.observations) == 0) # stack is empty, first letter of a word
                for node in self.root:      # so let's look for it
                    if(node.letter == char):
                        self.observations.append(node)
                        break
                
                if(len(self.observations) == 0): # we haven't seen this char yet
                    newguy = Node(char)
                    self.root.append(newguy)     # a sort() isn't needed here because appending 0 observation node
                    self.observations.append(newguy)



            # find the child of the topmost node on the stack which has a letter value corresponding to
            # the observed letter. if it is found then push that on the stack, otherwise create a new one
            # and then push it on the stack

    def suggest(self, num=1):
        # return the best 'num' word(s). default is 1

        infinity = 20 ## XXX temporary, obviously

        prefix = ""
        for node in self.observations
            prefix += node.letter

        possibilities = self.seenWords.search_prefix(prefix, infinity)
        orderedPos = sorted(possibilities, key=lambda item: item[1])

        return orderedPos[:num]





