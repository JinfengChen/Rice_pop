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
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#B001    6       0       6       379     378     0       B001    blue    Heibiao|B001|Temp       Heibiao China   Temperate jap
def readtable(infile):
    data = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : int())))
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'): 
                unit = re.split(r'\t',line)
                if unit[0] is not '':
                    #G-type Ping
                    if int(unit[1]) > 1 and int(unit[2]) > 1 and int(unit[3]) == 0:
                        data['ping']['G'][unit[12]] += 1
                    #A-type Ping
                    elif int(unit[1]) > 1 and int(unit[2]) == 0 and int(unit[3]) > 1:
                        data['ping']['A'][unit[12]] += 1
                    #GA-type Ping
                    elif int(unit[1]) > 1 and int(unit[2]) > 1 and int(unit[3]) > 1:
                        data['ping']['GA'][unit[12]] += 1
                    #G-tu[e mPing
                    if int(unit[4]) > 1 and int(unit[5]) > 1 and int(unit[6]) == 0:
                        data['mping']['G'][unit[12]] += 1
                    #A-type mPing
                    elif int(unit[4]) > 1 and int(unit[5]) == 0 and int(unit[6]) > 1:
                        data['mping']['A'][unit[12]] += 1
                    #GA-type mPing
                    elif int(unit[4]) > 1 and int(unit[5]) > 1 and int(unit[6]) > 1:
                        data['mping']['GA'][unit[12]] += 1
    for e in ['ping', 'mping']:
        for pop in sorted(data[e]['G'].keys()):
            print '%s G-type %s strains: %s' %(e, pop, data[e]['G'][pop])
        for pop in sorted(data[e]['A'].keys()):
            print '%s A-type %s strains: %s' %(e, pop, data[e]['A'][pop])
        for pop in sorted(data[e]['GA'].keys()):
            print '%s GA-type %s strains: %s' %(e, pop, data[e]['GA'][pop])
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

    readtable(args.input)

if __name__ == '__main__':
    main()

