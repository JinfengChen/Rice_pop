#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
from Bio import AlignIO

def usage():
    test="name"
    message='''
python Build_Tree.py --fasta test.fasta
python Build_Tree.py --plink 3K_coreSNP-v2.1

Build phylogenetic tree using SNPs based alignment for large scale population analysis.
--fasta: fasta format alignment
--plink: plink prefix of map and ped, which we use to extract vcf and convert to fasta alignment
--tool: tool we use to build tree, phylip, fasttree 
--step: 1 to convert plink to fasta, 2 to convert fasta to phy, 3 to build tree using phy
 
    '''
    print message

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

def fasta2phy(fa_align, phy_file):
    #phy_file = '%s.phy' %(os.path.splitext(fa_align)[0])
    ofile    = open(phy_file, 'w') 
    AlignIO.convert(fa_align, 'fasta', ofile, 'phylip-relaxed')
    ofile.close()

def phylip_tree_run(phy_align):
    dist = '%s.dist' %(phy_align)
    tree = '%s.tree' %(phy_align)
    phylip  = '%s.phylip' %(phy_align)
    if not os.path.isfile(dist):
        os.system('cp %s infile' %(phy_align))
        os.system('rm outfile')
        os.system('echo y | /usr/local/bin/dnadist')
        os.system('mv outfile %s' %(dist))
    if not os.path.isfile(tree):
        os.system('cp %s infile' %(dist))
        os.system('echo y | /usr/local/bin/neighbor')
        os.system('mv outtree %s' %(tree))
        os.system('mv outfile %s' %(phylip))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fasta')
    parser.add_argument('-p', '--plink')
    parser.add_argument('-s', '--step')
    parser.add_argument('-t', '--tool')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        os.path.isfile(args.fasta) or os.path.isfile(args.plink)
    except:
        usage()
        sys.exit(2)

    if not args.step:
        args.step = '123'
    if not args.tool:
        args.tool = 'phylip'

    if not args.fasta and args.plink and '1' in args.step:
        #Plink to fasta with option of prune
        #plink2fasta()
        pass
    elif os.path.isfile(args.fasta) and ('2' in args.step or '3' in args.step):
        #phylip tree from phylip format alignment
        phy_file = '%s.phy' %(os.path.splitext(args.fasta)[0])
        if '2' in args.step:
            fasta2phy(args.fasta, phy_file)
        if '3' in args.step:
            if args.tool == 'phylip':
                phylip_tree_run(phy_file)

if __name__ == '__main__':
    main()

