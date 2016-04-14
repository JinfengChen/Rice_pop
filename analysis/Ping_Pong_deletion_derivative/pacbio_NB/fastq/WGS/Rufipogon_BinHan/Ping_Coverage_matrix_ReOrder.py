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
python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rufipogon400_MSU7.matrix.1.header --qry pong_coverage_rufipogon400_MSU7.matrix.1.header &

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

#ERR068679.bam.ping.coverage.clean.txt   0       0
def read_ping_id(infile):
    data = []
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                id_raw = unit[0]
                id_new = re.sub(r'\.bam\.ping\.coverage\.clean\.txt', r'', id_raw)
                #print id_new
                data.append(id_new)
    return data

#ERR068679.bam.ping.coverage.clean.txt   0       0
def read_id_dict(infile):
    data = defaultdict(lambda : list())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                id_raw = unit[0]
                ids    = re.split(r'\.', id_raw)
                id_new = ids[0]
                #id_new = re.sub(r'\.bam\.ping\.coverage\.clean\.txt', r'', id_raw)
                #print id_new
                #print len(unit)
                #print len(unit[1:])
                data[id_new] = unit
    return data

def write_ordered(qry_dict, id_order, qry_file):
    qry_file_matrix = '%s.ordered.txt' %(qry_file)
    qry_file_header = '%s.ordered.header.txt' %(qry_file)
    ofile1 = open (qry_file_matrix, 'w')
    ofile2 = open (qry_file_header, 'w')
    for ids in id_order:
        print >> ofile1, '%s' %('\t'.join(qry_dict[ids][2:]))
        print >> ofile2, '%s' %('\t'.join(qry_dict[ids]))
    ofile1.close()
    ofile2.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ref')
    parser.add_argument('-q', '--qry')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.ref) > 0
    except:
        usage()
        sys.exit(2)

    id_order = read_ping_id(args.ref)
    qry_dict = read_id_dict(args.qry)
    write_ordered(qry_dict, id_order, args.qry)

if __name__ == '__main__':
    main()

