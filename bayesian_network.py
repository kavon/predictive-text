###
#   Using a Hidden Markov Model
###

from radix_tree import RadixTree

class Node:

    def __init__(self, letter):
        self.key = letter           # letter this node represents
        self.passes = 0             # passing observations of this node
        self.stops = 0              # observations of a word that stopped at this node
        self.children = []          # ordered list of children of this node
        self.childObs = 0           # total number of observations the children have had
        self.stopstamp = 0          # "word" timestamp of the last time this node was a stop

        # might remove this
        self.longestPath = None     # child leading to the longest observed string of nodes

    # Less than method used by list.sort() to keep nodes sorted.
    # Sorts by number of observations
    def __lt__(self, other):
        return self.probability() < other.probability()

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
    def probability(self, currentStamp):
        stampDelta = currentStamp - self.stopstamp
        totalObs = self.stops * 1.3 + self.passes
        return (totalObs * decayValue(currentStamp - self.stopstamp)) / totalObs

        

    # update observation values
    def observe(self, stoppingObs = False, stoppingStamp = -1):
        if stoppingObs:
            self.stops += 1
            assert stoppingStamp != -1   # if you choose to have True as an argument
                                         # do not forget the stoppingStamp argument also!
            self.stopstamp = stoppingStamp
        else:
            self.passes += 1
            self.childObs += 1

    def validSuffixes(self):
        # base case, node has no children. so see if it was a stopping node
        # by definition i believe it would _have_ to be a stopping node but
        # lets check for shits and giggles.
        if(len(self.children) == 0):
            if(self.stops > 0):
                return [ (self.key, self.probability()) ] 
            return []

        # inductive case
        suffixes = []
        for node in self.children:
            suffixes.extend(validSuffixes(node))

        for suffix in suffixes:
            suffix = self.key + suffix

        if(self.stops > 0):
            suffixes.append( (self.key, self.probability()) )


# returns coefficient to multiply something by to apply a decay of how long ago
# the word was used.
def decayValue(currentTimestamp, lastTimestamp):
    assert currentTimestamp >= lastTimestamp
    return 2 ** ( -(delta) / 100 )

class Network:

    def __init__(self):
        
        """ I don't think we need a root node variable """

        #self.rootNode = Node(None)              # start empty, we can't account for every character
                                                 # initially, and even case matters!
        
        self.observations = []                  # stack of observed nodes to simulate recursion
        self.observations.append(Node(None))    # keep root node in stack always
        
        self.currentPrefix = ""
        
        self.seenWords = RadixTree()


    def observe(self, char):
        assert len(char) == 1

        """

        should also note that the last node on the stack should have its
        stopping observation counter incremented to note how many times a sequence ended
        there (aka, that node now represents a word) and also have that node record the
        "timestamp", aka the number of total word observations (the root node's observations)
        to factor in how many words ago the word was last observed?
        
        Also, would a node's observations equal the sum of the observations of its children?

        """


        # if you find this character in the string of all whitespace characters
        # so, when the char is a whitespace
        if string.find(string.whitespace, char) != -1:

            # pop the last node, and tell it that none of its children were observed because it's the stopping node

            if(self.observations > 1):
                temp = self.observations.pop()
                temp.observe(True, self.observations[0].passes)


            # pop the other nodes, and by default they think one of their children was observed
            while(self.observations > 1):
                temp = self.observations.pop()
                temp.observe()

            # let the root node know we observed a word, but don't pop it
            
            ## XXX be careful of the cases where self.observations == 1 at the beginning of these conditions.
            ##     we would just be observing the root node when nothing was typed. put a boolean somewhere for this?
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

        

        #infinity = 200 # XXX temporary

        #possibilities = self.seenWords.search_prefix(self.currentPrefix, infinity)
        #orderedPos = sorted(possibilities, key=lambda item: item[1])

        return orderedPos[:num]





