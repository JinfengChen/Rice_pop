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
import subprocess
import pysam

def usage():
    test="name"
    message='''
python Ping_SNP.py --input fq_RelocaTE2

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines %s --interval 120 --task 1 --mem 15G --time 10:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

def read_fastq(indir):
    fqs = glob.glob('%s/*_1.fastq.gz' %(indir))
    fq1_list = []
    fq2_list = []
    for fq1 in sorted(fqs):
        fq2 = re.sub(r'_1.fastq.gz', r'_2.fastq.gz', fq1)
        fq1_list.append(fq1)
        fq2_list.append(fq2)
    return ' '.join(fq1_list), ' '.join(fq2_list)
        

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

def count_nucleotides(dna, nucleotide):
    return dna.lower().count(nucleotide.lower())

#input bam file of SNP splitted
#return dict with read cover the SNP
def snp_reads_from_bam(bam, snp):
    fsam = pysam.AlignmentFile(bam, 'rb')
    data = defaultdict(lambda : int())
    for record in fsam.fetch(until_eof = True):
        if not record.is_unmapped:
            name   = record.query_name
            start  = int(record.reference_start) + 1
            end    = int(record.reference_end) + 1
            if start < 16 and end > 16:
                data[name] = 1
    return data

#overlap SNP reads and Ping
#input ping_reads, G_reads and A_reads
#return dict with SNP->reads->1 
def overlap_reads(ping_reads, G_reads, A_reads):
    ping_reads_class = defaultdict(lambda : defaultdict(lambda : int()))
    for ping_read in sorted(ping_reads.keys()):
        if G_reads.has_key(ping_read):
            ping_reads_class['G'][ping_read] = 1
        elif A_reads.has_key(ping_read):
            ping_reads_class['A'][ping_read] = 1
        else:
            ping_reads_class['UN'][ping_read] = 1
    return ping_reads_class 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fastq_dir')
    parser.add_argument('-g', '--genome')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.fastq_dir) > 0
    except:
        usage()
        sys.exit(2)

    samtools = '/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools'
    ping = os.path.abspath(args.genome)
    strain_fq1 = glob.glob("%s/*_1.fastq.gz" %(args.fastq_dir))
    ofile = open('run_mapping.sh', 'w')
    for fq1 in sorted(strain_fq1):
        #print >> ofile, strain_dir
        fq1 = os.path.abspath(fq1)
        fq2 = re.sub(r'_1.fastq.gz', r'_2.fastq.gz', fq1)
        strain = re.sub(r'_1.fastq.gz', r'_Pseudo', fq1)
        cmd = []
        ##
        cmd.append('''/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa mem %s %s %s | %s view -F4 -bS -o %s.raw.bam -''' %(ping, fq1, fq2, samtools, strain))
        #cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools view -bS -o %s.raw.bam %s.sam' %(strain, strain)) 
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools sort -m 1000000000 %s.raw.bam %s' %(strain, strain))
        cmd.append("/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools view -h %s.bam | perl -lane 'if($F[11] =~ /^NM:i:(\d+)$/){print if $1<=2}else{print}'| /opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools view -bS - -o %s.NM2.bam" %(strain, strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools index %s.bam' %(strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools index %s.NM2.bam' %(strain))
        #cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools mpileup %s.NM2.bam > %s.NM2.mpileup' %(strain, strain))
        #cmd.append('rm %s.raw.bam %s.sam %s_1.te_repeat.5_3_prime.fa %s_2.te_repeat.5_3_prime.fa %s_1.te_repeat.ContainingReads.fq %s_2.te_repeat.ContainingReads.fq %s_1.te_repeat.ContainingReads.fa %s_2.te_repeat.ContainingReads.fa %s_1.te_repeat.ContainingReads_middle.fa %s_2.te_repeat.ContainingReads_middle.fa' %(strain, strain, strain, strain, strain, strain, strain, strain, strain, strain))
        print >> ofile, '\n'.join(cmd)
        #cat fq_RelocaTE2/rufipogon_W1715_RelocaTE2/repeat/te_only_read_portions_fa/*.five_prime.fa > rufipogon_W1715_1.te_repeat.five_prime.fa
    ofile.close()

    runjob('run_mapping.sh', 5)

if __name__ == '__main__':
    main()

