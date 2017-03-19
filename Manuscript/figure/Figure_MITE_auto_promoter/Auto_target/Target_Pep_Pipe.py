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
        len(args.input) > 0 or len(args.reference) > 0
    except:
        usage()
        sys.exit(2)

    if not args.cpu:
        args.cpu = 1

    cd_hit_est='/opt/linux/centos/7.x/x86_64/pkgs/cd-hit/4.6.4/cd-hit-est'
    #
    cmd = []
    home_dir   = os.path.abspath(os.path.dirname(sys.argv[0]))
    script_dir = '%s/scripts' %(home_dir)
    reference  = args.reference
    target_pep_dir  = os.path.abspath(args.input)
    target_activeTE = '%s_activeTE' %(target_pep_dir)
    #
    cmd.append('mkdir %s' %(target_activeTE))
    cmd.append('python %s/make_BEDfile_all_protein_hits.py %s %s/all_pep-hits.bed %s %s/nonredundant_pep_union-10kb.fa %s/nonredundant_pep_union-hits.fa' %(script_dir, target_pep_dir, target_activeTE, reference, target_activeTE, target_activeTE))
    cmd.append('python %s/split_fasta.py %s/nonredundant_pep_union-10kb.fa %s/split' %(script_dir, target_activeTE, target_activeTE))
    cmd.append('%s -i %s/nonredundant_pep_union-hits.fa -o %s/nonredundant_pep_union-hits_c80 -c 0.8 -G 1 -n 3 -d 0 -g 1 -r 1 -T 24 -M 16000' %(cd_hit_est, target_activeTE, target_activeTE))
    cmd.append('python %s/make_multi_seq_sum.py %s/nonredundant_pep_union-hits_c80.clstr' %(script_dir, target_activeTE))
    cmd.append('perl %s/make_multi_seq.pl %s/nonredundant_pep_union-10kb.fa %s/nonredundant_pep_union-hits_c80.clstr %s/nonredundant_pep_union-10kb_c80_multi 2' %(script_dir, target_activeTE, target_activeTE, target_activeTE))
    cmd.append('python %s/trim_flanks_directory.py %s/nonredundant_pep_union-10kb_c80_multi/ 5000' %(script_dir, target_activeTE))
    #cmd.append('python %s/make_mafft_pep-cluster_split_one_sh.py %s/nonredundant_pep_union-10kb_c80_multi "*trimmed-5000.fa" %s' %(script_dir, target_activeTE, args.cpu))
    #cmd.append('bash mafft.sh') 
    # 
    for c in cmd:
        print c
        os.system(c)


if __name__ == '__main__':
    main()

