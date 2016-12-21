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
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource nodes=1:ppn=12,walltime=100:00:00,mem=20G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#Taxa    Color   Label   Name    Origin  Group   mPing   Ping    Pong
#B001    blue    Heibiao|B001|Temp       Heibiao China   Temperate jap   71      1       8
#B002    blue    Sansuijin|B002|Temp     Sansuijin       China   Temperate jap   61      0       4
def prepare_plot_table(ping_s, infile):
    data = defaultdict(str)
    print 'Taxa\tmPing\tPing\tPong\tCode'
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'):
                unit = re.split(r'\t',line)
                if ping_s.has_key(unit[0]) and int(unit[7]) == 1:
                    print '%s\t%s\t%s\t%s\t1' %(unit[0], unit[6], unit[7], unit[8])
                elif ping_s.has_key(unit[0]) and int(unit[7]) > 1:
                    print '%s\t%s\t%s\t%s\t2' %(unit[0], unit[6], unit[7], unit[8])
                elif int(unit[7]) == 1:
                    print '%s\t%s\t%s\t%s\t3' %(unit[0], unit[6], unit[7], unit[8])
                elif int(unit[7]) > 1:
                    print '%s\t%s\t%s\t%s\t4' %(unit[0], unit[6], unit[7], unit[8])
                elif int(unit[7]) == 0:
                    print '%s\t%s\t%s\t%s\t5' %(unit[0], unit[6], unit[7], unit[8])
    return data

#B160
#B235
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

    ping_s = readtable('special_ping.list')
    prepare_plot_table(ping_s, args.input)

if __name__ == '__main__':
    main()

