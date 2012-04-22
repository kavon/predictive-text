###
#   Using a Markov Model
###

import string

# fine tuning variables
STOP_IMPORTANCE = 5                 # 
SENIOR_STATUS = 100                 #  

COMBO_LIMIT = SENIOR_STATUS / 5     # words which appear more than once within this number of words
                                    # are exponentially boosted

COMBO_BOOST = 1.5                   # this ^ (combo streak) is the rate in which to boost a word

LENGTH_PENALTY = 4                  # words of length <= this value are penalized
LENGTH_BOOST = 0.4                  # steepness of boost curve. 0 < boost < 1



class Node:

    def __init__(self, letter):
        self.key = letter           # letter this node represents
        self.passes = 0             # passing observations of this node
        self.stops = 0              # observations of a word that stopped at this node
        self.children = []          # ordered list of children of this node
        self.stopstamp = 0          # "word" timestamp of the last time this node was a stop
        self.combo = 0              # how long of a combo streak this node is currently on.
        self.lengthBonus = 1.0      # function of the length of the word if this is a stop

    # less than function for python's sort function
    def __lt__(self, other):
        return (STOP_IMPORTANCE * self.stops) + self.passes

    # adds an existing child to this node
    def addChild(self, kid):
        self.children.append(kid)
        self.children.sort()

    # returns reference to child matching description, None otherwise
    def findChild(self, description):
        for child in self.children:
            if child.key == description:
                return child
        return None
    
    # return probability of itself in the sequence given the observations of its children?
    def rank(self, currentStamp):
        observationDelta = currentStamp - self.stopstamp
        
        # C-C-C-COMBOBREAKER
        if(observationDelta > COMBO_LIMIT):
            self.stops += self.combo
            self.combo = 0

        hotness = COMBO_BOOST ** self.combo
        ageFactor = decayValue(observationDelta)
        
        return ageFactor * self.lengthBonus * ((hotness * STOP_IMPORTANCE * self.stops) + (self.passes / currentStamp)) 

    # update observation values
    def observe(self, stoppingObs = False, stoppingStamp = -1, depth=1):
        if stoppingObs:

            if self.stops == 0:
                self.lengthBonus = lengthBonus(depth)

            self.stops += 1
            assert stoppingStamp != -1   # if you choose to have True as an argument
                                         # do not forget the stoppingStamp argument also!
            
            # C-C-C-COMBOBREAKER
            if(stoppingStamp - self.stopstamp <= COMBO_LIMIT):
                self.combo += 1
            else:
                self.stops += self.combo
                self.combo = 0

            self.stopstamp = stoppingStamp

        else:
            self.passes += 1

    def validSuffixes(self, stamp):
        # base case, node has no children. so see if it was a stopping node.
        # by definition i believe it would _have_ to be a stopping node but
        # lets check for shits and giggles.
        if(len(self.children) == 0):
            if(self.stops > 0):
                return [ Suffix(self.key, self.rank(stamp)) ] 
            return []

        # inductive case

        # get all the suffixes of this node's child
        suffixes = []
        for node in self.children:
            suffixes.extend(node.validSuffixes(stamp)) 

        # prepend the key of this node to all of them
        for suffix in suffixes:
            suffix.prepend(self.key)

        # if this node itself is a stopping node, add it
        # to the list of possible suffixes
        if(self.stops > 0):
            suffixes.append( Suffix(self.key, self.rank(stamp)) )

        return suffixes

    # debugging method
    def printStats(self):
        print "\nkey=", self.key
        print "passes=", self.passes
        print "stops=", self.stops
        print "# children=", len(self.children)
        print "combo=", self.combo
        print "stopstamp=", self.stopstamp
        print "lengthBonus=", self.lengthBonus
        

# suffix value bundle
class Suffix:
    def __init__(self, chars, val):
        self.key = chars
        self.value = val
    
    def prepend(self, chars):
        # probably trying to prepend the root node, ignore it
        if(chars == None):
            return

        self.key = chars + self.key

    # allows for a list of Suffixes to have sort() called
    # defines the ordering
    def __lt__(self, other):
        return other.value < self.value

    # how to "convert" this object into a string for printing purposes
    def __str__(self):
        return "(" + self.key + ", " + `self.value` + ")"

# returns coefficient to multiply something by to apply a decay of how long ago
# the word was used.
def decayValue(delta):
    return 2.0 ** ( -(delta) / float(SENIOR_STATUS) )

# returns a multiplier bonus/penalty for word length.
def lengthBonus(x):
    if x >= 1 and x <= (LENGTH_PENALTY + 1):
        return ((x - 1) ** 2.0) / (LENGTH_PENALTY ** 2.0)
    elif x > (LENGTH_PENALTY + 1):
        return (x - LENGTH_PENALTY) ** LENGTH_BOOST
    
    return 0.0

class Network:

    def __init__(self):
        self.observations = []                  # stack of observed nodes to simulate recursion
        self.observations.append(Node(None))    # keep root node in stack always
        
        self.currentPrefix = ""

    #reset what's currently being observed
    def clear(self):
        self.currentPrefix = ""
        numToPop = len(self.observations) - 1 # don't pop root node!
        for i in xrange(0, numToPop):
            self.observations.pop()

    def observe(self, char):
        assert len(char) == 1


        # if you find this character in the string of all whitespace characters
        # so, when the char is a whitespace
        if string.find(string.whitespace, char) != -1:
            # pop the last node, and tell it that none of its children were observed because it's the stopping node

            if(len(self.observations) > 1):
                temp = self.observations.pop()
                temp.observe(True, self.observations[0].passes, len(self.observations)) # not -1 here because of root node
                                                                                        # because we popped one off


            # pop the other nodes, and by default they think one of their children was observed
            while(len(self.observations) > 1):
                temp = self.observations.pop()
                temp.observe()

            
            ## XXX be careful of the cases where self.observations == 1 at the beginning of these conditions.
            ##     we would just be observing the root node when nothing was typed. put a boolean somewhere for this?

            # let the root node know we observed a word, but don't pop it
            self.observations[0].observe()
            
            #reset prefix 
            self.currentPrefix = ""

            # pop everything off the observed stack while updating each node's value
        
        elif char == '\b': #backspace
            # there is no need to decrement observations of the popped child
            # because increments are done once the word was completed.
            # unfortunately if you observe a new char and then observe backspaces over and over
            # you'll be adding a bunch of 0 observation nodes to the topmost node for no reason
            # i might add a prune() method to Node which recursively prunes all 0
            # observation nodes to slim down on memory use if we're using a lot
            
            self.observations.pop()

            # pop and discard the value on the stack

        else:

            # find the child of the topmost node on the stack which has a letter value corresponding to
            # the observed letter. if it is found then push that on the stack, otherwise create a new one
            # and then push it on the stack

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
                            


    def suggest(self, num=1):
        # return the best 'num' word(s). default is 1

        possibilities = self.observations[len(self.observations) - 1].validSuffixes(self.observations[0].passes)
        possibilities.sort()

        #cut out extra nodes
        possibilities = possibilities[:num]

        #add prefix to suffixes
        for suffix in possibilities:
            suffix.prepend(self.currentPrefix[:len(self.currentPrefix)-1])

        #filter out the current prefix as a suggestion
        possibilities = [x for x in possibilities if x.key != self.currentPrefix]

        return possibilities





