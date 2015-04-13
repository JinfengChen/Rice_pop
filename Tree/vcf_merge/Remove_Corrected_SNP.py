#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
import vcf

def usage():
    test="name"
    message='''
Remove_Corrected_SNP.py


    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def readtable(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if not data.has_key(unit[0]):
                    data[unit[0]] = unit[1]
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    #try:
    #    len(args.input) > 0
    #except:
    #    usage()
    #    sys.exit(2)

    #store reference
    ref_allele  = defaultdict(lambda : str())
    rice_3k_vcf = vcf.Reader(filename='3K_coreSNP-v2.1.binary.1.recode.vcf.gz')
    for record in rice_3k_vcf:
        pos = '%s_%s' %(str(record.CHROM), str(record.POS))
        ref_allele[pos] = str(record.REF)
        #print pos, str(record.REF)
     

    #skip difference reference snp
    count = 0
    corrected = 0
    ofile = open('HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.recode.NoCorrected.vcf', 'w')
    with gzip.open ('HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.recode.vcf.gz', 'rb') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                if line.startswith(r'#'):
                    print >> ofile, line
                else:
                    unit = re.split(r'\t',line)
                    pos  = '%s_%s' %(str(unit[0]), str(unit[1]))
                    count += 1
                    if ref_allele[pos] == str(unit[3]):
                        print >> ofile, line
                    else:
                        corrected += 1
    ofile.close()
    print 'all snp: %s' %(count)
    print 'corrected: %s' %(corrected)

if __name__ == '__main__':
    main()

