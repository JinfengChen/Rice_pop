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
python merge_anno.py

Generate annotation table for tree view
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#1       IRRI    IRIS 313-15896  FEDEARROZ 50::G1-1              FEDEARROZ 50    Colombia        IRGC 126957     FEDEARROZ 50::G1        Indica  ERS467753
def readtable_1A(infile, group_color):
    data = defaultdict(lambda : list)
    #ofile1 = open('rice_line_IRRI_2466_1.download.list', 'w')
    #ofile2 = open('rice_line_IRRI_2466_2.download.list', 'w')
    #ofile3 = open('rice_line_IRRI_2466_3.download.list', 'w')
    #ofile4 = open('rice_line_IRRI_2466_4.download.list', 'w')
    #ofile5 = open('rice_line_IRRI_2466_5.download.list', 'w')
    #ofile  = [ofile1, ofile2, ofile3, ofile4, ofile5]
    #count  = 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'E'): 
                #count += 1
                #rank   = int(float(count - 1)/float(num))
                unit   = re.split(r'\t',line)
                #unit[2]= re.sub(r' ', '_', unit[2])
                #print unit[5], unit[6], unit[9]
                sample_name = unit[5] if not unit[5] == '' else 'NA'
                origin      = unit[6] if not unit[6] == '' else 'NA'
                group       = unit[9] if not unit[9] == '' else 'NA'
                color       = group_color[group] if group_color.has_key(group) else 'black'
                data[unit[2]] = [color, sample_name, origin, group]
                #for ln in sorted(sample2sra[unit[10]].keys()):
                #    print >> ofile[rank], '%s\t%s\t%s\t%s\t%s\t%s' %(unit[0], unit[2], unit[6], unit[9], unit[10], ln)
    #for o in ofile:
    #    o.close()
    return data 

#Entry_No        Source  DNA_UNIQUE_ID   DNA_VARNAME_source      DNA_Othername_source    ORI_COUNTRY     Genetic_Stock_Accno     Variety Group   SRA Accession
#1       MC      B001    <E9><BB><91><E6><A0><87>        Heibiao China   I1A12996        Temperate japonica      ERS470219
def readtable_1B(infile, group_color):
    data = defaultdict(lambda : list)
    #ofile = open('rice_line_CAAS_534.download.list', 'w')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'E'): 
                unit = re.split(r'\t',line)
                sample_name = unit[4] if not unit[4] == '' else unit[3]
                origin      = unit[5] if not unit[5] == '' else 'NA'
                group       = unit[7] if not unit[7] == '' else 'NA'
                color       = group_color[group] if group_color.has_key(group) else 'black'
                data[unit[2]] = [color, sample_name, origin, group]
                #print unit[0], unit[2], unit[5], unit[7], unit[8]
                #for ln in sorted(sample2sra[unit[8]].keys()):
                #    print >> ofile, '%s\t%s\t%s\t%s\t%s\t%s' %(unit[0], unit[2], unit[5], unit[7], unit[8], ln)
    #ofile.close()
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


#ERS467799_RelocaTEi     11      31      IRIS313-9346    Taiwan  Temperate japonica
#ERS470219_RelocaTEi     30      60      B001    China   Temperate japonica
def read_mping(infile, mping):
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                uid  = re.sub(r'IRIS', r'IRIS ', unit[3])
                mping[uid] = unit[2]


def main():

    group_color = {
        'Indica'             : 'green',
        'Temperate japonica' : 'blue',
        'Tropical japonica'  : 'cornflowerblue',
        'Japonica'           : 'cyan',
        'Aus/boro'           : 'chocolate',
        'Basmati/sadri'      : 'darkorchid',
        'Intermediate type'  : 'black'
    }
  
    mping = defaultdict(lambda : int())
    read_mping('../CAAS/Japonica_fastq_RelocaTEi_mPing.summary', mping)
    read_mping('../IRRI/Japonica_fastq_RelocaTEi_mPing_IRRI_Jap.summary', mping)

    #sample2sra = readtable_sra('seq_file_mapping_to_SRA.txt')
    irri = readtable_1A('rice_line_metadata_20141029_TableS1A.txt', group_color)
    caas = readtable_1B('rice_line_metadata_20141029_TableS1B.txt', group_color)
    ofile = open('rice_line_ALL_3000.anno.list', 'w')
    print >> ofile, 'Taxa\tColor\tLabel\tName\tOrigin\tGroup\tmPing'
    for unique_id in sorted(caas.keys()):
        label = '|'.join(map(lambda x: str.replace(x, ' ', '_'), [caas[unique_id][1], unique_id, caas[unique_id][3][:4]]))
        mping_c = mping[unique_id] if mping.has_key(unique_id) else -10
        print >> ofile, '%s\t%s\t%s\t%s\t%s\t%s\t%s' %(unique_id, caas[unique_id][0], label, caas[unique_id][1], caas[unique_id][2], caas[unique_id][3], mping_c)
    for unique_id in sorted(irri.keys()):
        label = '|'.join(map(lambda x: str.replace(x, ' ', '_'), [irri[unique_id][1], unique_id, irri[unique_id][3][:4]]))
        mping_c = mping[unique_id] if mping.has_key(unique_id) else -10
        print >> ofile, '%s\t%s\t%s\t%s\t%s\t%s\t%s' %(unique_id, irri[unique_id][0], label, irri[unique_id][1], irri[unique_id][2], irri[unique_id][3], mping_c)
    ofile.close()


if __name__ == '__main__':
    main()

