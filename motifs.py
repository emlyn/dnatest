#!/usr/bin/env python

import re

# data was found at http://dragon.bio.purdue.edu/pmotif/
# read lines into an array, dropping the first line
genome = file("data/ecoli.genome").readlines()[1:]
# strip off newlines and join into a string
genome = ''.join([line.strip() for line in genome])

# the pattern we are searching for
pattern = re.compile('CAT.{0,3}CACA')

pos = 0   # current position in genome
count = 0 # how many times we've seen the pattern so far
freq = [] # cumulative frequency of pattern up to position n in genome
for match in pattern.finditer(genome):
    # fill in cumulative frequency up to next position
    freq.extend([count] * (match.start() - pos))
    pos = match.start()
    count += 1
# finally fill in the cumulative frequency up to the end of the genome
freq.extend([count] * (len(genome) - pos))

window = 1000 # size of window
thresh = 4    # number of occurrences needed of pattern in window
for x in xrange(window, len(freq)):
    n = freq[x] - freq[x-window]
    if n >= thresh:
        print "%d: %d-%d" % (n, x-window, x)
