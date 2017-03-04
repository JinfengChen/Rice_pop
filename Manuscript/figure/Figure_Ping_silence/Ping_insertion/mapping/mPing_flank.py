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
python mPing_flank.py --list Ping.list --fasta mPing_Ping_Pong.fa
python mPing_flank.py --list mPing.list --fasta mPing_Ping_Pong.fa

Make flanking sequence and mPing/Ping for methylation
--list:
Chr1:4220010..4220012	ping	+
Chr3:28019800..28019802	ping	+
Chr7:26460307..26460309	ping	+

    '''
    print message

def complement(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    bases = list(seq)
    for i in range(len(bases)):
        bases[i] = complement[bases[i]] if complement.has_key(bases[i]) else bases[i]
    return ''.join(bases)

def reverse_complement(seq):
    return complement(seq[::-1])


def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = str(record.seq)
    return fastaid

#Chr1:4220010..4220012	ping	+
#Chr1:4220010..4220012	ping
#mping.Chr10_21829433_21829435 mping.rc mping A119_2 Chr10:21829433..21829435 FLANK1:1..600 TSD1:598..600 TE:601..1030 TSD2:1031..1033 FLANK2:1031..1630
def flank_seq(infile, mping, ref, output):
    data   = defaultdict(str)
    fl_len = 1000
    r = re.compile(r'(\w+):(\d+)\.\.(\d+)')
    ofile = open(output, 'w')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit     = re.split(r'\t',line)
                strand   = 'NA'
                
                if len(unit) == 3:
                    strand = unit[2]
                str_key  = ''
                if strand == '+':
                    str_key = 'fwd'
                elif strand == '-':
                    str_key = 'rc'
                elif strand == '.':
                    str_key = 'UN'
                else:
                    continue
                chrs, start, end = r.search(unit[0]).groups(0) if r.search(unit[0]) else ['','','']
                if not chrs == '':
                    if int(end)-int(start) <= 3:
                        flank1 = ref[chrs][int(end)-fl_len:int(end)]
                        flank2 = ref[chrs][int(start)-1:int(start)+fl_len-1]
                        ins    = mping[unit[1]] 
                        ids    = '%s_%s_%s_%s %s.%s FLANK1:1..%s TSD1:%s..%s TE:%s..%s TSD2:%s..%s FLANK2:%s..%s' %(chrs, start, end, str_key, unit[1], str_key, fl_len, fl_len-2, fl_len, fl_len+1, fl_len+len(mping[unit[1]]), fl_len+len(mping[unit[1]])+1, fl_len+len(mping[unit[1]])+3, fl_len+len(mping[unit[1]])+1, fl_len+len(mping[unit[1]])+fl_len)
                        print >> ofile, '>%s' %(ids)
                        if strand == '+':
                            print >> ofile, '%s%s%s' %(flank1, ins, flank2)
                        else:
                            print >> ofile, '%s%s%s' %(flank1, reverse_complement(ins), flank2)
                    else:
                        flank1 = ref[chrs][int(start)-fl_len:int(start)-1]
                        flank2 = ref[chrs][int(end):int(end)+fl_len]
                        ins    = ref[chrs][int(start)-1:int(end)]
                        ids    = '%s_%s_%s_%s %s.%s FLANK1:1..%s TSD1:%s..%s TE:%s..%s TSD2:%s..%s FLANK2:%s..%s' %(chrs, start, end, str_key, unit[1], str_key, fl_len, fl_len-2, fl_len, fl_len+1, fl_len+len(mping[unit[1]]), fl_len+len(mping[unit[1]])+1, fl_len+len(mping[unit[1]])+3, fl_len+len(mping[unit[1]])+1, fl_len+len(mping[unit[1]])+fl_len)
                        print >> ofile, '>%s' %(ids)
                        print >> ofile, '%s%s%s' %(flank1, ins, flank2)
    ofile.close()
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list')
    parser.add_argument('-f', '--fasta')
    parser.add_argument('-g', '--genome')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.list) > 0 and len(args.fasta) > 0
    except:
        usage()
        sys.exit(2)
   
    if args.genome is None:
        args.genome = '/rhome/cjinfeng/BigData/00.RD/seqlib/MSU_r7.fa'

    if args.output is None:
        args.output = './mPing_flanking_1000.fa'

    mping = fasta_id(args.fasta)
    ref   = fasta_id(args.genome)
    flank_seq(args.list, mping, ref, args.output)
 
if __name__ == '__main__':
    main()

