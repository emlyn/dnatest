#!/usr/bin/env pypy

from itertools import izip
from collections import defaultdict
import string

def distance(k1, k2):
    "Returns the Hamming distance between two strings, assumes they are the same length"
    return sum(c1 != c2 for c1, c2 in izip(k1, k2))

translate_table = string.maketrans("GCATgcat", "CGTAcgta");

def revcomp(s):
    return ''.join(reversed(s.translate(translate_table)))

def kmerswithin(distance, roots, alphabet = "GCAT"):
    "Returns a set of all kmers within hamming distance of any of the roots"
    result = set(roots)
    for _ in xrange(distance):
        temp = set()
        for kmer in result:
            for i in xrange(len(kmer)):
                pref = kmer[:i]
                suff = kmer[i+1:]
                for c in alphabet:
                    temp.add(pref + c + suff)
        result = temp
    #print "Found %d candidates" % len(result)
    return result

def go(text, k, d=0):
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
    # For each candidate kmer
    for pattern in kmerswithin(d, kmers.keys()):
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

def gorc(text, k, d):
    kmers = defaultdict(int)
    for i in xrange(len(text) - k + 1):
        kmer = text[i:i+k]
        for km in kmerswithin(d, [kmer]):
            kmers[km] += 1
            kmers[revcomp(km)] += 1
    maxcount = 0
    maxkmers = []
    for k, n in kmers.iteritems():
        if n > maxcount:
            maxcount = n
            maxkmers = [k]
        elif n == maxcount:
            maxkmers.append(k)
    print ' '.join(maxkmers)


def positions(pattern, genome, dist = 0):
    result = []
    l = len(pattern)
    for pos in xrange(len(genome) - l + 1):
        if distance(genome[pos:pos+l], pattern) <= dist:
            result.append(pos)
    return ' '.join(str(i) for i in result)

def clumps(genome, k, L, t):
    kmers = defaultdict(list)
    for pos in xrange(len(genome) - k + 1):
        kmers[genome[pos:pos+k]].append(pos)
    #print "Found %d kmers" % len(kmers)
    results = []
    for kmer, pos in kmers.iteritems():
        if len(pos) < t: continue
        #print "Checking %s: %s" % (kmer, str(pos))
        for i, v in enumerate(pos[:-t + 1]):
            #print i, v
            if pos[i+t-1] - v <= L:
                results.append(kmer)
                break
    return ' '.join(results)

def skews(genome):
    result = [0]
    skew = 0
    for c in genome:
        if c == 'G':
            skew += 1
        elif c == 'C':
            skew -= 1
        result.append(skew)
    return ' '.join(map(str, result))

def minskews(genome):
    minskew = 0
    result = [0]
    skew = 0
    for i, c in enumerate(genome):
        if c == 'G':
            skew += 1
        elif c == 'C':
            skew -= 1
        if skew < minskew:
            minskew = skew
            result = [i+1]
        elif skew == minskew:
            result.append(i+1)
    return ' '.join(map(str, result))

## 1.1
#go("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4)

## 1.2
#print revcomp("AAAACCCGGT")

##1.3
#print positions("ATAT", "GATATATGCATATACTT")

## 1.4

#print clumps("CGGACTCGACAGATGTGAAGAACGACAATGTGAAGACTCGACACGACAGAGTGAAGAGAAGAGGAAACATTGTAA", 5, 50, 4)

## 1.5

#print skews('GAGCCACCGCGATA')
#print minskews("TAAAGACTGCCGAGAGGCCAACACGAGTGCTAGAACGAGGGGCGTAAACGCGGGTCCGAT")

## 1.6

#print positions("ATTCTGGA",
#                "CGCCCGAATCCAGAACGCATTCCCATATTTCGGGA" +
#                "CCACTGGCCTCCACGGTACGGACGTCAATCAAAT",
#                3)

## 1.7

#go("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1)
# GATG ATGC ATGT

## 1.8

#gorc("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1)
#gorc("TCTCTCCTTGCTTGCGCCCGCTGCCGCCCTCTCCCCTGCTGCCGCGCCCTGCCCTCTGCCCGCCGCTCCGCCTCCTGCCTGCCTGCCTTCCTGCCCTGCGCTCTCTCCCGCCCCTCCCTGCCTGCTTCCCTCCTCTCCCCGCGCTTTCTCTTCCCTTGCGCTTTCTCTCCTCTCTCTCCCGCTTCTTGCCCCTCGCCCCTCTCTCCTCTCCCCTTCT",
#     10, 2)

#go("CTTGCCGGCGCCGATTATACGATCGCGGCCGCTTGCCTTCTTTATAATGCATCGGCGCCGCGATCTTGCTATATACGTACGCTTCGCTTGCATCTTGCGCGCATTACGTACTTATCGATTACTTATCTTCGATGCCGGCCGGCATATGCCGCTTTAGCATCGATCGATCGTACTTTACGCGTATAGCCGCTTCGCTTGCCGTACGCGATGCTAGCATATGCTAGCGCTAATTACTTAT",
#   9, 3)
