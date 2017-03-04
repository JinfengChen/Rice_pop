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

#Accession	Bajie	Dasheng	Retro1	RIRE2	RIRE3	Copia2	karma
#ERS467753_RelocaTEi	0	19	6	72	81	6	0	IRIS313-15896	Colombia	Indica
#ERS467754_RelocaTEi	1	11	8	76	99	2	0	IRIS313-15897	China	Indica
#ERS467755_RelocaTEi	0	16	3	83	91	3	0	IRIS313-15898	Philippines	Indica
def read_TE_table(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and line.startswith(r'ERS'): 
                unit = re.split(r'\t',line)
                unit[8] = re.sub(r'IRIS', r'IRIS_', unit[8])
                data[unit[8]] = unit[2:8]
                #print unit[8]
                #print data[unit[8]]
    return data



#Taxa	Color	Label	Name	Origin	Group	mPing	Ping	Pong
#B001	blue	Heibiao|B001|Temp	Heibiao	China	Temperate jap	71	1	8
#B002	blue	Sansuijin|B002|Temp	Sansuijin	China	Temperate jap	61	0	4
#B003	blue	Zaoshengbai|B003|Temp	Zaoshengbai	China	Temperate jap	72	1	3
def convert_table(infile, TE_table):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and line.startswith(r'Taxa'): 
                unit = re.split(r'\t',line)
                unit = unit[0:7]
                unit.extend(['nDart','Gaijin','spmlike','Truncator','mGing','nDaiz'])
                print '\t'.join(unit)
            elif len(line) > 2:
                unit = re.split(r'\t',line)
                unit = unit[0:7]
                unit.extend(TE_table[unit[0]])
                print '\t'.join(unit)
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

    TE_table = read_TE_table(args.input)
    convert_table('rice_line_ALL_3000.anno.landrace.list', TE_table) 

if __name__ == '__main__':
    main()

