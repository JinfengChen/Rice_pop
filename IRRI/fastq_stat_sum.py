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

python fastq_stat_sum.py --input HEG4_temperate_group.fastq.list.fastq.stat

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

#711     IRIS313-8209    Greece  Temperate japonica      ERS468463       anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/ERR/ERR607/ERR607769/ERR607769.sra
def readtable(infile):
    data = defaultdict(lambda : str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                name = re.sub(r'IRIS', r'IRIS_', unit[1])
                dirs = re.split(r'/', unit[5]) 
                acc  = re.sub(r'.sra', r'', dirs[-1])
                data[acc] = name
    return data


#Sample  #Read   Average Total   Depth
#ERR607323_?     5954626 83      494233958       1.32859
def sum_stat(infile, acc2name):
    data = defaultdict(lambda : defaultdict(lambda : float()))
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Sample'): 
                unit = re.split(r'\t',line)
                acc  = re.sub(r'\_\?', r'', unit[0])
                #print acc
                data[acc2name[acc]]['#Read'] += float(unit[1])
                data[acc2name[acc]]['Length'] = float(unit[2])
                data[acc2name[acc]]['Total'] += float(unit[3])
                data[acc2name[acc]]['Depth'] += float(unit[4])
    ofile = open('%s.sum' %(infile), 'w')
    for name in sorted(data.keys()):
        #print name
        print >> ofile, '%s\t%s\t%s\t%s\t%s' %(name, data[name]['#Read'], data[name]['Length'], data[name]['Total'], data[name]['Depth'])
    ofile.close()

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

    acc2name = readtable('rice_line_IRRI_2466.download.list')
    sum_stat(args.input, acc2name) 


if __name__ == '__main__':
    main()

