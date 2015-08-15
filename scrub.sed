#map the uppercase letters to lowercase
y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/

#remove any visible non-letter or non-dash characters
s/[^-a-z]/ /g

#remove excess spaces
s/  */ /g
