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
python Split_Fastq2PE.py --input rufipogon_W0180_RelocaTE2.te_reads.fq
Input fastq is a mix of read1 and read2 of PE sequence. We split the fatsq file into read1.fq, read2.fq and unpaired.fq using read name.

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines %s --interval 120 --task 1 --mem 15G --time 100:00:00 --queue stajichlab --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#repeat	Chr1:38668855..38668857	Left_supporting_reads	ERR068809.5052702,ERR068809.7020963,ERR068809.10628656
def locus_reads_list(infile):
    data = defaultdict(lambda : list())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                unit[1] = re.sub(r'\.\.', r'_', unit[1])
                unit[1] = re.sub(r':', r'_', unit[1])
                locus = '%s_%s' %(unit[0], unit[1])
                print line, locus
                if len(unit) < 4:
                    continue
                reads = re.split(r',', unit[3])
                for read in reads:
                    data[locus].append(re.split(r':', read)[0])
    prefix = re.sub(r'.list', r'', infile)
    for locus in data.keys():
        ofile = open('%s.%s.list' %(prefix, locus), 'w')
        print >> ofile, '\n'.join(list(set(data[locus])))
        ofile.close()

def get_fastq_seq_by_list(fastqfile, id_list, prefix):
    ofile = open('%s.fq' %(prefix), 'w')
    for record in SeqIO.parse(fastqfile, "fastq"):
        #print 'id:', record.id
        #print 'seq:', record.seq
        unit = re.split(r':', str(record.id))
        record.id = unit[0]
        if id_list.has_key(unit[0]):
            SeqIO.write(record, ofile, 'fastq')
    ofile.close()

def read_list(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                data[unit[0]] = 1
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    home_dir = os.path.split(os.path.realpath(__file__))[0]
    file_list = glob.glob('%s/*.NM2.bam' %(args.input))
    ofile     = open('%s.asm.sh' %(args.input), 'w')
    cmd = []
    for f in file_list:
        #ERS470279_Pseudo.NM2.bam
        prefix = re.sub(r'_Pseudo.NM2.bam', r'', f)
        if not os.path.exists('%s.assembly' %(prefix)):
            cmd.append('cd %s' %(os.path.dirname(os.path.abspath(args.input))))
            cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.6/bin/samtools view %s Ping_up:50-750 | cut -f1 > %s.upreads.list' %(f, prefix))
            cmd.append('python %s/Get_List_Raw_Fastq.py --list %s.upreads.list --fq1 %s_1.fastq.gz --fq2 %s_2.fastq.gz' %(home_dir, prefix, prefix, prefix))
            #cmd.append('python %s/Split_Fastq2PE.py --input %s' %(home_dir, re.sub(r'.list', r'.fq', f)))
            cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth %s.up.assembly 31 -shortPaired -fastq -separate %s.upreads_1.fq %s.upreads_2.fq' %(prefix, prefix, prefix))
            cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg %s.up.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes' %(prefix))

            cmd.append('/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.6/bin/samtools view %s Ping_up:6120-6900 | cut -f1 >> %s.downreads.list' %(f, prefix))
            cmd.append('python %s/Get_List_Raw_Fastq.py --list %s.downreads.list --fq1 %s_1.fastq.gz --fq2 %s_2.fastq.gz' %(home_dir, prefix, prefix, prefix))
            cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth %s.down.assembly 31 -shortPaired -fastq -separate %s.downreads_1.fq %s.downreads_2.fq' %(prefix, prefix, prefix))
            cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg %s.down.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes' %(prefix))
    for c in cmd:
        print >> ofile, c
        #os.system(c)
    ofile.close()
    runjob('%s.asm.sh' %(args.input), 9) 
    ofile     = open('%s.asm2.sh' %(args.input), 'w')
    cmd = []
    cmd.append('cd %s' %(os.path.abspath(args.input)))
    cmd.append('cat *.upreads_1.fq > test_upreads_1.fq')
    cmd.append('cat *.upreads_2.fq > test_upreads_2.fq')
    cmd.append('cat *.downreads_1.fq > test_downreads_1.fq')
    cmd.append('cat *.downreads_2.fq > test_downreads_2.fq')
    cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq')
    cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes')
    cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq')
    cmd.append('/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes')
    cmd.append('cd ..')
    for c in cmd:
        print >> ofile, c
    ofile.close()
    os.system('bash %s.asm2.sh' %(args.input)) 

if __name__ == '__main__':
    main()

