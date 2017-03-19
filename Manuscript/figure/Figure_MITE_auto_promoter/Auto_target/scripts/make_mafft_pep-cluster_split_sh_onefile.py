#!/usr/bin/env python

import sys
import os
import fnmatch
import os.path
import subprocess as subp
import fastaIO



top = '''#!/bin/bash
#PBS -l nodes=1:ppn=8,mem='''
middle = '''g

/usr/bin/mafft --ep 0.15 --op 1.55 --thread 8 --localpair --maxiterate 16 --out '''


path = sys.argv[1]
c = 0
with open(path, "r") as f:
    for title, seq in fastaIO.FastaGeneralIterator(f):
        c += 1
if c >= 201:
    print "Shuffling and splitting file for seperate alignments\n"
    split_list, copies = fastaIO.shuffle_split(path, 200)
    for new_path in split_list:
        out = new_path + ".msa"
        new_filename = os.path.split(new_path)[1]
        base = os.path.split(new_filename)[1]
        mem = 200
        full = top + str(mem) + middle + out + " " + new_path
        out_handle = open("mafft_" + new_filename + ".sh", "w")
        print>>out_handle, full
        out_handle.close()
        
        
else:
    mem = 0
    if c <= 10:
        mem = 24
    elif 10 < c <= 20:
        mem = 32
    elif 20 < c <= 30:
        mem = 40
    elif 30 < c <= 50:
        mem = 50
    elif 50 < c <= 75:
        mem = 70
    elif 75 < c <= 100:
        mem = 130
    elif 100 < c <= 200:
        mem = 200
    out = os.path.splitext(path)[0] + ".msa"
    full = top + str(mem) + middle + out + " " + path
    base = os.path.split(path)[1]
    out_handle = open("mafft_" + base + ".sh", "w")
    print>>out_handle, full
    out_handle.close()

