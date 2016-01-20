#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
sys.path.append('/rhome/cjinfeng/BigData/software/ProgramPython/lib')
from utility import gff_parser, createdir
import glob

def usage():
    test="name"
    message='''
python Strain_Diff.py --input ../Rice_50_fastq_allTE_RelocaTE2 > log 2>&1 &

    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def line_num(infile):
    num = 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                num += 1 
    return num

#711     IRIS313-8209    Greece  Temperate japonica      ERS468463
def name2acc(infile):
    data = defaultdict(lambda : str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                unit = re.split(r'\t', line)
                unit[1] = re.sub(r'IRIS', r'IRIS_', unit[1])
                data[unit[4]] = unit[1]
                #print unit[1], unit[4]
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

    name_dict = name2acc('rice_line_IRRI_2466.download.list')

    #~/BigData/00.RD/RelocaTE_i/Real_Data/Rice_50/RelocaTEi/TE_diversity/Rice_50_fastq_allTE_RelocaTE2/11010_TRJ_RelocaTE2
    #HEG4_group_RelocaTEi/ERS467761_RelocaTEi/repeat/results/ALL.all_nonref_insert.high_conf.gff
    #link gff file into "gff"
    gffs = glob.glob('%s/*/repeat/results/*.high_conf.gff' %(args.input))
    createdir('gff')
    for gff in gffs:
        dirs = re.split(r'/', gff) 
        name = re.sub(r'_RelocaTEi', r'', dirs[-4])
        #print name, name_dict[name], gff
        #if not name.startswith('niv') and not name.startswith('ruf'):
        #    words = re.split(r'_', name)
        #    name  = '%s_%s' %(words[1], words[0])
        #os.system('ln -sf %s gff/%s.gff' %(os.path.abspath(gff), name_dict[name]))
        os.system('grep -v "ping" %s > gff/%s.gff' %(os.path.abspath(gff), name_dict[name]))

    #create pairwise difference of TE
    gffs = glob.glob('gff/*.gff')
    data = defaultdict(lambda : defaultdict(lambda : list()))
    for i in range(0, len(gffs)):
        strain1 = os.path.splitext(os.path.split(gffs[i])[1])[0]
        for j in range(0, len(gffs)):
            strain2 = os.path.splitext(os.path.split(gffs[j])[1])[0]
            if not i == j:
                os.system('bedtools window -w 100 -a %s -b %s > temp.overlap' %(gffs[i], gffs[j]))
                data[strain1][strain2] = [line_num(gffs[i])-line_num('temp.overlap'), line_num(gffs[j])-line_num('temp.overlap'), line_num('temp.overlap')]
            else:
                data[strain1][strain2] = [0, 0, line_num(gffs[i])]

    header = ['Strain']
    lines  = []
    for s1 in sorted(data.keys()):
        #header.append(s1)
        #line = [s1]
        for s2 in sorted(data[s1].keys()):
            if s1 == s2:
                #line.append(0)
                continue
            else:
                print '%s\t%s\t%s\t%s\t%s' %(s1, s2, data[s1][s2][0], data[s1][s2][1], data[s1][s2][2])
                #line.append('%s|%s|%s' %(data[s1][s2][0], data[s1][s2][1], data[s1][s2][2]))
        #lines.append(line)
    #print '\t'.join(header)
    #for l in lines:
    #    print '\t'.join(map(str, l))

if __name__ == '__main__':
    main()

