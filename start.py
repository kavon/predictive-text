#!/usr/bin/env python




from bayesian_network import Network

n = Network()


import fileinput
for line in fileinput.input():
    for char in line:
        n.observe(char)

n.observe("a")
#n.observe("o")
#n.observe("b")
#n.observe("b")

for word in n.suggest(20):
    print word



"""
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
"""

