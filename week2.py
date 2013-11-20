#!/usr/bin/env pypy

filepath = "data/RNA_codon_table_1.txt"
table = [l.strip().split() for l in file(filepath).readlines()]
table = {t[0]: t[1] if len(t) > 1 else None for t in table}

def translate(rna):
    protein = ""
    for i in xrange(0, len(rna), 3):
        codon = rna[i:i+3]
        if table[codon]:
            protein += table[codon]
    return protein

## 2.1

print translate("AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA")
