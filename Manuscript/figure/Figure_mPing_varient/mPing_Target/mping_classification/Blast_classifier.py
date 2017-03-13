#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
import glob
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
sys.path.append('/rhome/cjinfeng/BigData/software/ProgramPython/lib')
from utility import gff_parser, createdir
import networkx as nx

def usage():
    test="name"
    message='''
python Blast_classifier.py --input rice3k.9.mPing.clean.Nclean.mPing_var.blast.table

Use blast results to classfy sequence and generate fasta of representive sequence

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def sub_fasta_seq(fastafile, seq_list):
    fasta_s = defaultdict(lambda : str())
    for record in SeqIO.parse(fastafile,"fasta"):
        if seq_list.has_key(record.id):
            fasta_s[record.id] = record.seq
    return fasta_s

#Query_id        Query_length    Query_start     Query_end       Subject_id      Subject_length  Subject_start   Subject_end     Identity        Positive        Gap     Align_length    Score
#1_rice3k.fa.9   450     1       450     mPingD  450     1       450     1       --      0       450     892     0.0     Query:mPing_TSD-UNKSbjct:ERS468296

def blast_classifier(infile):
    data = defaultdict(str)
    blast_g = nx.Graph()
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Query_id'): 
                unit = re.split(r'\t',line)
                #not self hit
                if not unit[0] == unit[4]:
                    #query and target are 100% aligned without gap and mismatch
                    if int(unit[11]) == int(unit[1]) and int(unit[11]) == int(unit[5]) and int(unit[10]) == 0 and float(unit[8]) == 1:
                        blast_g.add_edge(unit[0], unit[4])
    #write representive id
    blast_g_sub = list(nx.connected_component_subgraphs(blast_g))
    rank = 0
    reprensentive = defaultdict(lambda : str())
    ofile_class = open('%s.class' %(infile), 'w')
    ofile_representive = open('%s.representive.fa' %(infile), 'w')
    for subgraph in blast_g_sub:
        rank += 1
        node = 'node%s' %(rank)
        print >> ofile_class, 'node%s: %s\t%s' %(rank, subgraph.number_of_nodes(), ','.join(subgraph.nodes()))
        rep_id = sorted(subgraph.nodes())[0]
        reprensentive[rep_id] = node
    #write representive fasta
    fastafile = re.sub(r'.blast.table', r'.fa', infile)
    rep_seq = sub_fasta_seq(fastafile, reprensentive)
    for seq_id in rep_seq.keys():
        rep_record = SeqRecord(rep_seq[seq_id], id=seq_id, name=seq_id, description=reprensentive[seq_id])
        SeqIO.write(rep_record, ofile_representive, 'fasta') 
    ofile_class.close()
    ofile_representive.close()


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

    blast_classifier(args.input)

if __name__ == '__main__':
    main()

