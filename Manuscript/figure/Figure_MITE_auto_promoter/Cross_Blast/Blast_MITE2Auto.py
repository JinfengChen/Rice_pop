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
python CircosConf.py --input circos.config --output pipe.conf

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-c', '--cpu')
    parser.add_argument('-r', '--reference')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    if not args.cpu:
        args.cpu = 1

    cd_hit_est='/opt/linux/centos/7.x/x86_64/pkgs/cd-hit/4.6.4/cd-hit-est'
    #
    target_dir  = os.path.abspath(args.input)
    print target_dir
    target_activeTE = glob.glob('%s/*_activeTE' %(target_dir))
    #/Target_Run_DJ123_angiosperm_harbinger_tpase_angiosperm_harbinger_tpase_2017_03_18_162312_activeTE/
    r = re.compile(r'Target_Run_(\w+?)_angiosperm_(\w+?)_tpase')
    for aTE in sorted(target_activeTE):
        print aTE
        m = r.search(aTE)
        strain = 'NA'
        repeat = 'NA'
        if m:
            strain = m.groups(0)[0]
            repeat = m.groups(0)[1]
        cmd = []
        cmd.append('ln -s %s/nonredundant_pep_union-10kb.fa Auto_%s_%s.fa' %(aTE, strain, repeat))
        cmd.append('formatdb -i Auto_%s_%s.fa -p F' %(strain, repeat))
        cmd.append('blastall -p blastn -i %s -d Auto_%s_%s.fa -o MITE2%s_%s.blast -e 1e-5 -F F' %('MSU7.MITEhunter.fasta.len800.fasta', strain, repeat, strain, repeat))
        cmd.append('perl ~/BigData/software/bin/blast_parser.pl MITE2%s_%s.blast > MITE2%s_%s.blast.table' %(strain, repeat, strain, repeat))
        cmd.append('python MITE_Auto_Pairs.py --input MITE2%s_%s.blast.table' %(strain, repeat))

        for c in cmd:
            print c
            os.system(c)


if __name__ == '__main__':
    main()

