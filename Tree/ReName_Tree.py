#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
from ete2 import Tree

def usage():
    test="name"
    message='''
python ReName_Tree.py --input test.3000.phy.tree --fasta test.3000.fasta

Rename the sample name in tree because phyilp only accept 10 characters for that. We use sample name
in fasta to replace the sample in tree.
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(lambda : str())
    for record in SeqIO.parse(fastafile,"fasta"):
        s_id  = str(record.id).replace(r'IRIS_313-', r'I')
        fastaid[s_id] = str(record.id)
        #print '%s\t%s' %(s_id, fastaid[s_id])
    return fastaid


def convert_tree(infile, id_dict):
    tree_file = '%s.formal_id.tree' %(os.path.splitext(infile)[0])
    tree_t = Tree(infile, format=1) 
    for node in tree_t.traverse("postorder"):
        #print '%s\t%s' %(node.name, id_dict[node.name])
        if id_dict.has_key(node.name):
            node.name = id_dict[node.name]
    tree_t.write(format=1, outfile=tree_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-f', '--fasta')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    id_dict = fasta_id(args.fasta)
    convert_tree(args.input, id_dict)

if __name__ == '__main__':
    main()

