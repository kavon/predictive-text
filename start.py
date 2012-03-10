#!/usr/bin/env python

from radix_tree import RadixTree

## testing radix tree

rt = RadixTree()

rt.insert("apple", ("apple", 0.2))
rt.insert("appleshack", ("appleshack", 0.5))
rt.insert("appleshackcream", ("appleshack", 0.6))
rt.insert("applepie", ("applepie", 0.3))
rt.insert("ape", ("ape", 0.1))

# an update to a key's value means you just insert it again
rt.insert("apple", ("apple", 0.9))
rt.insert("?wat", ("?wat", 0.42))


print "value of apple", rt.find("apple")
print "value of applepie", rt.find("applepie")

print "given prefix 'app', the best unambiguous completion is:", rt.complete("app")

print "words I know given '?':"

for word in rt.search_prefix("?", 10):
    print word

print "have you seen 'ducks'?", rt.contains("ducks")





