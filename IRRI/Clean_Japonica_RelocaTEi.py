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
import fnmatch

def usage():
    test="name"
    message='''
python Clean_Japonica_RelocaTEi.py --input Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Ping/

In Japonica_fastq_RelocaTEi_Ping/mPing/Pong, some results were generated using HEG4_groups. These directory have strain that do not belong to Japonica, which will overlap with Other_fastq.
We delete these results


    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource nodes=1:ppn=12,walltime=100:00:00,mem=20G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#rice_line_IRRI_2466.Japonica.download.list
#711     IRIS313-8209    Greece  Temperate japonica      ERS468463       anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/ERR/ERR607/ERR607769/ERR607769.sra
def readtable(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                data[unit[4]] = unit[1]
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
    temp_out   = '/rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/IRRI/Transposon_mPing_Ping_Pong/temp' 
    strain_jap = readtable('rice_line_IRRI_2466.Japonica.download.list')
    for result in os.listdir(args.input):
        if fnmatch.fnmatch(result, '*_RelocaTEi'):
            #print result
            acc = re.sub(r'_RelocaTEi', r'', result)
            if not strain_jap.has_key(acc):
                print acc
                os.system('mv %s/%s %s/%s_temp/' %(args.input, result, temp_out, result))

if __name__ == '__main__':
    main()

