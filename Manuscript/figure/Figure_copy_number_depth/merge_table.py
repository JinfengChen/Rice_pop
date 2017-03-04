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

#IRIS_313-9996	cornflowerblue	SUWEON_295|IRIS_313-9996|Trop	SUWEON 295	South Korea	Tropical jap	38	0	3
def read_table_anno(infile):  
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'): 
                unit = re.split(r'\t',line)
                data[unit[0]] = '%s\t%s\t%s' %(unit[6], unit[7], unit[8])
    return data

#IRIS_313-10080	0.171380408316164	0.0112440547668	21.3878776142525	8.41939179409	15.2418688693856
def read_table_depth(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'): 
                unit = re.split(r'\t',line)
                data[unit[0]] = '%s\t%s' %(unit[2], unit[4])
    return data



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    #try:
    #    len(args.input) > 0
    #except:
    #    usage()
    #    sys.exit(2)
    
    if not args.output:
        args.output = 'ping_coverage_rice3000_MSU7.matrix'
 
    RelocaTE2 = read_table_anno('rice_line_ALL_3000.anno.landrace.list')
    depth     = read_table_depth('rice_3k_copy_number_depth.txt')
    for strain in sorted(RelocaTE2.keys()):
        if depth.has_key(strain):
            print '%s\t%s\t%s' %(strain, RelocaTE2[strain], depth[strain])

if __name__ == '__main__':
    main()

