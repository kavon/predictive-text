# predictive text #

This proof-of-concept program suggests words as the user is typing based upon what it has learned about what the user has typed recently. It was originally created as a class project.


## usage ##

The makefile has all the things you can do with it in there, but
the main ones are:

To use, at a prompt when in the directory with the Makefile, just issue `make`.
knowledge 
This launches the predictive text program with no new training data. It will try to find a ` knowledge.dat` file in the same directory. If it can't find it will will make a new file and
begin to accept new word prefixes at the prompt.

`make train file=<path-to-file>`

This launches the predictive text program with new training data.
If a knowlege file exists then it will load it into memory. 
Then it will train IN MEMORY and then give you a prompt. This
does not modify the knowledge file. If you want to save this new
trained data with the old one it loaded type `\s` at the prompt.

`make clean`

This deletes the current knowlege file (and compiled python file).


### a sometimes confusing aspect at the prompt ###
What is typed at the prompt is the prefix of a word and the program defines the
end of a word with a space. So if you were to type:

"hello world"

with no space after "world" and hit enter, then "hello" is "trained" on and it gives
suggestions for words that begin with "world". If you were to instead give it

"hello world "

Then it will train on both words and by default spit out the top suggestions for an
empty prefix.