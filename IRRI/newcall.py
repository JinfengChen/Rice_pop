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
python newcal.py Japonica_fastq_RelocaTEi_otherJap_mPing01.summary Japonica_fastq_RelocaTEi_otherJap_mPing0.summary

Compare between files and output new call from the first
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def readtable(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if not data.has_key(unit[0]):
                    data[unit[0]] = line
    return data


def main():
    
    list1 = readtable(sys.argv[1])
    list2 = readtable(sys.argv[2])
    for ril in sorted(list1.keys()):
        if not list2.has_key(ril):
            #print 'Only in list1: %s' %(ril)
            print list1[ril]
    #for ril in sorted(list2.keys()):
    #    if not list1.has_key(ril):
    #        print 'Only in list2: %s' %(ril)
    #        #print ril
if __name__ == '__main__':
    main()

