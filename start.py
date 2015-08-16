#!/usr/bin/env python

# Copyright (C) 2015  Kavon Farvardin (http://kavon.farvard.in)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys                  # allows for processing command line arguments
import fileinput            # allows for processing stdin
import cPickle as pickle    # use cPickle instead of pickle but load it under same name, it's hella fast
from bayesian_network import Network

# find out how many suggestions the user wants, otherwise default to 10
if len(sys.argv) >= 2 and sys.argv[1].isdigit():
    numSuggestions = int(sys.argv[1])
else:
    numSuggestions = 10

# load previous knowlege
try:
    trainingData = open('knowledge.dat', 'rb')

    sys.stdout.write('Loading learned data... ')
    sys.stdout.flush()

    n = pickle.load(trainingData)

    sys.stdout.write('done\n')
    sys.stdout.flush()
except:
    print "No existing training data found. Making new file."
    # file probably didn't exist or some other error, just start fresh.
    trainingData = open('knowledge.dat', 'wb')
    n = Network()

# train from stdin
sys.stdout.write('Processing new data... ')
sys.stdout.flush()

for line in fileinput.input():
    for char in line:
        n.observe(char)
sys.stdout.write('done!\n')
sys.stdout.flush()

# prompt for a prefix to suggest for and make a suggestion
print "Commands:\n \s\t save everything learned\n \e\t exit\n \se\t save then exit\n\n"
sys.stdout.flush()

# turns out that after recieving the ^D from stdin to mark EOF, python on OS X
# and sometimes Linux will close stdin for good. So we're reopening it here.
sys.stdin = open('/dev/tty')

while True:
    
    try:    
        prefix = raw_input('-> ')
    except:
        print
        break

    if prefix == '\s' or prefix == '\se':
        sys.stdout.write('Saving learned data... ')
        sys.stdout.flush()
        
        pickle.dump(n, open('knowledge.dat', 'wb'))

        sys.stdout.write('done\n')
        sys.stdout.flush()

    if prefix == '\e' or prefix == '\se':
        break

    #otherwise make a suggestion based on prefix.
    for char in prefix:
        n.observe(char)
    
    
    for word in n.suggest(numSuggestions):
        print word

    sys.stdout.flush()
    n.clear()   #clear any built up word observation in progress from the prefix
    print       #print a newline

