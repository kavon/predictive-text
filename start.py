#!/usr/bin/env python

from bayesian_network import Network

n = Network()


import fileinput
for line in fileinput.input():
    for char in line:
        n.observe(char)

n.observe("c")
n.observe("o")
n.observe("r")
n.observe("r")
n.observe("e")
n.observe("c")
n.observe("t")
n.observe("n")
n.observe("e")
n.observe("s")
n.observe("s")
n.observe(" ")

n.observe("c")
n.observe("o")
n.observe("r")
n.observe("r")
n.observe("e")
n.observe("c")
n.observe("t")
n.observe("n")
n.observe("e")
n.observe("s")
n.observe("s")
n.observe(" ")

n.observe("c")
n.observe("o")
n.observe("r")
n.observe("r")

for word in n.suggest(20):
    print word


