#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
import glob
from Bio import SeqIO
sys.path.append('/rhome/cjinfeng/BigData/software/ProgramPython/lib')
from utility import gff_parser, createdir

def usage():
    test="name"
    message='''
python add_group_color.py --input Rufipogon_57_RelocaTE2.mPing_Ping_Pong.copy.depth.txt --group Rufipogon.group.color.txt

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


#Taxa	Group	Color
#rufipogon_IRGC103824	wild group IIIb	red
#rufipogon_IRGC105705	wild group IIIb	red
#rufipogon_IRGC93183	wild group IIIb	red
def readgroup(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                data[unit[0]] = '%s\t%s' %(unit[1], unit[2])
    return data

#Taxa	mPing_Mean_copy_estimate	Ping_Mean_copy_estimate	Ping_Mean_copy_estimate	Genome_Depth
#rufipogon_IRGC100897	1.99983387602	0.891570511218	4.44351695895	9.64963872748
def readtable(infile, group):
    outfile = '%s.group.txt' %(os.path.splitext(infile)[0])
    ofile = open(outfile, 'w') 
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                print >> ofile, '%s\t%s' %(line, group[unit[0]])
    ofile.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-g', '--group')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    group = readgroup(args.group)
    readtable(args.input, group)

if __name__ == '__main__':
    main()

