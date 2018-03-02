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
python Compare_Pop_Assign.py --strain_list core_v0.7.pruneddata.structure.nosex

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

#Taxa	Color	Label	Name	Origin	Group	mPing	Ping	Pong
#B001	blue	Heibiao|B001|Temp	Heibiao	China	Temperate jap	71	1	8
#IRIS_313-10000	ind1B
def read_anno(infile, col):
    data = defaultdict(lambda : str())
    pop  = defaultdict(lambda : int())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa') and not line.startswith(r'Strain'): 
                unit = re.split(r'\t',line)
                data[unit[0]] = unit[int(col-1)]
                pop[unit[int(col-1)]]  = 1
    #for p in sorted(pop.keys()):
    #    print '%s\t%s' %(p, pop[p])
    return data, pop

def read_table(infile):
    data = []
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'): 
                unit = re.split(r'\s+', line)
                data.append(unit)
    return data

def sum_anno(anno):
    pop_sum = defaultdict(lambda : int())
    for s in anno.keys():
        pop_sum[anno[s]] += 1
    return pop_sum

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strain_list')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.strain_list) > 0 
    except:
        usage()
        sys.exit(2)

    meta = defaultdict(lambda : defaultdict(lambda : int()))
    anno1, pop1 = read_anno('core_v0.7.pruneddata3.8.Q.subgroup.assign.txt', 2)
    anno2, pop2 = read_anno('rice_line_ALL_3000.anno.list', 6)
    strains     = read_table(args.strain_list)
    #cluster      = read_table(args.meanQ_list)
    for i in range(len(strains)):
        s  = strains[i][0]
        p1 = anno1[s]
        p2 = anno2[s]
        meta[p1][p2] += 1

    print 'Pop\t%s' %('\t'.join(sorted(pop2)))
    for p1 in sorted(pop1.keys()):
        line = [p1]
        for p2 in sorted(pop2): 
            line.append(meta[p1][p2])
        print '%s' %('\t'.join(map(str, line))) 

if __name__ == '__main__':
    main()

