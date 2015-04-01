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
python merge_inf.py

    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#1       IRRI    IRIS 313-15896  FEDEARROZ 50::G1-1              FEDEARROZ 50    Colombia        IRGC 126957     FEDEARROZ 50::G1        Indica  ERS467753
def readtable_1A(infile, sample2sra, num):
    data = defaultdict(str)
    ofile1 = open('rice_line_IRRI_2466_1.download.list', 'w')
    ofile2 = open('rice_line_IRRI_2466_2.download.list', 'w')
    ofile3 = open('rice_line_IRRI_2466_3.download.list', 'w')
    ofile4 = open('rice_line_IRRI_2466_4.download.list', 'w')
    ofile5 = open('rice_line_IRRI_2466_5.download.list', 'w')
    ofile  = [ofile1, ofile2, ofile3, ofile4, ofile5]
    count  = 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'E'): 
                count += 1
                rank   = int(float(count - 1)/float(num))
                unit   = re.split(r'\t',line)
                unit[2]= re.sub(r' ', '', unit[2])
                #print unit[0], unit[2], unit[6], unit[9], unit[10]
                for ln in sorted(sample2sra[unit[10]].keys()):
                    print >> ofile[rank], '%s\t%s\t%s\t%s\t%s\t%s' %(unit[0], unit[2], unit[6], unit[9], unit[10], ln)
    for o in ofile:
        o.close()
    

#Entry_No        Source  DNA_UNIQUE_ID   DNA_VARNAME_source      DNA_Othername_source    ORI_COUNTRY     Genetic_Stock_Accno     Variety Group   SRA Accession
#1       MC      B001    <E9><BB><91><E6><A0><87>        Heibiao China   I1A12996        Temperate japonica      ERS470219
def readtable_1B(infile, sample2sra):
    data = defaultdict(str)
    ofile = open('rice_line_CAAS_534.download.list', 'w')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'E'): 
                unit = re.split(r'\t',line)
                #print unit[0], unit[2], unit[5], unit[7], unit[8]
                for ln in sorted(sample2sra[unit[8]].keys()):
                    print >> ofile, '%s\t%s\t%s\t%s\t%s\t%s' %(unit[0], unit[2], unit[5], unit[7], unit[8], ln)
    ofile.close()
    return data

#PRJEB6180       IRIS_313-10889  ERS469694       4530    ERX562030       IRIS_313-10889_111221_I147_FCC0CB6ACXX_L3_RICwdsRSYHSD17-3-IPAAPEK-21.exp       ERR605259
def readtable_sra(infile):
    data = defaultdict(lambda : defaultdict(lambda : int()))
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Project'): 
                unit   = re.split(r'\t',line)
                #print unit[2], unit[6]
                subdir = unit[6][:6]
                #wget
                #link   = 'ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/ERR/%s/%s/%s.sra' %(subdir, unit[6], unit[6])
                #ascp
                link    = 'anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/ERR/%s/%s/%s.sra' %(subdir, unit[6], unit[6])
                data[unit[2]][link] = 1
    return data

def main():

    sample2sra = readtable_sra('seq_file_mapping_to_SRA.txt')
    readtable_1A('rice_line_metadata_20141029_TableS1A.txt', sample2sra, 500)
    readtable_1B('rice_line_metadata_20141029_TableS1B.txt', sample2sra)

if __name__ == '__main__':
    main()

