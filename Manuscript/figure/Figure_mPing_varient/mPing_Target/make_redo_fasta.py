#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def usage():
    test="name"
    message='''
python make_redo_fasta.py Target/Target_Run_unique_group.redo.list initial_data/AaegL3.MH_RM/query/AedesL3_unique.fa

initial_data/AaegL3.MH_RM/query/AedesL3_unique.split.list should be there with initial_data/AaegL3.MH_RM/query/AedesL3_unique.fa

    '''
    print message

#>AaegL3_1_401158_trim
def write_fasta(fastafile, id_list):
    count = 0
    out_list = defaultdict(lambda : str())
    out_dir  = '%s.redo' %(os.path.splitext(fastafile)[0])
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    ofile1 = open ('%s/%s.redo_1k.fa' %(out_dir, os.path.splitext(os.path.split(fastafile)[1])[0]), 'w')
    ofile2 = open ('%s/%s.redo_1kto3k.fa' %(out_dir, os.path.splitext(os.path.split(fastafile)[1])[0]), 'w')
    ofile3 = open ('%s/%s.redo_3k.fa' %(out_dir, os.path.splitext(os.path.split(fastafile)[1])[0]), 'w')
    for record in SeqIO.parse(fastafile, "fasta"):
        new_id = str(record.id).replace(r'#', '_').replace(r'/', '_').replace(r'?', '')
        if id_list.has_key(new_id):
            newrecord = SeqRecord(record.seq, id=new_id, description="")
            ofile4 = open ('%s/%s.fa' %(out_dir, id_list[new_id]), 'w')
            if len(str(record.seq)) <= 1000:
                SeqIO.write(newrecord, ofile1, "fasta")
                SeqIO.write(newrecord, ofile4, "fasta")
            elif len(str(record.seq)) <= 3000:
                SeqIO.write(newrecord, ofile2, "fasta")
                SeqIO.write(newrecord, ofile4, "fasta")
            else:
                SeqIO.write(newrecord, ofile3, "fasta")
                SeqIO.write(newrecord, ofile4, "fasta")
            count += 1
            out_list[new_id]
    print '%s of sequence output' %(count)
    ofile1.close()
    ofile2.close()
    ofile3.close()
    for id_i in sorted(id_list.keys()):
        if not out_list.has_key(id_i):
            print id_i


##AedesL3_unique_split447.flank_filter-1.2_under
def read_redo_list(infile):
    data = defaultdict(str)
    r    = re.compile(r'(.*)\.flank_filter*')
    count= 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                sid  = ''
                if r.search(unit[0]):
                    sid = r.search(unit[0]).groups(0)[0]
                    #count += 1
                if not data.has_key(sid):
                    data[sid] = 1
                    count += 1
    print '%s of redo sequence' %(count)
    return data

##AedesL3_unique_split1   AaegL3_1_401158_trim
def read_split_list(infile, redo_id):
    data = defaultdict(str)
    count= 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if redo_id.has_key(unit[0]):
                    data[unit[1]] = unit[0]
                    count += 1
    print '%s of id matched' %(count)
    return data

def main():
    if not len(sys.argv) == 3:
        usage()
        sys.exit(2)

    split_file = '%s.split.list' %(os.path.splitext(sys.argv[2])[0]) 
    redo_id    = read_redo_list(sys.argv[1])
    id_list    = read_split_list(split_file, redo_id)
    write_fasta(sys.argv[2], id_list)

if __name__ == '__main__':
    main()

