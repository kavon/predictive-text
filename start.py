#!/usr/bin/env python

from radix_tree import RadixTree

## testing radix tree
"""
rt = RadixTree()

rt.insert("apple", ("apple", 0.2))
rt.insert("appleshack", ("appleshack", 0.5))
rt.insert("appleshackcream", ("appleshackcream", 0.6))
rt.insert("applepie", ("applepie", 0.3))
rt.insert("ape", ("ape", 0.1))

# an update to a key's value means you just insert it again
rt.insert("apple", ("apple", 0.9))
rt.insert("?wat", ("?wat", 0.42))


print "value of apple", rt.find("apple")
print "value of applepie", rt.find("applepie")

print "given prefix 'app', the best unambiguous completion is:", rt.complete("app")

print "words I know given 'apples':"

for word in rt.search_prefix("apples", 10):
    print word

print "have you seen 'ducks'?", rt.contains("ducks")
"""



from bayesian_network import Network

n = Network()

for i in range(0, 10):
    n.observe("r")
    n.observe("a")
    n.observe("c")
    n.observe("k")
    n.observe(" ")

for i in range(0, 15):
    n.observe("r")
    n.observe("a")
    n.observe("c")
    n.observe("q")
    n.observe("u")
    n.observe("e")
    n.observe("t")
    n.observe(" ")

for i in range(0, 1):
    n.observe("c")
    n.observe("i")
    n.observe("t")
    n.observe("y")
    n.observe(" ")

for i in range(0, 1):
    n.observe("p")
    n.observe("h")
    n.observe("o")
    n.observe("n")
    n.observe("e")
    n.observe(" ")

#n.observe("r")
#n.observe("a")

for word in n.suggest(10):
    print word
