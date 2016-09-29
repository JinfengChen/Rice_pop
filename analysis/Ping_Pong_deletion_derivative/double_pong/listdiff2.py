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
python CircosConf.py --input circos.config --output pipe.conf

    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def readtable(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                data["_".join(unit)] = 1
    return data


def main():
    
    list1 = readtable(sys.argv[1])
    list2 = readtable(sys.argv[2])
    count = [0, 0, 0]
    for ril in sorted(list1.keys()):
        if not list2.has_key(ril):
            print 'Only in list1: %s' %(ril)
            count[0] += 1
        else:
            print 'Shared: %s' %(ril)
            count[1] += 1

    for ril in sorted(list2.keys()):
        if not list1.has_key(ril):
            print 'Only in list2: %s' %(ril)
            count[2] += 1
            #print ril

    print 'File1 %s only: %s' %(sys.argv[1], count[0])
    print 'File2 %s only: %s' %(sys.argv[2], count[2])
    print 'Shared: %s' %(count[1])


if __name__ == '__main__':
    main()

