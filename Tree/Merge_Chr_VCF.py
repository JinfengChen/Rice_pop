#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO

def usage():
    test="name"
    message='''
python Merge_Chr_VCF.py --input 3K_coreSNP-v2.1 

Merge vcf of individual chromosome into one file
--input: prefix of vcf

    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

##fileformat=VCFv4.2
##fileDate=20150410
##source=PLINKv1.90
##contig=<ID=12,length=27530114>
##INFO=<ID=PR,Number=0,Type=Flag,Description="Provisional reference allele, may not be based on real reference genome">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
def readvcf(infile, chro, header, ofile):
    count= 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                count += 1
                if count <= 3:
                    header[chro][0].append(line)
                elif count == 4:
                    header[chro][1].append(line)
                elif count <= 7:
                    header[chro][2].append(line)
                else:
                    print >> ofile, line


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

    #just in case you have X and Y chromosome
    chrs = [1,2,3,4,5,6,7,8,9,10,11,12]
    temp_vcf  = '%s.temp.vcf' %(args.input)
    temp_head = '%s.temp.header' %(args.input)
    comb_vcf  = '%s.vcf' %(args.input)
    
    #read chromosome vcf
    header = defaultdict(lambda : defaultdict(lambda : list()))
    ofile  = open(temp_vcf, 'w')
    for chro in sorted(chrs, key=int):
        vcf_chr = '%s.%s.vcf' %(args.input, chro)
        readvcf(vcf_chr, chro, header, ofile)
    ofile.close()
    
    #write header of vcf
    ofile = open(temp_head, 'w')
    print >> ofile, '\n'.join(header[chrs[0]][0])
    for chro in sorted(header.keys(), key=int):
        print >> ofile, header[chro][1][0]
    print >> ofile, '\n'.join(header[chrs[0]][2])
    ofile.close()

    #merge files
    os.system('cat %s %s > %s' %(temp_head, temp_vcf, comb_vcf))

if __name__ == '__main__':
    main()

