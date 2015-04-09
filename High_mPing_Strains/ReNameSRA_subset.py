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


#temperate.mPing.group.id
def readtable(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if not data.has_key(unit[0]):
                    data[unit[0]] = 1
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

    args.output = '%s.download.list' %(args.input)
    unique_id   = readtable(args.input)
    ofile = open(args.output, 'w')
    #1       IRIS313-15896   Colombia        Indica  ERS467753       anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/ERR/ERR626/ERR626447/ERR626447.sra
    infile = '../GigaScience/rice_line_IRRI_2466.download.list'
    #infile = '../GigaScience/rice_line_CAAS_534.download.list'
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                unit = re.split(r'\t',line)
                if unique_id.has_key(unit[1]):
                    print >> ofile, line
    ofile.close()
if __name__ == '__main__':
    main()

