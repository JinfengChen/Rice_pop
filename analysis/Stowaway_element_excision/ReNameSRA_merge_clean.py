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
python ReNameSRA_merge_clean.py --input ./CAAS_1/

Read sra under directory of CAAS_1 and check if fastq exists in output delete these sra
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
        args.list = '../GigaScience/rice_line_IRRI_2466.download.list'
    if not args.output:
        args.output = args.input

    if not os.path.exists(args.output):
        os.mkdir(args.output)
    ##process 50 only each time
    num       = 2
    acc_sra  = defaultdict(lambda : int())
    acc_fq   = defaultdict(lambda : int())
    acc_dir  = defaultdict(lambda : str())
    ##get accession only from sub population
    acc2pop   = read_sra_run(args.list, 'japonica')
    sras      = glob.glob('%s/*/*.sra' %(args.input))
    ofile     = open('clean.sh', 'w')
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
        acc_dir[acc] = dirname
        acc_sra[acc] += 1
        if os.path.isfile(fq1gz) and os.path.getsize(fq1gz) > 0 and os.path.isfile(fq2gz) and os.path.getsize(fq2gz) > 0:
            acc_fq[acc] += 1
    for acc in sorted(acc_sra.keys()):
        #print '%s %s' %(acc_sra[acc], acc_fq[acc])
        if acc_sra[acc] == acc_fq[acc] and not acc == '':
            cmd = 'rm %s/*.sra' %(acc_dir[acc])
            print >> ofile, cmd
    ofile.close()
    #runjob('dump.sh', 3) 

if __name__ == '__main__':
    main()

