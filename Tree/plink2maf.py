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
python plink2maf.py --input 3K_coreSNP-v2.1.ped

    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#IRIS_313-15896 IRIS_313-15896 0 0 0 -9 0 0 G G
def convert(infile, output):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r' ',line)
                head = unit[0]
                for i in range(6, len(unit)):
                    
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)
    
    if not args.output:
        args.output = '%s.maf' %(os.path.split(args.input)[-1])
    print args.input, args.output 
    #convert(args.input, args.output)

if __name__ == '__main__':
    main()

