#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO

def usage():
    test="name"
    message='''
python make_multi_seq_sum.py Target/nonredundant_pep_union-hits_c90.clstr 


>Cluster 0
0       97nt, >pep-hit146_supercont1.215_1539731_1539826_plus... at +/90.72%
1       11784nt, >pep-hit330_supercont1.518_160977_172759_plus... *
2       121nt, >pep-hit471_supercont1.9_4480841_4480960_minus... at +/94.21%
>Cluster 1
0       9430nt, >pep-hit304_supercont1.44_1925791_1935219_plus... *

    '''
    print message


def readtable(infile):
    data  = defaultdict(lambda : int())
    rept  = defaultdict(lambda : str())
    count = 0
    header= 0
    r = re.compile(r'>Cluster (\d+)')
    rr= re.compile(r'.*>(.*)\.\.\. \*')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if line.startswith(r'>'):
                header = line
                cluster= r.search(header).groups(0)[0] if r.search(header) else 'NA'
                data[cluster] = 0
            else:
                data[cluster] += 1
                if rr.search(line):
                    name = rr.search(line).groups(0)[0]
                    rept[cluster] = name

    ofile = open('%s.sum' %(infile) , 'w')
    for c in sorted(data.keys(), key=int):
        print >> ofile, 'Cluster%s\t%s\t%s' %(c, data[c], rept[c])
    ofile.close()

def main():

    readtable(sys.argv[1])

if __name__ == '__main__':
    main()

