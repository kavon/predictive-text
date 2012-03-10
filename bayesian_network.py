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

        #might remove this
        self.longestPath = None     # child leading to the longest observed string of nodes

    # Less than method used by list.sort() to keep nodes sorted.
    # Sorts by number of observations
    def __lt__(self, other):
        return self.obs < other.obs

    def addChild(self, kid):
        self.childObs += kid.obs
        self.children.append(kid)
        self.children.sort()

    # returns reference to child matching description, None otherwise
    def findChild(self, description):
        for child in self.children:
            if child.letter == description:
                return child
        return None
    
    # return probability of itself in the sequence given the observations of its children?
    def probability(self):

    # update observation values
    def observe(self, childWasObserved=True):
        

class Network:

    def __init__(self):
        
        """ I don't think we need a root node variable """

        #self.rootNode = Node(None)              # start empty, we can't account for every character
                                                 # initially, and even case matters!
        
        self.observations = []                  # stack of observed nodes to simulate recursion
        self.observations.append(Node(None))    # keep root node in stack always
        
        self.currentPrefix = ''
        
        self.seenWords = RadixTree()


    def observe(self, char):
        assert len(char) == 1

        # if you find this character in the string of all whitespace characters
        # so, when the char is a whitespace
        if string.find(string.whitespace, char) != -1:
            # pop the last node, and tell it that none of its children were observed
            # and collect its probability

            if(self.observations > 1):
                temp = self.observations.pop()
                temp.observe(False)


            # pop the other nodes, and by default they think one of their children was observed
            while(self.observations > 1):
                temp = self.observations.pop()
                temp.observe()

            # let the root node know we observed a word, but don't pop it
                self.observations[0].observe()
            

            # pop everything off the observed stack while updating each node's value

            # and collecting the total probability of that sequence.
            # then insert the word that was observed and its probability into the radix tree
        
        elif char == '\b': #backspace
            # there is no need to decrement observations of the popped child
            # because increments are done once the word was completed.
            # unfortunately if you observe a new char and then observe backspaces over and over
            # you'll be adding a bunch of 0 observation nodes to the topmost node for no reason
            # i might add a prune() method to Node which recursively prunes all 0
            # observation nodes to slim down on memory use if we're using a lot
            
            self.observations.pop()

            """ done """
            # pop and discard the value on the stack

        else:

            # update current observed prefix for a word
            self.currentPrefix += char

            # grab the top node. if we're starting at the beginning of a new word it would be the root node
            topNode = self.observations[len(self.observations) - 1] # choose from children of node on top of stack
            
            result = topNode.findChild(char)
            
            # if the node doesn't have this child
            if(result == None):
                result = Node(char)
                topNode.addChild(result)
            
            self.observations.append(result)
                            

            """ looks done to me """
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





