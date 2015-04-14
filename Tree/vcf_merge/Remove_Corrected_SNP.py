#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import vcf
import gzip

def usage():
    test="name"
    message='''
Remove_Corrected_SNP.py

Change to write a fasta of HEG4, EG4, A123, A119. 3K vcf do not have reference (reference not real)
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = str(record.seq)
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

    #reference sequence
    ref_seq = fasta_id('/rhome/cjinfeng/BigData/00.RD/seqlib/MSU_r7.fa')

    #store landrace
    landrace_allele = defaultdict(lambda : defaultdict(lambda : list()))
    #landrace_vcf = vcf.Reader(filename='HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.test.vcf.gz')
    #landrace_vcf = vcf.Reader(open('HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1_12.vcf', 'r'))
    landrace_vcf = vcf.Reader(filename='HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.recode.vcf.gz')
    for record in landrace_vcf:
        pos = '%s_%s' %(str(record.CHROM), str(record.POS))
        for sample in record.samples:
            #print '1: %s\t%s\t%s\t%s' %(pos, sample.sample, sample.gt_type, sample.gt_bases)
            if not sample.gt_type is None:
                landrace_allele[pos][str(sample.sample)] = [sample.gt_type, sample.gt_bases, str(record.REF)]
                #print '2: %s\t%s\t%s\t%s' %(pos, sample.sample, landrace_allele[pos][str(sample.sample)][0], landrace_allele[pos][str(sample.sample)][1])


    #generate fasta for landrace
    landrace_fa = defaultdict(lambda : str())
    ref_allele  = defaultdict(lambda : str)
    #rice_3k_vcf = vcf.Reader(filename='3K_coreSNP-v2.1.binary.1.test.vcf.gz')
    #rice_3k_vcf = vcf.Reader(open('3K_coreSNP-v2.1.binary.vcf', 'r'))
    rice_3k_vcf = vcf.Reader(filename='3K_coreSNP-v2.1.binary.1.recode.vcf.gz')
    landraces   = ['A119_2', 'A123_2', 'EG4_2', 'HEG4_2']
    for record in rice_3k_vcf:
        pos = '%s_%s' %(str(record.CHROM), str(record.POS))
        #ref_allele[pos] = str(record.REF)
        #print pos, str(record.REF)
        chro = 'Chr%s' %(str(record.CHROM))
        ref  = ref_seq[chro][int(str(record.POS))-1]
        if landrace_allele.has_key(pos):
            print '%s\t%s\t%s\t%s\t%s' %(pos, str(record.REF), str(record.ALT[0]), ref, landrace_allele[pos]['HEG4_2'])
            for sample in landraces:
                print sample
                if not landrace_allele[pos].has_key(sample):
                    landrace_fa[sample] += '-'
                    print 'no key'
                elif landrace_allele[pos][sample] == []:
                    landrace_fa[sample] += '-'
                    print 'empty key'
                else:
                    print 'have key: %s' %(landrace_allele[pos][sample])
                    #heterzygous, use reference base
                    if int(landrace_allele[pos][sample][0]) == 1:
                        landrace_fa[sample] += ref
                        print 'heter: %s' %(landrace_allele[pos][sample])
                    #homozygous alternative
                    elif int(landrace_allele[pos][sample][0]) == 2:
                        #ref is consistence, use alternative
                        if ref == landrace_allele[pos][sample][2]:
                            landrace_fa[sample] += landrace_allele[pos][sample][1][0]
                            print 'homo alt good: %s' %(landrace_allele[pos][sample])
                        #ref is not consistence, use '-'
                        else:
                            landrace_fa[sample] += '-'
                            print 'homo alt bad: %s' %(landrace_allele[pos][sample])
                    #homozygous reference
                    elif int(landrace_allele[pos][sample][0]) == 0:
                        #ref is consistence, use ref
                        if ref == landrace_allele[pos][sample][2]:
                            landrace_fa[sample] += ref
                            print 'homo ref good: %s' %(landrace_allele[pos][sample])
                        #ref is not consistence, use '-'
                        else:
                            landrace_fa[sample] += '-'
                            print 'homo ref bad: %s' %(landrace_allele[pos][sample])
                
        else:
            print '%s\t%s\t%s\t%s' %(pos, str(record.REF), str(record.ALT[0]), ref)    
            for sample in landraces:
                landrace_fa[sample] += ref

    ofile = open('HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.fasta','w')
    #ofile = open('HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.test.fasta','w')
    #ofile = open('HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1_12.fasta','w')
    for sample in sorted(landrace_fa.keys()):
        seq = Seq(landrace_fa[sample])
        record = SeqRecord(seq, id=sample, description="")
        SeqIO.write(record, ofile, "fasta") 
        #print >> ofile, '>%s\n%s' %(sample, landrace_fa[sample])
    ofile.close()

'''
####################################
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
'''

if __name__ == '__main__':
    main()

