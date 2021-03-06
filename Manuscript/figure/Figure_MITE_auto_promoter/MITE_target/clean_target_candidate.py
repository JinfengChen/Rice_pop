#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
import glob
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
sys.path.append('/rhome/cjinfeng/BigData/software/ProgramPython/lib')
from utility import gff_parser, createdir

def usage():
    test="name"
    message='''
Use mPing start and end sequence to clean flanking sequence from fasta
python clean_target_candidate.py --input Target_merge_elements/mPing_target_condidate.fa

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def mping_clean(fastafile):
    s = re.compile(r'(GGCCAGT.*ACTGGCC)', re.IGNORECASE)
    newfile = re.sub(r'.fa', r'.clean.fa', fastafile)
    ofile = open(newfile, 'w')
    old = defaultdict(lambda : int())
    new = defaultdict(lambda : int())
    for record in SeqIO.parse(fastafile,"fasta"):
        mping_raw = str(record.seq)
        old[record.id] = 1
        m = s.search(mping_raw)
        if m:
            new[record.id] = 1
            mping = m.groups(0)[0]
            mping_record = SeqRecord(Seq(mping), id=record.id, name=record.name, description=record.description) 
            SeqIO.write(mping_record, ofile, 'fasta')
    ofile.close()
    #for i in old.keys():
    #    if not new.has_key(i):
    #        print '%s missed' %(i)

def readtable(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if not data.has_key(unit[0]):
                    data[unit[0]] = unit[1]
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

    mping_clean(args.input)

if __name__ == '__main__':
    main()

