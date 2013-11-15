#!/usr/bin/env python

from itertools import izip

def distance(k1, k2):
    return sum(c1 != c2 for c1, c2 in izip(k1, k2))

def allkmers(within, root, alphabet="GCAT"):
    if within < 1:
        yield root
    else:
        for kmer in allkmers(within - 1, root, alphabet):
            yield kmer
            for i in xrange(len(kmer)):
                pref = kmer[:i]
                base = kmer[i]
                suff = kmer[i+1:]
                for c in alphabet:
                    if c != base:
                        yield pref + c + suff

def candidates(roots, distance):
    result = set()
    for root in roots:
        for kmer in allkmers(distance, root):
            result.add(kmer)
    return result

def go(text, k, d):
    kmers = {}
    for i in xrange(len(text)-k):
        kmer = text[i:i+k]
        try:
            kmers[kmer] += 1
        except KeyError:
            kmers[kmer] = 1
    maxcount = 0
    maxkmers = []
    print "Calculating candidates"
    c = candidates(kmers.keys(), d)
    print "Found ", len(c)
    for pattern in c:
        count = 0
        for kmer, n in kmers.iteritems():
            if distance(pattern, kmer) <= d:
                count += n
        if count > maxcount:
            maxcount = count
            maxkmers = [pattern]
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
# should get: GCACACAGAC GCGCACACAC
# but get: GCACACAGAC ACACACACAC GCGCACACAC CCCGCACACA
