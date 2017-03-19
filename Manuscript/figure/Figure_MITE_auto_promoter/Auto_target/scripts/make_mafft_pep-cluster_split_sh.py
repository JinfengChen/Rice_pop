#!/usr/bin/env python

import sys
import os
import fnmatch
import os.path
import subprocess as subp
import fastaIO



top = '''#!/bin/bash
#PBS -l nodes=1:ppn='''

middle1 = ''',walltime=48:00:00,mem='''
middle2 = '''gb

/usr/bin/mafft --ep 0.15 --op 1.55 --thread '''

middle3 = ''' --localpair --maxiterate 16 --out '''
tag = sys.argv[3]
proc = 12
files = os.listdir(sys.argv[1])
for filename in files:
    if fnmatch.fnmatch(filename, sys.argv[2]):
        path = os.path.join(sys.argv[1], filename)
        c = 0
        with open(path, "r") as f:
            for title, seq in fastaIO.FastaGeneralIterator(f):
                c += 1
        if c >= 200:
            proc = 12
            print "Shuffling and splitting file for seperate alignments\n"
            split_list, copies = fastaIO.shuffle_split(path, 200)
            for new_path in split_list:
                out = new_path + ".msa"                
                mem = 200
                full = top + str(proc) + middle1 + str(mem) + middle2 + str(proc) + middle3 + out + " " + path
                out_handle = open("mafft_" + tag + "_" + filename + "_200.sh", "w")
                print>>out_handle, full
                out_handle.close()
                
                
        else:
            mem = 0
            end = ''
            if c <= 8:
                mem = 15
                end = "_15.sh"
                proc = 6
            elif 8 < c <= 20:
                mem = 34
                end = "_34.sh"
                proc = 12
            elif 20 < c <= 30:
                mem = 44
                end = "_44.sh"
                proc = 12
            elif 30 < c <= 50:
                mem = 68
                end = "_68.sh"
                proc = 12
            elif 50 < c <= 75:
                mem = 95
                end = "_95.sh"
                proc = 12
            elif 75 < c <= 100:
                mem = 150
                end = "_190.sh"
                
                proc = 12
            elif 100 < c < 200:
                mem = 200
                end = "_200.sh"
                proc = 12
            out = os.path.splitext(path)[0] + ".msa"
            full = top + str(proc) + middle1 + str(mem) + middle2 + str(proc) + middle3 + out + " " + path
            out_handle = open("mafft_" + tag + "_" + filename + end, "w")
            print>>out_handle, full
            out_handle.close()

