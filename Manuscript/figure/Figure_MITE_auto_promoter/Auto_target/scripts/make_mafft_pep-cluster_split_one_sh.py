#!/usr/bin/env python

import sys
import os
import fnmatch
import os.path
import subprocess as subp
import fastaIO



top = '''#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --mem=40G
#SBATCH --time=40:00:00
#SBATCH --output=slurm.stdout
#SBATCH -p intel
#SBATCH --workdir=./

module load mafft

'''

middle = '''mafft --ep 0.15 --op 1.55 --thread %s --localpair --maxiterate 16 ''' %(sys.argv[3])

files = os.listdir(sys.argv[1])
out_handle = open("mafft" + ".sh", "w")
print >> out_handle, top
for filename in files:
    if fnmatch.fnmatch(filename, sys.argv[2]):
        path = os.path.join(sys.argv[1], filename)
        c = 0
        with open(path, "r") as f:
            for title, seq in fastaIO.FastaGeneralIterator(f):
                c += 1
        if c >= 200:
            print "Shuffling and splitting file for seperate alignments\n"
            split_list, copies = fastaIO.shuffle_split(path, 200)
            for new_path in split_list:
                out = new_path + ".msa"                
                mem = 200
                full = middle + path + " > " + out
                print>>out_handle, full
        else:
            out = os.path.splitext(path)[0] + ".msa"
            full = middle + path + " > " + out
            print>>out_handle, full
           
print >>out_handle, '\n\necho "Done"' 
out_handle.close()

