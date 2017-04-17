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
import urllib2
import subprocess

def usage():
    test="name"
    message='''
python Rice3k_copy_number_depth.py > log 2>&1 &

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 100 --lines %s --interval 120 --resource nodes=1:ppn=1,walltime=200:00:00,mem=10G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#Sample  #Read   Depth   Mapped_Depth    Mapped_rate     Dupli_rate      Insert_median   Map_quality     GC_percent      Coverage_mapped Coverage(1-5X)  BamFile
#nivara_IRGC105327       66904761        8.816764895     8.36437303618   0.948689585783  0.0141527745686 210     43.27    41.26  92.15   92.15%;87.63%;82.68%;77.04%;70.61%      nivara_IRGC105327.bam
def read_table_depth(infile):  
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Sample'): 
                unit = re.split(r'\t',line)
                data[unit[0]] = unit[5]
    return data

#Taxa    Ping_Mean       Ping_Median     Ping_STD
#nivara_IRGC105327       7.5616470044    8.0     3.93064795023
def read_table_ping_estimate(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                strain = re.sub(r'.NM2.mpileup', r'', unit[0])
                data[strain] = '%s' %(unit[1])
    return data

#1	B001	China	Temperate japonica	ERS470219
def read_download_table(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                strain = re.sub(r'IRIS', r'IRIS_', unit[1])
                data[unit[4]] = strain
               
    return data



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-d', '--depth')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    #try:
    #    len(args.input) > 0
    #except:
    #    usage()
    #    sys.exit(2)
    
    if not args.output:
        args.output = re.sub(r'.txt', r'.depth.txt', args.input)
 
    acc2name = read_download_table('rice_line_3000.download.list')
    depth = read_table_depth(args.depth)
    copy  = read_table_ping_estimate(args.input)
    ofile = open(args.output, 'w')
    print >> ofile, 'Taxa\t%s\tCopy_estimate\tGenome_Depth' %(copy['Taxa'])
    for strain in sorted(copy.keys()):
        print strain, acc2name[strain]
        if depth.has_key(acc2name[strain]) and not strain == 'Taxa':
            print >> ofile, '%s\t%s\t%s\t%s' %(acc2name[strain], copy[strain], float(copy[strain])/float(depth[acc2name[strain]]), depth[acc2name[strain]])
    ofile.close()

if __name__ == '__main__':
    main()

