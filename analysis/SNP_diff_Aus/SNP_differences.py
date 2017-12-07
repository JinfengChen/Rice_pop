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
    cmd = 'perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource nodes=1:ppn=12,walltime=100:00:00,mem=20G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def compare_sample_vcf(infile):
    data = defaultdict(lambda : defaultdict(lambda : int()))
    samples = []
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if line.startswith(r'#CHROM'): 
                samples.extend(re.split(r'\t',line))
                #for i in range(9,len(samples)):
                    #print samples[i]
            elif not line.startswith(r'#') and len(line) > 2:
                print line
                unit = re.split(r'\t',line)
                for i in range(9,len(unit)-1):
                    for j in range(i+1,len(unit)):
                        #print i, j
                        #compared, shared, differences, unique1, unique2
                        #compare = [0, 0, 0, 0, 0]
                        pairs = '%s:%s' %(samples[i], samples[j])
                        if not unit[i][0] == unit[i][2] or unit[i][0] == '.' or unit[i][2] == '.':
                            #sample 1 het or not covered
                            continue
                        elif not unit[j][0] == unit[j][2] or unit[j][0] == '.' or unit[j][2] == '.':
                            #sample 2 het or not covered
                            continue
                        elif unit[i][0] == unit[j][0] and unit[i][0] == '0':
                            #both same with NB
                            continue

                        else:
                            #both sample hom
                            data[pairs][0] += 1
                            if unit[i][0] == unit[j][0] and unit[i][0] == '1':
                                #both difference from NB
                                data[pairs][1] +=1
                            elif unit[i][0] == '1':
                                print '{} is 1'.format(unit[i][0])
                                #sample 1 diff from NB, sample2 same
                                data[pairs][2] += 1
                                data[pairs][3] += 1
                            elif unit[j][0] == '1':
                                print '{} is 1'.format(unit[j][0])
                                #sample 2 diff from NB, sample1 same
                                data[pairs][2] += 1
                                data[pairs][4] += 1
                            else:
                                print 'not possible'
                                continue
                        #print pairs
                        #print compare
                        #print '%s\t%s' %(pairs, '\t'.join(map(str, compare)))
    outfile = '%s.SNPdiff' %(infile)
    ofile = open(outfile, 'w')
    for pair in sorted(data.keys()):
        #print data[pair][0]
        compare = [data[pair][0], data[pair][1], data[pair][2], data[pair][3], data[pair][4]]
        print >> ofile, '%s\t%s' %(pair, '\t'.join(map(str, compare)))
    ofile.close()

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

    compare_sample_vcf(args.input)

if __name__ == '__main__':
    main()

