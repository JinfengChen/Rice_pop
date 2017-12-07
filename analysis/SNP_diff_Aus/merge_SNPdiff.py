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
python CircosConf.py --input circos.config --output pipe.conf

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource nodes=1:ppn=12,walltime=100:00:00,mem=20G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#IRIS_313-10057:IRIS_313-10059   9978    1229    8749    6959    1790
#IRIS_313-10057:IRIS_313-10092   14826   1219    13607   6876    6731
def readtable(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                pairs= sorted(re.split(r':', unit[0]))
                pair = '%s:%s' %(pairs[0], pairs[1])
                data[pair] = map(int, unit[1:6])
    return data

#IRIS_313-10057  IRIS_313-10059  20      187     12
def read_te_diff(infile):
    data = defaultdict(lambda : list())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                pair = '%s:%s' %(unit[0], unit[1])
                data[pair] = unit[2:5]
    return data




def main():
    prefix = 'NB_final_snp.aus_group'
    #te_diff      = read_te_diff('../../IRRI/HEG4_group_RelocaTEi.TEdiff')
    sum_snp_diff = defaultdict(lambda : list())
    for i in range(1,13):
        snpdiff = '%s.%s.vcf.SNPdiff' %(prefix, i)
        diff = readtable(snpdiff)
        for pair in diff.keys():
            if sum_snp_diff.has_key(pair):
                for j in range(5):
                    #print j, sum_snp_diff[pair], diff[pair]
                    sum_snp_diff[pair][j] += int(diff[pair][j])
            else:
                sum_snp_diff[pair].extend(diff[pair])
    ofile = open('%s.SNPdiff' %(prefix), 'w') 
    for pair in sorted(sum_snp_diff.keys()):
        #if te_diff.has_key(pair):
        print >> ofile, '%s\t%s' %(pair, '\t'.join(map(str, sum_snp_diff[pair])))
    ofile.close()

if __name__ == '__main__':
    main()

