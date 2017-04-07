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

#Taxa	Color	Label	Name	Origin	Group	mPing	Ping	Pong
#B001	blue	Heibiao|B001|Temp	Heibiao	China	Temperate jap	71	1	8
#B002	blue	Sansuijin|B002|Temp	Sansuijin	China	Temperate jap	61	0	4
#B003	blue	Zaoshengbai|B003|Temp	Zaoshengbai	China	Temperate jap	72	1	3
def readtable(infile):
    data = defaultdict(lambda : defaultdict(lambda : int()))
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'): 
                unit = re.split(r'\t',line)
                data[unit[5]]['Total'] += 1
                if int(unit[6]) > 0:
                    data[unit[5]]['mPing'] += 1
                if int(unit[7]) > 0:
                    data[unit[5]]['Ping'] += 1
                if int(unit[8]) > 0:
                    data[unit[5]]['Pong'] += 1
    print 'Group\tTotal\tmPingN\tmPing\tPingN\tPing\tPongN\tPong'
    for group in ["Indica", "Aus/boro", "Basmati/sadri", "Intermediate", "Japonica", "Temperate jap", "Tropical jap"]:
        print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' %(group, data[group]['Total'], data[group]['mPing'], float(data[group]['mPing'])/data[group]['Total'], data[group]['Ping'], float(data[group]['Ping'])/data[group]['Total'], data[group]['Pong'], float(data[group]['Pong'])/data[group]['Total'])
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

