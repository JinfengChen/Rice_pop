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
python Select_Multiple_HighIdentity.py --input Target/Target_Run_2017_02_15_132003

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_num(fastafile):
    fastaid = defaultdict(str)
    data = 0
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
        data += 1
    return data


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
    print 'Target_Dirs\tNumberOfSequence\tTop_Identity:Top_Seq_Number\tTop_Align_Len:Top_Identity:Top_Seq_Number' 
    for d in sorted(query_dirs):
        d_name = os.path.split(d)[1]
        #print d, d_name
        blast = '%s/%s.blast' %(d, d_name)
        blast_table = '%s/%s.blast.table' %(d, d_name)
        seq   = '%s/%s.flank_filter-1.2_under' %(d, d_name) 
        if not os.path.exists(blast_table) and os.path.exists(seq) and os.path.exists(blast):
            seq_n = fasta_num(seq)
            os.system('perl ~/BigData/software/bin/blast_parser.pl %s > %s' %(blast, blast_table)) 
            top_id, top_id_len = blast_identity(blast_table)
            #print top_id
            #print top_id[1][0]
            print '%s\t%s\t%s:%s\t%s:%s' %(d, seq_n, top_id[0][0], top_id[0][1], top_id_len[0][0], top_id_len[0][1])
        elif os.path.exists(blast_table) and os.path.exists(seq) and os.path.exists(blast):
            seq_n = fasta_num(seq)
            top_id, top_id_len = blast_identity(blast_table)
            print '%s\t%s\t%s:%s\t%s:%s' %(d, seq_n, top_id[0][0], top_id[0][1], top_id_len[0][0], top_id_len[0][1])
if __name__ == '__main__':
    main()

