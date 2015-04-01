#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
import glob
import gzip

def usage():
    test="name"
    message='''
python ReNameSRA_merge_subset.py --input ./CAAS_1/

Read all directory under CAAS_1, convert sra into fastq and merge fastq in one subdir into two _1 and _2 files
We deal with 50 sample everytime to save space. Use subpop to deal with Japonica only first
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource walltime=100:00:00,mem=2G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP/SRP003/SRP003189/
#"SRX025294","Resequencing of 50 rice individuals-rufipogon_Yuan3-9 ","Oryza sativa","Illumina Genome Analyzer II","BGI","SRP003189","Resequencing of 50 rice individuals","SRS086373","","243.58","1","6711790","590637520","ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX025/SRX025294","SZC08001CTDCAAPE","WGS","GENOMIC","PCR"
def read_sra_inf(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit    = re.split(r',', line)
                acc     = re.sub(r'"','', unit[0])
                strain  = re.sub(r'"','', unit[1][37:])
                strain  = re.sub(r' ','', strain)
                link    = re.sub(r'"','', unit[13])
                link    = re.sub(r' ','', link)
                data[acc] = [strain, link]
    return data

#1       B001    China   Temperate japonica      ERS470219       anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/ERR/ERR622/ERR622583/ERR622583.sra
#1       B001    China   Temperate japonica      ERS470219       anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/ERR/ERR622/ERR622584/ERR622584.sra
def read_sra_run(infile, pop):
    data = defaultdict(str)
    r    = re.compile(r'%s' %(pop), re.IGNORECASE)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit    = re.split(r'\t', line)
                acc     = unit[4]
                if r.search(unit[3]):
                    if not data.has_key(acc):
                        data[acc] = pop
    return data


def merge_fq(fastq, fq_out):
    infile = gzip.open(fastq, 'r')
    ofile  = gzip.open(fq_out, 'ab')
    for record in SeqIO.parse(infile, "fastq"):
        SeqIO.write(record, ofile, 'fastq')
    infile.close()
    ofile.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-l', '--list')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)
    
    if not args.list:
        args.list = 'rice_line_CAAS_534.download.list'
    if not args.output:
        args.output = 'Japonica_fastq'

    if not os.path.exists(args.output):
        os.mkdir(args.output)
    ##process 50 only each time
    num       = 50
    acc_left  = defaultdict(lambda : int())
    acc_num   = defaultdict(lambda : int())
    ##get accession only from sub population
    acc2pop   = read_sra_run(args.list, 'japonica')
    sras      = glob.glob('%s/*/*.sra' %(args.input))
    ofile     = open('dump.sh', 'w')
    for sra in sras:
        sra    = os.path.abspath(sra)
        dirname= os.path.abspath(os.path.dirname(sra))
        prefix = os.path.split(os.path.splitext(sra)[0])[-1]    
        acc    = os.path.split(dirname)[-1]
        dirout = '%s/%s' %(os.path.abspath(args.output), acc)
        fq1    = '%s/%s_1.fastq' %(dirout, prefix)
        fq2    = '%s/%s_2.fastq' %(dirout, prefix)
        fq1gz  = '%s/%s_1.fastq.gz' %(dirout, prefix)
        fq2gz  = '%s/%s_2.fastq.gz' %(dirout, prefix)
        ##skip if result exists or not belong to subpop
        if os.path.isfile(fq1gz) or os.path.isfile(fq2gz) or not acc2pop.has_key(acc):
            continue
        acc_num[acc]  = 1
        #print 'Before: %s, %s' %(sra, len(acc_num.keys()))
        ##skip if already have 50 sample process
        if len(acc_num.keys()) > num:
            acc_left[acc]  = 1
            continue
        #print 'After: %s, %s' %(sra, len(acc_num.keys()))
        if not os.path.exists(dirout):
            os.mkdir(dirout)
        cmd    = []
        #fq1    = '%s/%s_1.fastq' %(dirout, prefix)
        #fq2    = '%s/%s_2.fastq' %(dirout, prefix)
        #fq1gz  = '%s/%s_1.fastq.gz' %(dirout, prefix)
        #fq2gz  = '%s/%s_2.fastq.gz' %(dirout, prefix)
        if not os.path.isfile(fq1) and not os.path.isfile(fq1gz):
            cmd.append('/opt/sratoolkit/2.4.2/bin/fastq-dump --outdir %s --split-files %s' %(dirout, sra))
            cmd.append('gzip %s' %(fq1))
            cmd.append('gzip %s' %(fq2))
            #pass
        elif os.path.isfile(fq1) and not os.path.isfile(fq1gz):
            cmd.append('gzip %s' %(fq1))
            cmd.append('gzip %s' %(fq2))
        print >> ofile, '\n'.join(cmd)
    ofile.close()
    print 'Left sample: %s' %(len(acc_left.keys()))
    runjob('dump.sh', 12) 

if __name__ == '__main__':
    main()

