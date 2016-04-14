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
python Ping_Coverage_matrix.py --input bam_5_rufipogon/ --output ping_coverage_rufipogon.matrix

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource nodes=1:ppn=1,walltime=100:00:00,mem=10G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#Chr6_23521641_23526981_fwd      1       0
#Chr6_23521641_23526981_fwd      2       0
#Chr6_23521641_23526981_fwd      3       0
#Chr6_23521641_23526981_fwd      4       0
def read_cov(infile):
    name     = os.path.split(infile)[1]
    coverage = 0
    data     = []
    count   = 0
    covered = 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if int(unit[2]) > 0:
                    data.append('10')
                else:
                    data.append('0')
                count += 1
                if int(unit[2]) > 0:
                    covered += 1
    coverage = covered
    return coverage, data


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

    if not args.output:
        args.output = 'ping_coverage.matrix'

    samtools = '/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools'
    bedtools = '~/BigData/software/bedtools2-2.19.0/bin/bedtools' 
    bams  = glob.glob('%s/*.bam' %(args.input))
    #####generate coverage file for bams
    ofile = open('ping_coverage.sh', 'w')
    count = 0
    for bam in sorted(bams):
        print bam
        coverage = '%s.ping.coverage.txt' %(bam)
        if not os.path.exists(coverage) or int(os.path.getsize(coverage)) == 0:
            print coverage
            cmd = '%s view -b %s Chr6_23521641_23526981_fwd:1-7340 | %s genomecov -ibam stdin -d > %s' %(samtools, os.path.abspath(bam), bedtools, os.path.abspath(coverage))
            print >> ofile, cmd
            count += 1
    ofile.close()
    if count > 0:
        runjob('ping_coverage.sh', 1)
    #####summarize coverage into matrix
    covs = glob.glob('%s/*.ping.coverage.txt' %(args.input))
    all_num = defaultdict(lambda : int())
    all_line= defaultdict(lambda : list())
    for cov in covs:
        name = os.path.split(cov)[1] 
        cov_num, cov_line = read_cov(cov)
        all_num[name]  = cov_num
        all_line[name] = cov_line
    ofile = open(args.output, 'w') 
    for name, num in sorted(all_num.items(), key=lambda x:x[1]):
        #print >> ofile, '%s\t%s\t%s' %(name, num, '\t'.join(all_line[name]))
        print >> ofile, '\t'.join(all_line[name])
    ofile.close()

if __name__ == '__main__':
    main()

