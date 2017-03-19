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
python Select_Multiple_HighIdentity.py --input Target/Target_Run_2017_02_15_132003

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#calculate sequence identity between two aligned sequence
def calculate_identify(seq1, seq2):
    count = 0
    gap   = 0
    mm    = 0
    for n in range(0, len(seq1)):
        if seq1[n] == seq2[n]:
            if seq1[n] != '-':
                count = count + 1
            else:
                gap = gap + 1
        elif seq1[n] == '-' or seq2[n] == '-':
            gap = gap + 1
        else:
            mm = mm + 1
    seq_identity = float(count)/float(len(seq1)-gap)
    seq_align_len= len(seq1)-gap
    return seq_identity, seq_align_len

#3_MSU7.fa rice_3_118674_TSD_Len-3_31 364 /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/Ma Chr5  4 37 8572662 8572695 1 cccctttgaatcgcaggattgagaaaacgtagga cccctttgaatcgcaggattgagaaaacgtagga  47 336 8572696 8572966 1 ac
def sequence_identity(list_file, seq_id_dict):
    data = defaultdict(lambda : str())
    seq_identity_list  = []
    seq_align_len_list = []
    with open (list_file, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\s+',line)
                #print 'checking: %s' %(line)
                if seq_id_dict.has_key(unit[0]):
                    #print 'has key'
                    segments = unit[5:]
                    seq1 = ''
                    seq2 = ''
                    for i in range(len(segments)):
                        #print 'checking %s: %s, %s' %(i, i%7, segments[i])
                        if i%7 == 5:
                            seq1 = seq1 + segments[i]
                        elif i%7 == 6:
                            seq2 = seq2 + segments[i]
                    #print unit[0], unit[1], seq1, seq2
                    if len(seq1) != len(seq2):
                        #print 'different length of sequence'
                        continue 
                    seq_identity, seq_align_len = calculate_identify(seq1, seq2)
                    seq_identity_list.append(seq_identity)
                    seq_align_len_list.append(seq_align_len)
                else:
                    continue
                    #print 'no key: %s' %(unit[0])
    return np.mean(seq_identity_list), np.mean(seq_align_len_list)
 


def fasta_num(fastafile, query_len, cutoff, flank_len):
    fastaid = defaultdict(lambda : int())
    data = 0
    for record in SeqIO.parse(fastafile,"fasta"):
        #print float(len(str(record.seq)))-2*flank_len, float(query_len)*float(cutoff)
        if float(len(str(record.seq)))-2*flank_len <= float(query_len)*float(cutoff):
            #print 'sequence have <= 1.2 of query length: %s' %(record.id)
            fastaid[record.id] = 1
            data += 1
    return data, fastaid


#Fairchild_7_7738_TSD_Len-9_6    478     1       478     tig00000572_pilon       604449  382192  382690  0.91
def blast_identity(infile):
    data = defaultdict(lambda : int())
    data_len = defaultdict(lambda : int())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Query_id'):
                unit = re.split(r'\t', line)
                #print line
                #print unit[8]
                if (int(unit[3]) - int(unit[2]))/float(unit[1]) > 0.5:
                    align_len = str(int(unit[3]) - int(unit[2]))
                    index     = '%s:%s' %(align_len, unit[8])
                    data_len[index] += 1
                    data[unit[8]]   += 1
                    #print line
    data_sorted = sorted(data.items(), key=lambda x:x[1], reverse=True)
    data_len_sorted = sorted(data_len.items(), key=lambda x:x[1], reverse=True)
    return data_sorted, data_len_sorted


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

    #Target/Target_Run_2017_02_15_132003/Fairchild_MITEhunter10_split1/Fairchild_MITEhunter10_split1.blast
    query_dirs = glob.glob('%s/*_split*' %(args.input))
    ofile = open('%s.MITE_copy_identify.txt' %(args.input), 'w')
    print >> ofile, 'Target_Dirs\tQuery\tQueryLength\tNumberOfSequence\tTop_Identity:Top_Seq_Number\tTop_Align_Len:Top_Identity:Top_Seq_Number\ttTop_Align_Len\tTop_Identity\tTop_Seq_Number\tAvg_Identity\tAvgAlignLength' 
    for d in sorted(query_dirs):
        d_name = os.path.split(d)[1]
        blast = '%s/%s.blast' %(d, d_name)
        blast_table = '%s/%s.blast.table' %(d, d_name)
        list_file   = '%s/%s.list' %(d, d_name)
        cmd = 'grep "Query=" %s | sed "s/Query= //"' %(blast)
        query_name = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip() 
        print d, d_name, query_name
        #blast = '%s/%s.blast' %(d, d_name)
        #blast_table = '%s/%s.blast.table' %(d, d_name)
        #seq   = '%s/%s.flank_filter-1.2_under' %(d, d_name)
        seq   = '%s/%s.flank' %(d, d_name) 
        if not os.path.exists(blast_table) and os.path.exists(seq) and os.path.exists(blast):
            os.system('perl ~/BigData/software/bin/blast_parser.pl %s > %s' %(blast, blast_table))
            query_len_cmd = 'tail -n 1 %s | cut -f2' %(blast_table)
            query_len     = subprocess.Popen(query_len_cmd, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
            seq_n, seq_id = fasta_num(seq, query_len, 1.2, 200)
            top_id, top_id_len = blast_identity(blast_table)
            identity_avg, align_len_avg = sequence_identity(list_file, seq_id) 
            #print top_id
            #print top_id[1][0]
            print >> ofile, '%s\t%s\t%s\t%s\t%s:%s\t%s:%s\t%s\t%s\t%s\t%s' %(d, query_name, query_len, seq_n, top_id[0][0], top_id[0][1], top_id_len[0][0], top_id_len[0][1], '\t'.join(re.split(r':', top_id_len[0][0])), top_id_len[0][1], identity_avg, align_len_avg)
        elif os.path.exists(blast_table) and os.path.exists(seq) and os.path.exists(blast):
            query_len_cmd = 'tail -n 1 %s | cut -f2' %(blast_table)
            query_len     = subprocess.Popen(query_len_cmd, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
            seq_n, seq_id = fasta_num(seq, query_len, 1.2, 200)
            top_id, top_id_len = blast_identity(blast_table)
            identity_avg, align_len_avg = sequence_identity(list_file, seq_id)
            print >> ofile, '%s\t%s\t%s\t%s\t%s:%s\t%s:%s\t%s\t%s\t%s\t%s' %(d, query_name, query_len, seq_n, top_id[0][0], top_id[0][1], top_id_len[0][0], top_id_len[0][1], '\t'.join(re.split(r':', top_id_len[0][0])), top_id_len[0][1], identity_avg, align_len_avg)
        else:
            print 'check blast and sequence files!'
    ofile.close()
    os.system("cut -f1-4,10,11 %s.MITE_copy_identify.txt | awk '$4>0'  > %s.MITE_copy_identify.brief.txt" %(args.input, args.input))
if __name__ == '__main__':
    main()

