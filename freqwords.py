#!/usr/bin/env python

from itertools import izip

def distance(k1, k2):
    "Returns the Hamming distance between two strings, assumes they are the same length"
    return sum(c1 != c2 for c1, c2 in izip(k1, k2))

def kmerswithin(distance, root, alphabet="GCAT"):
    "Returns all kmers within Hamming distance of root, might repeat some"
    if distance < 1:
        yield root
    else:
        for kmer in kmerswithin(distance - 1, root, alphabet):
            yield kmer
            for i in xrange(len(kmer)):
                pref = kmer[:i]
                base = kmer[i]
                suff = kmer[i+1:]
                for c in alphabet:
                    if c != base:
                        yield pref + c + suff

def candidates(roots, distance):
    "Return all kmers within hamming distance of any of the roots, without repeats"
    result = set()
    for root in roots:
        for kmer in kmerswithin(distance, root):
            result.add(kmer)
    return result

def go(text, k, d):
    "Solve the problem"
    # Find counts of all kmers in input sequence
    kmers = {}
    for i in xrange(len(text) - k + 1):
        kmer = text[i:i+k]
        try:
            kmers[kmer] += 1
        except KeyError:
            kmers[kmer] = 1
    # Find candidate kmers within specified distance of input kmers
    maxcount = 0
    maxkmers = []
    print "Calculating candidates"
    c = candidates(kmers.keys(), d)
    print "Found ", len(c)
    # For each candidate kmer
    for pattern in c:
        count = 0
        # Check each input kmer
        for kmer, n in kmers.iteritems():
            # And if it is within the specified distance add to count
            if distance(pattern, kmer) <= d:
                count += n
        # If it is the most frequent so far, record it
        if count > maxcount:
            maxcount = count
            maxkmers = [pattern]
        # Or if it is equally frequent, add it to list
        elif count == maxcount:
            maxkmers.append(pattern)
    print ' '.join(maxkmers)

go("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1)
# GATG ATGC ATGT

go("CACAGTAGGCGCCGGCACACACAGCCCCGGGCCCCGGGCCGCCCCGGGCCGGCGGCCGCCGGCGCCGGCA" +
   "CACCGGCACAGCCGTACCGGCACAGTAGTACCGGCCGGCCGGCACACCGGCACACCGGGTACACACCGGG" +
   "GCGCACACACAGGCGGGCGCCGGGCCCCGGGCCGTACCGGGCCGCCGGCGGCCCACAGGCGCCGGCACAG" +
   "TACCGGCACACACAGTAGCCCACACACAGGCGGGCGGTAGCCGGCGCACACACACACAGTAGGCGCACAG" +
   "CCGCCCACACACACCGGCCGGCCGGCACAGGCGGGCGGGCGCACACACACCGGCACAGTAGTAGGCGGCC" +
   "GGCGCACAGCC", 10, 2)
# GCACACAGAC GCGCACACAC

#go("GCGACAACCCACCCCCGCAGCGACCGACCCTAGACCCGCGACCGCCGTAGGCGAACCCTAGACCCCAGCGACCGCCGGCGACAACCCTAGCAGCGATAGACCCTAGCAGCGACACAGCGAGCGAACCCTAGCCGTAGTAGTAGGCGAACCCTAGTAGCACCGTAGGCGAACCCGCGACACATAGGCGACAACCCCATAGCCGGCGACCGACCCGCGACATAGCAGCGAGCGAACCCCAGCGACACAGCGAGCGATAGTAGTAGCCGCCGCCGTAGTAGCCGGCGATAGCAACCCTAGCCGTAGCCGGCGAACCCCCGGCGACACCGTAGCACCGCAACCCTAGGCGAACCCTAGACCCACCCTAGACCCACCCCCGGCGACCG", 9, 3)
# CCCCAACCC
