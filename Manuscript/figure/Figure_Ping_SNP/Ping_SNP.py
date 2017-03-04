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
    return dna.count(nucleotide)

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

    ping = os.path.abspath('ping.fa')
    relocate2_dirs = glob.glob("%s/*_RelocaTE2" %(args.input))
    ofile = open('run_ping_SNP.sh', 'w')
    for strain_dir in sorted(relocate2_dirs):
        #print >> ofile, strain_dir
        strain = re.sub(r'_RelocaTEi', r'', os.path.split(strain_dir)[1])
        #strain = re.sub(r'_RelocaTE2', r'', os.path.split(strain_dir)[1])
        strain_dir = os.path.abspath(strain_dir)
        strain     = os.path.abspath(strain)
        cmd = []
        cmd.append('cat %s/repeat/te_only_read_portions_fa/*_1.te_repeat.*_prime.fa | sed "s/>/>read1\./" > %s_1.te_repeat.5_3_prime.fa' %(strain_dir, strain))
        cmd.append('cat %s/repeat/te_only_read_portions_fa/*_2.te_repeat.*_prime.fa | sed "s/>/>read2\./" > %s_2.te_repeat.5_3_prime.fa' %(strain_dir, strain))
        cmd.append('cat %s/repeat/te_containing_fq/*_1.te_repeat.ContainingReads.fq > %s_1.te_repeat.ContainingReads.fq' %(strain_dir, strain))
        cmd.append('cat %s/repeat/te_containing_fq/*_2.te_repeat.ContainingReads.fq > %s_2.te_repeat.ContainingReads.fq' %(strain_dir, strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/seqtk seq -A %s_1.te_repeat.ContainingReads.fq | sed "s/>/>read1\./" > %s_1.te_repeat.ContainingReads.fa' %(strain, strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/seqtk seq -A %s_2.te_repeat.ContainingReads.fq | sed "s/>/>read2\./" > %s_2.te_repeat.ContainingReads.fa' %(strain, strain))
        cmd.append('perl ~/BigData/software/bin/fastaDeal.pl --pat "middle" %s_1.te_repeat.ContainingReads.fa > %s_1.te_repeat.ContainingReads_middle.fa' %(strain, strain))
        cmd.append('perl ~/BigData/software/bin/fastaDeal.pl --pat "middle" %s_2.te_repeat.ContainingReads.fa > %s_2.te_repeat.ContainingReads_middle.fa' %(strain, strain))
        cmd.append('cat %s_1.te_repeat.5_3_prime.fa %s_2.te_repeat.5_3_prime.fa %s_1.te_repeat.ContainingReads_middle.fa %s_2.te_repeat.ContainingReads_middle.fa > %s.te_reads.fa' %(strain, strain, strain, strain, strain))
        cmd.append('python ~/BigData/software/bin/fasta2fastq.py %s.te_reads.fa %s.te_reads.fq' %(strain, strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa mem %s %s.te_reads.fq > %s.sam' %(ping, strain, strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools view -bS -o %s.raw.bam %s.sam' %(strain, strain)) 
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools sort -m 1000000000 %s.raw.bam %s' %(strain, strain))
        cmd.append("/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools view -h %s.bam | perl -lane 'if($F[11] =~ /^NM:i:(\d+)$/){print if $1<=2}else{print}'| /opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools view -bS - -o %s.NM2.bam" %(strain, strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools index %s.bam' %(strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools index %s.NM2.bam' %(strain))
        cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/0.1.19/bin/samtools mpileup %s.NM2.bam > %s.NM2.mpileup' %(strain, strain))
        print >> ofile, '\n'.join(cmd)
        #cat fq_RelocaTE2/rufipogon_W1715_RelocaTE2/repeat/te_only_read_portions_fa/*.five_prime.fa > rufipogon_W1715_1.te_repeat.five_prime.fa
    ofile.close()

    runjob('run_ping_SNP.sh', 170)

    ofile = open('run_ping_SNP.16th_SNP.summary', 'w')
    mpileup_files = glob.glob('*.mpileup')
    for f in sorted(mpileup_files):
        cmd = "cat %s | awk '{if($2==16){print $5}}'" %(f) 
        sequence = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
        g = count_nucleotides(sequence, 'G')
        t = count_nucleotides(sequence, 'T')
        a = count_nucleotides(sequence, 'A')
        c = count_nucleotides(sequence, 'C')
        strain = re.sub(r'.mpileup', r'', f)
        print >> ofile, '%s\t%s\t%s\t%s\t%s' %(strain, g, t, a, c)
    ofile.close()

if __name__ == '__main__':
    main()

