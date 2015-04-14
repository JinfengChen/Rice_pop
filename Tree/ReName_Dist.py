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
python ReName_Dist.py --input test.3000.phy.dist --fasta test.3000.fasta

Rename the sample name in dist because phyilp only accept 10 characters for that. We use the right part of sample name
in fasta to replace the sample in dist. Because the rank of fasta and dist is the same, the results are still good.
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(lambda : str())
    count   = 0
    for record in SeqIO.parse(fastafile,"fasta"):
        s_id  = str(record.id).replace(r'IRIS_313-', r'I')
        fastaid[str(count)] = s_id
        #print '%s\t%s\t%s' %(str(count), fastaid[str(count)], s_id)
        count += 1
    return fastaid


def read_dist(infile, id_dict):
    dist_file = '%s.short_id.dist' %(os.path.splitext(infile)[0])
    ofile = open(dist_file, 'w')
    count = 0
    r = re.compile(r'^\w+')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if r.search(line):
                #print line
                unit = re.split(r'\s+', line)
                unit[0] = str(id_dict[str(count)]).ljust(10)
                line = ' '.join(unit)
                print >> ofile, line
                count += 1
            else:
                print >> ofile, line
    ofile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-f', '--fasta')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    id_dict = fasta_id(args.fasta)
    read_dist(args.input, id_dict)

if __name__ == '__main__':
    main()

