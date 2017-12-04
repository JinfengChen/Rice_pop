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
Summary intact and truncated Ping and Pong in pop.

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource nodes=1:ppn=12,walltime=100:00:00,mem=20G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#rice_line_ALL_3000.anno.list
#Taxa    Color   Label   Name    Origin  Group   mPing   Ping    Pong
#B001    blue    Heibiao|B001|Temp       Heibiao China   Temperate jap   71      
def read_anno(infile):
    data =defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                data[unit[0]] = unit[5]
    return data

#IRIS_313-8921.ping.coverage.clean.txt   222     0
def read_ping_id(infile, actin, anno):
    data = []
    outfile = '%s.sum' %(infile)
    ofile = open(outfile, 'w')
    print >> ofile, 'ID\tCovered\tPercent\tActin_Percent\tGroup'
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                id_raw = unit[0]
                id_new = re.sub(r'\.ping\.coverage\.clean\.txt', r'', id_raw)
                covered = 0
                length  = 5339
                for pos in range(1000, 6339):
                    if int(unit[pos]) > 0:
                        covered += 1
                percent = float(covered)/length
                print >> ofile, '%s\t%s\t%s\t%s\t%s' %(id_new, covered, percent, actin[id_new], anno[id_new])
                #print id_new
                #data.append(id_new)
    ofile.close()
    return data

#ERR068679.bam.pong.coverage.clean.txt   0       0
def read_pong_id(infile):
    data = []
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                id_raw = unit[0]
                id_new = re.sub(r'\.bam\.pong\.coverage\.clean\.txt', r'', id_raw)
                covered = 0
                length  = 5164
                for pos in range(1000, 6164):
                    if int(unit[pos]) > 0:
                        covered += 1
                if float(covered)/length >= 0.3:
                    print '%s\t%s\t%s' %(id_new, covered, unit[1])
                #print id_new
                #data.append(id_new)
    return data

#IRIS_313-8921.control.coverage.clean.txt   222     0
def read_control_id(infile):
    data = defaultdict(lambda : float())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                id_raw = unit[0]
                id_new = re.sub(r'\.control\.coverage\.clean\.txt', r'', id_raw)
                covered = 0
                length  = 6999
                for pos in range(1, 6999):
                    if int(unit[pos]) > 0:
                        covered += 1
                data[id_new] = float(covered)/length
                #print id_new
                #data.append(id_new)
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-r', '--repeat')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    if not args.repeat:
        args.repeat = 'ping'
    
    actin = read_control_id('control_coverage_rice3000_MSU7.matrix.header')
    anno  = read_anno('rice_line_ALL_3000.anno.list')

    if args.repeat == 'ping':
        read_ping_id(args.input, actin, anno) 
    elif args.repeat == 'pong':
        read_pong_id(args.input, actin, anno)
    else:
        print 'repeat should be ping or pong'
        sys.exit(0)

if __name__ == '__main__':
    main()

