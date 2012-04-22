# run with no new training data, looking for existing knowlege file
# or it will make an empty one.
run:
	echo ^D | ./start.py

# give it training data from a file
train:
	sed -f scrub.sed < $(file) | ./start.py

# delete knowlege file
clean:
	rm -f knowlege.dat *.pyc
count:
	tr " " "\n" < $(file) | grep -ic $(word)
