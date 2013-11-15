#!/usr/bin/env python

import re

# data was found at http://dragon.bio.purdue.edu/pmotif/
genome = file("data/ecoli.genome").readlines()[1:]
genome = ''.join([line.strip() for line in genome])

pattern = re.compile('CAT.{0,3}CACA')

pos = 0
count = 0
freq = []
for match in pattern.finditer(genome):
    freq.extend([count] * (match.start() - pos)) 
    pos = match.start()
    count += 1
freq.extend([count] * (len(genome) - pos))

window = 1000
thresh = 4
for x in xrange(window, len(freq)):
    n = freq[x] - freq[x-window]
    if n >= thresh:
        print "%d: %d-%d" % (n, x-window, x)

